#!/bin/bash

python3 main.py

FILENAME="utils/links.csv"

while IFS="," read -r link band zoom uuid is_downloaded username password
do
  echo "link: $link "
  echo "band: $band"
  echo "zoom: $zoom"
  echo "uuid: $uuid"
  echo "is_downloaded: $is_downloaded"
  echo "username: $username"
  echo "password: $password"
  echo ""

  python3 file_downloader.py --url "$link" --user "$username" --password "$password" &
  sleep 2 # to avoid query flood
done < <(tail -n +2 $FILENAME)
sleep infinity
