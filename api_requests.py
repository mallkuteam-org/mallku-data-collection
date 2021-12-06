import requests


def make_query(username, password):
    auth = {
        "user": username,
        "password": password
    }

    response = requests.get(
        "https://scihub.copernicus.eu/dhus/search?q=footprint:%22Intersects(-31.4166,%20-64.1833)%22",
        auth=requests.auth.HTTPBasicAuth(auth['user'], auth['password']))
    return response
