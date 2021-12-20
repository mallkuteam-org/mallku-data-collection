import requests
import argparse
from tqdm import tqdm

def download_file(url, output_filename, user, password):

    # Streaming, so we can iterate over the response.
    response = requests.get(url, auth=(user, password), stream=True)
    total_size_in_bytes= int(response.headers.get('content-length', 0))
    block_size = 4*1024 #1 Kibibyte
    progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
    with open("downloads/"+output_filename, 'wb') as file:
        for data in response.iter_content(block_size):
            progress_bar.update(len(data))
            file.write(data)
    progress_bar.close()
    if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
        print("ERROR, something went wrong")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="url to download")
    parser.add_argument("-u","--user", help="user")
    parser.add_argument("-p","--password", help="password")

    parser.add_argument("-o","--output", help="output filename")
    args = parser.parse_args()

    url = args.url

    user = args.user
    password = args.password
    output_filename = args.url.split('\'')[1]
    output_filename = output_filename + ".zip"
    download_file(url, output_filename, user, password)

if __name__=="__main__":
    main()



