import requests

url = "https://embeddia.texta.ee/api/v1/comment_analyzer/"

data = {"text": "mine munni"}

for i in range(0,100):

    response = requests.post(url, data=data)
    print(response.status_code)