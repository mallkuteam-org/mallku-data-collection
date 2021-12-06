import requests


def make_query(username, password):
    auth = {
        "user": username,
        "password": password
    }

    coordinates = [-31.4166, -64.1833]
    coords = 'footprint:"Intersects(' + str(coordinates[0]) + ',' + str(coordinates[1]) + ')"'

    response = requests.get(
        'https://scihub.copernicus.eu/dhus/search?q=' + coords,
        auth=requests.auth.HTTPBasicAuth(auth['user'], auth['password']))
    return response
