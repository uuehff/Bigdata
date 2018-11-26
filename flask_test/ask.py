import requests

# r = requests.post('http://127.0.0.1:5000', data={'aaaaaaa':'bbbbbbbb','cc':'dd'})
r = requests.post('http://127.0.0.1:8081/login', {"username":"a","password":"b"})

print r
# print r.text
# print r.content