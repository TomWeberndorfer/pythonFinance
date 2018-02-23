import requests

url = "http://api.meaningcloud.com/sentiment-2.1"

text = "Nvidia shares up nearly 12% premarket after company handily beat with earnings"

payload = "key=5c613f1d6fa057c2f11b837e6cf7d883&lang=en&txt=" + text
headers = {'content-type': 'application/x-www-form-urlencoded'}

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)