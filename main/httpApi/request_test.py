# encoding:utf-8
import requests

r = requests.post('http://127.0.0.1:5000', data={'aaaaaaa':'bbbbbbbb','cc':'dd'})

# print r.text
print r.content

