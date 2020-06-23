__all__ = [
  "Comment"
]

class Comment(object):
  def __init__(self, data, proxies={}):
    self.proxies = proxies
    self._data = data
    for field, body in self.data.items():
      if not hasattr(self, field):
        setattr(self, field, body)

  def __str__(self):
    return '''Comment({}: "{}")'''.format(self.author if self.author else 'anonymous',
                                          self.body.replace('\r','').strip().split('\n',1)[0][:27]+'...' \
                                            if len(self.body.replace('\r',''))>30 \
                                            else self.body.replace('\r','').strip().split('\n',1)[0]
                                         )

  @property
  def data(self):
    return self._data