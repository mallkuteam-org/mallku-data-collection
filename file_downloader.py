from tqdm import tqdm
import requests

url = "https://scihub.copernicus.eu/dhus/odata/v1/Products('7002027f-b898-4c36-a9ef-00fcf71205c1')/$value" #big file test
user, password = 'vshoijet', 'vero3580'

# Streaming, so we can iterate over the response.
response = requests.get(url, auth=(user, password), stream=True)
total_size_in_bytes= int(response.headers.get('content-length', 0))
block_size = 1024 #1 Kibibyte
progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
with open('test.zip', 'wb') as file:
    for data in response.iter_content(block_size):
        progress_bar.update(len(data))
        file.write(data)
progress_bar.close()
if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
    print("ERROR, something went wrong")



