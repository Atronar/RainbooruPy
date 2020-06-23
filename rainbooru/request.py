import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from .helpers import wilson_score, format_params

__all__ = [
  "get_page_data", "get_image_data", "request_comments", "get_comment", "url"
]

def get_page_data(url, proxies={}):
  request = requests.get(url, proxies=proxies)

  if request.status_code == requests.codes.ok:
    page = request.text
    return page

def get_page_image_data(img_number, proxies={}):
  url = f"https://www.rainbooru.org/img/{img_number}"

  return get_page_data(url, proxies=proxies)

def get_image_data(id_number, proxies={}):
  page = get_page_image_data(id_number, proxies)

  if page:
    data = {}

    #if data["image"]["duplicate_of"]:
    #  return get_image_data(data["image"]["duplicate_of"], proxies=proxies)
    #else:
    #  return data["image"]
    soup = BeautifulSoup(page,'lxml')

    data['id'] = int(id_number)

    metas = soup.findAll('meta')
    for meta in metas:
       if meta.get("property")=="og:image":
          data['view_url'] = meta.get("content")
          filename = data['view_url'].rsplit('/',1)[-1]
          data['representations'] = {size: f'https://cdn.rainbooru.org/file/rainbooru/{size}/{filename}'
                                     for size in ('full','medium','thumb')}
          data['format'] = filename.rsplit('.',1)[-1]

    stats = soup.find('div',id="stats").extract().findAll('div','statelement')
    for stat in stats:
       if stat.a.text == "U":
          data['upvotes'] = int(stat.find('div','redout').text)
       elif stat.a.text == "D":
          data['downvotes'] = int(stat.find('div','redout').text)
       elif stat.a.text == "F":
          data['faves'] = int(stat.find('div','redout').text)
       elif stat.a.text == "H":
          data['hides'] = int(stat.find('div','redout').text)
    data['score'] = data['upvotes'] - data['downvotes']
    data['wilson_score'] = wilson_score(data['upvotes'], data['downvotes'])

    descs = soup.find('div',id='imdesc').extract().findAll('p')
    data['description'] = descs[0].text
    data['created_at'] = descs[1].text

    paragrs = soup.findAll('p')
    for paragr in paragrs:
       if paragr.text.startswith("Uploader:"):
          if paragr.a:
             data['uploader'] = paragr.a.text
             data['uploader_id'] = paragr.a.get("href").rsplit("/",1)[-1]
          else:
             data['uploader'] = None
             data['uploader_id'] = None

    #tags = soup.find('tagsection').extract().findAll('a','tag')
    tags = soup.findAll('a','tag')
    data['tags'] = [tag.text for tag in tags]
    data['tag_count'] = len(data['tags'])

    data['comment_count'] = len(soup.findAll('div','completecomment'))

    return data

def request_comments(img_number, limit=50, proxies={}):
  page = get_page_image_data(img_number, proxies)

  if page:
    soup = BeautifulSoup(page,'lxml')
    comments = soup.find('div', id='commentsection').extract()
    for comment in comments.findAll('div','completecomment',limit=limit):
       yield get_comment(comment, image_id=img_number)

def get_comment(comment_data, image_id=None):
   data = {}

   user = comment_data.find('div','username')
   if user.a:
      data['author'] = user.a.text.strip()
      data['user_id'] = user.a.get('href').rsplit("/",1)[-1]
   else:
      data['author'] = None
      data['user_id'] = None

   data['created_at'] = comment_data.find('div', 'comtimestamp').text
   data['body'] = comment_data.find('div','comment').text.strip()
   if image_id:
      data['image_id'] = image_id
   else:
      data['image_id'] = None

   return data

def url(params):
  p = format_params(params)
  if 'search' in p and p['search']:
     url = f"https://www.rainbooru.org/search?{urlencode(p)}"
  else:
     url = f"https://www.rainbooru.org/?{urlencode(p)}"
  return url

def get_images(params, limit=50, proxies={}):
  count = 0
  p = format_params(params)
  search = url(p)
  while count<limit:
     page = get_page_data(search, proxies=proxies)
     if not page:
        break
     soup = BeautifulSoup(page,'lxml').find('div',id='recent').extract()
     images = soup.findAll('a',limit=limit-count)
     if not images:
        break
   
     for image in images:
       id_number = image.get('href').rsplit("/",1)[-1]
       data = get_image_data(id_number, proxies=proxies)
       count += 1
       yield data

     p['page'] += 1
     search = url(p)