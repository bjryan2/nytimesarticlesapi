import requests
import urllib

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

  def _strip_dict(self, d):
    '''
    Strips out invalid fields form the dict
    '''

    valid_fields = {'q', 'fq', 'begin_date', 'end_date', 'sort', 'fl', 'h1', 'page', 'facet_field', 'facet_filter', 'request-type'}

    for item in d:
      if item not in valid_fields:
        del(d[item])

    return d


  def _format_fq(self, d):

    '''
    Formats the fq queries for proper lucene syntax
    '''

    #join lists of items into a single string
    for k, v in d.items():
      if isinstance(v, list):
        d[k] = " ".join(map(lambda x: '"{}"'.format(x), v))
      else:
        d[k] = '"{}"'.format(v)

    queries = []

    for k,v in d.items():
      q = '{}:({})'.format(k,v)
      queries.append(q)

    queries = ' AND '.join(queries)
    return queries


  def _utf8_enc(self,d):
    ''''
    encode all values into lowwecase and into utf8
    '''

    for k, v in d.items():

      d[k] = v.encode('utf8').lower()

      if isinstance(v, list):
        d[k] = map(lambda x: x.encode('utf8').lower(), v)

      if isinstance(v, dict):
        d[k] = self._utf8_enc('utf8', d)

    return d

  def _encode_qs(self, kwargs):
    '''
    encodes the url querystring
    '''

    kwargs = self._strip_dict(kwargs)
    kwargs = self._utf8_enc(kwargs)
    kwargs = self._boolean_encode(self, kwargs)

    val = []

    for k, v in kwargs.items():

      if k is 'fq' and isinstance(v, dict):
       v = self._format_fq(v)
      elif isinstance(v, list):
        v = ",".join(v)

      s = '{}={}'.format(k,v)
      val.append(s)

    qs = "&".join(val)

    return qs

  def search(self,
             response_format=None,
              **kwargs):
    '''
    Make a call to the NYTimes API

    Response format is JSON by default but could also be JSONP
    '''

    if response_format is None:
        response_format = self.response_format

    req_url = '{}{}?{}&api-key={}'.format(self.API_ROOT, response_format, self._encode_qs(**kwargs), self.key)

    r = requests.get(req_url)
    return r.json()

