import os
import urllib.request
import json
import time
import http.client

with open('C:/TEST FINAL YEAR/image.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i in data:
    url = i['url']
    file_name = os.path.join('C:/TEST FINAL YEAR/Restaurant_Core/static/photo', i['image_name'])
    if os.path.exists(file_name):
        print(f"File '{file_name}' already exists. Skipping download...")
        continue
    else:
        try:
            urllib.request.urlretrieve(url, file_name)
            print(f"Downloaded '{file_name}'")
            time.sleep(0.1)
        except (urllib.error.HTTPError, urllib.error.URLError, http.client.RemoteDisconnected) as e:
            print(f"Download of '{file_name}' failed with error: {e}. Retrying in 10 seconds...")
            time.sleep(10)
            continue
