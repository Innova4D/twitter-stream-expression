from TwitterAPI import TwitterAPI
from ws4py.client.threadedclient import WebSocketClient
import unicodedata
import gzip

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
      TRACK_TERM = "Corona Capital"

      CONSUMER_KEY = 'vp4vDnkSY5RiozYE7ljBuxSCN'
      CONSUMER_SECRET = 'Wn1THfpm2H8Tc5ruG7b9NsJzA3C966XaKWMkrAQuk7q4PC4lgT'
      ACCESS_TOKEN_KEY = '19495636-ijh8Wtv6MvSBXj4CsOx7LTIdECQ6cNeWlES7jFjO5'
      ACCESS_TOKEN_SECRET = 'b163IxuQDj72zPAK0ec50lvMzMZ2bW2ZRBwm3oM28UeZr'

      api = TwitterAPI(
          CONSUMER_KEY,
          CONSUMER_SECRET,
          ACCESS_TOKEN_KEY,
          ACCESS_TOKEN_SECRET)

      r = api.request("statuses/filter", {"track":TRACK_TERM})
      print r.status_code
      for item in r:
        print item["text"]
        self.send('{"path": "cards-manager/4002ae38-0644-440d-8743-96226fcbf07c", "message": "comment", "content": "'+remove_special_characters(item["text"]).encode("utf-8")+'"}')

if __name__ == '__main__':
  try:
      ws = DummyClient('ws://localhost:8080/ws')
      ws.connect()
      ws.run_forever()
  except KeyboardInterrupt:
      ws.close()
