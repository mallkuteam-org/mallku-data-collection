import requests
import itertools
import pandas as pd
from domain.User import User
from domain.Filter import Filter
from domain.Result import Result
import xml.etree.ElementTree as ET
import csv


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
        xml_string = response.text
        users_iter = itertools.cycle(users)

        results = get_processed_xml(xml_string)
        for result,user in zip(results,users_iter):
            add_row_csv(result,user)


def build_query(filter):
    query = 'https://scihub.copernicus.eu/dhus/search?q='
    if filter.coordinates is not None:
        query += f'footprint:"Intersects{filter.coordinates}"'
    elif filter.polygon is not None:
        query += f'footprint:"Intersects(POLYGON({filter.polygon}))"'
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
        if row["coords"] is not pd.np.nan:
            filter.coordinates = row["coords"]
        if row["polygon"] is not pd.np.nan:
            filter.polygon = row["polygon"]
        filters.append(filter)
    return filters


def get_processed_xml(xml_string):
    results = []
    tree = ET.ElementTree(ET.fromstring(xml_string))
    entries = tree.findall('.//{http://www.w3.org/2005/Atom}entry')

    for entry in entries:
        result = Result()
        entry_string = ET.tostring(entry)
        entry_tree = ET.ElementTree(ET.fromstring(entry_string))
        for element in entry_tree.iter():
            if element.tag == "{http://www.w3.org/2005/Atom}title" and result.title is None:
                print('-----------------------------')
                print('title: ', element.text)
                result.title = element.text
            if element.tag == "{http://www.w3.org/2005/Atom}link" and result.link is None:
                print('link: ', element.attrib['href'])
                result.link = element.attrib['href']
            if element.attrib == {'name': 'ingestiondate'} and result.ingestion_date is None:
                print('Ingestion Date: ', element.text)
                result.ingestion_date = element.text
            if element.attrib == {'name': 'size'} and result.size is None:
                print('Size: ', element.text)
                result.size = element.text
            if element.attrib == {'name': 'processinglevel'} and result.processing_level is None:
                print('Processing Level: ', element.text)
                result.processing_level = element.text
            if element.attrib == {'name': 'uuid'} and result.uuid is None:
                print('uuid: ', element.text)
                result.uuid = element.text
        results.append(result)
    return results


def add_row_csv(result: Result, user):
    with open(r'utils/links.csv', 'a', newline='') as csvfile:
        fieldnames = ['link', 'title', 'ingestion_date', 'processing_level', 'size', 'uuid', 'is_downloaded','username','password']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'link': result.link,
                         'title': result.title,
                         'ingestion_date': result.ingestion_date,
                         'processing_level': result.processing_level,
                         'size': result.size,
                         'uuid': result.uuid,
                         'is_downloaded': result.is_downloaded,
                         'username': user.username,
                         'password': user.password
                         })
