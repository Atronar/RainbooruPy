from .request import request_comments
from .comment import Comment
from .helpers import set_limit

__all__ = [
  "Comments"
]

class Comments(object):
  def __init__(self, limit=50, image_id="", proxies={}):
    self.proxies = proxies
    self._limit = set_limit(limit)
    self._image_id = set_limit(image_id)
    self._search = request_comments(self._image_id, limit=self._limit, proxies=self.proxies)
  
  def __iter__(self):
    return self

  def limit(self, limit):
    params = {"limit": limit, "image_id": self._image_id, "proxies": self.proxies}

    return self.__class__(**params)

  def image_id(self, image_id):
    params = {"limit": self._limit, "image_id": image_id, "proxies": self.proxies}

    return self.__class__(**params)

  def __next__(self):
    """
    Returns a result wrapped in a new instance of Comment().
    """
    return Comment(next(self._search), proxies=self.proxies)
