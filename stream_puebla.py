 from TwitterAPI import TwitterAPI
from ws4py.client.threadedclient import WebSocketClient
import unicodedata

def remove_special_characters(s):
           '''
             Removing specaial characters

             In:
                   (s:string) text string
             Out:
                   (string) text string free of special characters in unicode
           '''
           PRINTABLE = set(('Lu', 'Ll', 'Zs'))
           if isinstance(s, str):
               s = unicode(s, "utf-8", "xmlcharrefreplace")
           result = []
           for word in s:
               word = unicodedata.category(word) in PRINTABLE and word or u'#'
               result.append(word)
           return u''.join(result).replace(u'#', u' ')


class DummyClient(WebSocketClient):

    def opened(self):
      TRACK_TERM = "Puebla"

      CONSUMER_KEY = '9pBBabr7MpVbpOk7YPOx3RjYy'
      CONSUMER_SECRET = 'LH7A7jMjQqYXNK07WOIKqZv9tEBrovDmWv40Sg2Md61EjwPdEj'
      ACCESS_TOKEN_KEY = '19495636-lcYOEgKPfOp4xky5CTGQwzf5VdZuIcVV1ifGOi3ss'
      ACCESS_TOKEN_SECRET = 'I4O0FciZA8HxqGgC6jEz6oS21kHWObPChLpI9Syd299Jf'

      api = TwitterAPI(
          CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN_KEY,
          ACCESS_TOKEN_SECRET)

      r = api.request("statuses/filter", {"track":TRACK_TERM})
      for item in r.get_iterator():
        print item["text"]
        self.send('{"path": "cards-manager/871c707f-bb9b-49c8-bf69-07195cfbc8db", "message": "comment", "content": "'+remove_special_characters(item["text"]).encode("utf-8")+'"}')

if __name__ == '__main__':
  try:
      ws = DummyClient('ws://localhost:8080/ws')
      ws.connect()
      ws.run_forever()
  except KeyboardInterrupt:
      ws.close()
