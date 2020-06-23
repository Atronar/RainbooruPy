from .request import get_images, url
from .image import Image
from .helpers import tags, join_params, set_limit

__all__ = [
  "Search"
]

class Search(object):
  def __init__(self, search=set(), limit=50, page=0, proxies={}):
    self.proxies = proxies
    self._params = {
      "search": tags(search),
      "page": set_limit(page)
    }
      
    self._limit = set_limit(limit)
    self._search = get_images(self._params, self._limit, proxies=self.proxies)
  
  def __iter__(self):
    return self

  @property
  def parameters(self):
    return self._params

  @property
  def url(self):
    """
    https://www.rainbooru.org/search?search=safe&page=1
    """
    return url(self.parameters)

  def query(self, *q):
    """
    Takes one or more strings for searching by tag and/or metadata.
    """
    params = join_params(self.parameters, {"search": q,
                                           "limit": self._limit,
                                           "proxies": self.proxies}
                        )

    return self.__class__(**params)

  def limit(self, limit):
    params = join_params(self.parameters, {"limit": limit, "proxies": self.proxies})

    return self.__class__(**params)

  def query_append(self,*q):
     """
     Adds tags to current search.
     """
     query = self.parameters['search'].union(q)
     params = join_params(self.parameters, {"search": query,
                                            "limit": self._limit,
                                            "proxies": self.proxies}
                         )

     return self.__class__(**params)

  def query_remove(self,*q):
     """
     Removes tags from current search.
     """
     query = self.parameters['search'].difference(q)
     params = join_params(self.parameters, {"search": query,
                                            "limit": self._limit,
                                            "proxies": self.proxies}
                         )

     return self.__class__(**params)

  def get_page(self,page):
    """
    Set page for gets result of search.
    """
    params = join_params(self.parameters, {"page": page,
                                           "limit": self._limit,
                                           "proxies": self.proxies}
                        )

    return self.__class__(**params)

  def __next__(self):
    return Image(next(self._search), proxies=self.proxies)
