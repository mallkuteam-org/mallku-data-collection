#!/bin/bash

FILENAME="utils/links.csv"

while IFS="," read -r link title ingestion processing_level size uuid foo
do
  echo "link: $link "
  echo "title: $title"
  echo "ingestion date: $ingestion"
  echo "processing level: $processing_level"
  echo "size: $size"
  echo "uuid: $uuid"
  echo ""

  python3 file_downloader.py --url "$link" --user vshoijet --password vero3580 >> ${PWD}/logs/${title}.log 2>&1 &
done < <(tail -n +2 $FILENAME)
