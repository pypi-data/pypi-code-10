import json
from requests import Response
from .http import Http
from .decorators import json_response_body


def repr(self):
  r = '{method} {url}\n'.format(method=self.request.method, url=self.request.url)
  if self.request.body:
    r += str(self.request.body) + '\n'
  r += '\n'
  for key, value in self.headers.items():
    r += '{key}: {value}\n'.format(key=key, value=value)
  r += '\n' + json.dumps(self.body, sort_keys=True, ensure_ascii=False, indent=2)
  return r

Response.__repr__ = repr

http = Http()
