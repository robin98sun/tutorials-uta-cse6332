import requests

# url = 'http://127.0.0.1:8080/data'
# myobj = {
#     'city_name': 'New Rome2',
#     'lat': 19.8987,
#     'lng': -155.6659,
#     'country': 'Utopia',
#     'state': 'Nowhere',
#     'population': '1442000',
#     # 'population': '0',
# }

# res = requests.put(url, json = myobj)

url = 'http://127.0.0.1:8080/data?city_name="New Rome"'
res = requests.delete(url)

print(res.text)
