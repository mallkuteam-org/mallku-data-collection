import csv
import itertools

import pandas as pd
import requests
import xmltodict

from domain.Filter import Filter
from domain.Result import Result
from domain.User import User
from ast import literal_eval


def get_links():
    users = get_users()
    auth = {
        "user": users[0].username,
        "password": users[0].password
    }

    filters = get_filters()
    for filter in filters:
        query = build_query(filter)
        response = requests.get(
            query,
            auth=requests.auth.HTTPBasicAuth(auth['user'], auth['password']))
        json_response = response.json()
        results = get_results_from_json(json_response, auth, filter)

        users_iter = itertools.cycle(users)
        for result, user in zip(results, users_iter):
            add_row_csv(result, user)


def build_query(filter):
    limit = filter.limit if filter.limit is not None else 100
    query = f'https://scihub.copernicus.eu/dhus/search?format=json&start=0&rows={int(limit)}&q='
    if filter.coordinates is not None:
        query += f'footprint:"Intersects{filter.coordinates}"'
    elif filter.polygon is not None:
        query += f'footprint:"Intersects(POLYGON({filter.polygon}))"'

    if filter.begin_position is not None:
        query += f' AND beginposition:{filter.begin_position}'
    if filter.end_position is not None:
        query += f' AND endposition:{filter.end_position}'
    if filter.product_type is not None:
        query += f' AND producttype:{filter.product_type}'
    if filter.cloud_cover_percentage is not None:
        query += f' AND cloudcoverpercentage:{filter.cloud_cover_percentage}'
    if filter.order_by is not None:
        query += f'&orderby={filter.order_by}'

    return query


def get_users():
    df = pd.read_csv("utils/users.csv")
    users = []
    for index, row in df.iterrows():
        users.append(User(row["username"], row["password"]))
    return users


def get_filters():
    df = pd.read_csv("utils/filters.csv")
    filters = []
    for index, row in df.iterrows():
        filter = Filter()
        if not isNaN(row["coords"]):
            filter.coordinates = row["coords"]
        if not isNaN(row["polygon"]):
            filter.polygon = row["polygon"]
        if not isNaN(row["beginposition"]):
            filter.begin_position = row["beginposition"]
        if not isNaN(row["endposition"]):
            filter.end_position = row["endposition"]
        if not isNaN(row["producttype"]):
            filter.product_type = row["producttype"]
        if not isNaN(row["cloudcoverpercentage"]):
            filter.cloud_cover_percentage = row["cloudcoverpercentage"]
        if not isNaN(row["orderby"]):
            filter.order_by = row["orderby"]
        if not isNaN(row["limit"]):
            filter.limit = row["limit"]
        if not isNaN(row["imagezooms"]):
            filter.image_zooms = literal_eval(row["imagezooms"])
        if not isNaN(row["bands"]):
            filter.bands = literal_eval(row["bands"])
        filters.append(filter)
    return filters


def get_results_from_json(json_file, auth, filter):
    results = []
    entries = json_file['feed']['entry']
    for entry in entries:
        manifest_link = f"https://scihub.copernicus.eu/dhus/odata/v1/Products('{entry['id']}')" \
                   f"/Nodes('{entry['title']}.SAFE')" \
                   "/Nodes('MTD_MSIL2A.xml')/$value"
        response = requests.get(
            manifest_link,
            auth=requests.auth.HTTPBasicAuth(auth['user'], auth['password']))

        if response.status_code != 200:
            print(f"Status code {response.status_code} for manifest link = {manifest_link}")
            continue
        xml_string = response.text
        results.extend(get_results_from_xml(xml_string, entry['id'], filter))
    return results


def get_results_from_xml(xml_string, product_id, filter):
    results = []
    xml_dict = xmltodict.parse(xml_string)
    product_uri = xml_dict['n1:Level-2A_User_Product']['n1:General_Info']['Product_Info']['PRODUCT_URI']
    image_files = xml_dict['n1:Level-2A_User_Product']['n1:General_Info']['Product_Info']['Product_Organisation']['Granule_List']['Granule']['IMAGE_FILE']
    for file in image_files:
        file_parts = file.split("/")
        zoom_and_band = file_parts[4][-7:]
        zoom = zoom_and_band[-3:]
        band = zoom_and_band[:3]
        if filter.image_zooms is not None and zoom not in filter.image_zooms:
            continue
        if filter.bands is not None and band not in filter.bands:
            continue
        link = f"https://scihub.copernicus.eu/dhus/odata/v1/Products('{product_id}')" \
               f"/Nodes('{product_uri}')" \
               f"/Nodes('{file_parts[0]}')" \
               f"/Nodes('{file_parts[1]}')" \
               f"/Nodes('{file_parts[2]}')" \
               f"/Nodes('{file_parts[3]}')" \
               f"/Nodes('{file_parts[4]}.jp2')" \
               f"/$value"
        results.append(Result(link, band, zoom, product_id))
    return results


def add_row_csv(result: Result, user):
    with open(r'utils/links.csv', 'a', newline='') as csvfile:
        fieldnames = ['link', 'band', 'zoom', 'uuid', 'is_downloaded', 'username', 'password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'link': result.link,
                         'band': result.band,
                         'zoom': result.zoom,
                         'uuid': result.uuid,
                         'is_downloaded': result.is_downloaded,
                         'username': user.username,
                         'password': user.password
                         })


def isNaN(value):
    return value != value
