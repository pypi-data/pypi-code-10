import requests
from datetime import datetime
from fake_useragent import UserAgent
from pytz import timezone

ua = UserAgent()
HEADERS = {"User-Agent": ua.chrome}

def watch(url):
   try:
      return requests.get(url, headers=HEADERS).status_code
   except requests.exceptions.RequestException:
      return -1


def judge(status_code):
   now = datetime.now().strftime("%Y-%m-%d %H:%M")
   if status_code in (200, 302):
      return {"status": "up", "timestamp": now}
   else:
      return {"status": "down", "timestamp": now}

