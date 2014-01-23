import requests

class NoKeyException(Exception):
  '''
  Exception class for not providing an API key
  '''

  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class NYTArticleAPI(object):
  '''
  Python wrapper around the NYTimes Article Search API (version 2)
  '''

  def __init__(self, key = None):
    self.API_ROOT = 'http://api.nytimes.com/svc/search/v2/articlesearch'
    self.key = key
    self.response_format = 'json'

    if self.key is None:
        raise NoKeyException("You have not provided an API Key")



  def _boolean_encode(self,d):
    '''
    Converts python truth values to lowercase
    '''

    for key, value in d.items():
      if isinstance(value, bool):
        d[key] = str(value).lower()

    return d


  def search(self,
             response_format=None,
              **kwargs):
    '''
    Make a call to the NYTimes API

    Response format is JSON by default but could also be JSONP
    '''

    if response_format is None:
        response_format = self.response_format

    req_url = '{}{}?{}&api-key={}'.format(self.API_ROOT, response_format, self.options(**kwargs), self.key)

    r = requests.get(req_url)
    return r.json()

