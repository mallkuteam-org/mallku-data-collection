#!/bin/bash

python main.py

FILENAME="utils/links.csv"

while IFS="," read -r link title ingestion processing_level size uuid downloaded username password
do
  echo "link: $link "
  echo "title: $title"
  echo "ingestion date: $ingestion"
  echo "processing level: $processing_level"
  echo "size: $size"
  echo "uuid: $uuid"
  echo "downloaded: $downloaded"
  echo "username: $username"
  echo "password: $password"
  echo ""

  python3 file_downloader.py --url "$link" --user "$username" --password "$password" >> ${PWD}/logs/${title}.log 2>&1 &
done < <(tail -n +2 $FILENAME)
