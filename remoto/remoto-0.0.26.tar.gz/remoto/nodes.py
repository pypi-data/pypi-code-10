import requests

url = 'http://paddles.front.sepia.ceph.com/nodes/'

response = requests.get(url)

for i in response.json():
    print i['name']
