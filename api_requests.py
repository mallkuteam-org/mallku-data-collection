import requests
import json


def request_breeds_by_name(name=None, should_save=False):
    headers = {
        "x-api-key": "66459bdf-91d4-4bd1-bf14-6c3a4a241951"
    }

    params = {
        "q": name
    } if name is not None else None

    breeds_rs = requests.get("https://api.thecatapi.com/v1/breeds/search", headers=headers, params=params)
    breeds_json = breeds_rs.json()
    if should_save:
        with open(f'data/searched_breeds.json', 'w') as outfile:
            json.dump(breeds_json, outfile)

    return breeds_json


def request_my_votes(sub_id=None, limit=None, should_save=False):
    headers = {
        "x-api-key": "66459bdf-91d4-4bd1-bf14-6c3a4a241951"
    }

    params = {
        "sub_id": sub_id,
        "limit": limit
    } if sub_id is not None or limit is not None else None

    votes_rs = requests.get("https://api.thecatapi.com/v1/votes", headers=headers, params=params)
    votes_json = votes_rs.json()
    if should_save:
        with open(f'data/myvotes.json', 'w') as outfile:
            json.dump(votes_json, outfile)

    return votes_json


def post_my_vote(image_id, sub_id, value):
    headers = {
        "x-api-key": "66459bdf-91d4-4bd1-bf14-6c3a4a241951"
    }

    payload = {
        "image_id": image_id,
        "sub_id": sub_id,
        "value": value
    }

    response = requests.post("https://api.thecatapi.com/v1/votes", headers=headers, json=payload)
    return response
