from .request import get_image_data

__all__ = [
  "Image"
]

class Image(object):
  def __init__(self, data, image_id=None, proxies={}):
    self.proxies = proxies

    if data is None and image_id:
      self._data = data = get_image_data(image_id, proxies=proxies)
    else:
      self._data = data

    for field, body in data.items():
      if not hasattr(self, field):
        setattr(self, field, body) 

  def __str__(self):
    return f"Image({self.id})"

  @property
  def representations(self):
    sizes = self.data["representations"].items()
    images = { image: url for image, url in sizes }

    return images

  @property
  def full(self):
    return self.representations["full"]

  @property
  def medium(self):
    return self.representations["medium"]

  @property
  def thumb(self):
    return self.representations["thumb"]

  @property
  def image(self):
    return self.data["view_url"]

  def comments(self):
    return Comments(proxies=self.proxies).image_id(self.id)
       
  @property
  def url(self):
    return f"https://www.rainbooru.org/img/{self.id}"

  @property
  def data(self):
    return self._data

  def update(self):
    data = get_image_data(self.id, proxies=self.proxies)

    if data:
      self._data = data

  @property
  def artists(self):
    return [tag for tag in self.tags if tag.startswith('artist:')]

  @property
  def rating(self):
    all_ratings = {"safe","suggestive","questionable","explicit",
                   "semi-grimdark","grimdark","grotesque"}
    rating_tags = list(set(self.tags).intersection(all_ratings))
    return rating_tags

  @property
  def spoiler(self):
    return [tag for tag in self.tags if tag.startswith('spoiler:')]