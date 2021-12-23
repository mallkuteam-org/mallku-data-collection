#!/bin/bash

#python3 main.py

FILENAME="utils/links.csv"
COUNTER=0
USER_COUNTER=($(wc -l utils/users.csv | awk '{print $1}'))
USER_COUNTER=$((USER_COUNTER - 1))
USER_COUNTER=$((USER_COUNTER*3))
echo "USERS: $USER_COUNTER"

while IFS="," read -r link band zoom uuid is_downloaded username password
do
  echo "---"
  echo "link: $link "
  echo "band: $band"
  echo "zoom: $zoom"
  echo "uuid: $uuid"
  echo "is_downloaded: $is_downloaded"
  echo "username: $username"
  echo "password: $password"

  python3 file_downloader.py --url "$link" --user "$username" --password "$password" &
  let COUNTER++
  sleep 2 # to avoid query flood

  if [ $COUNTER -gt $USER_COUNTER ]; then
    echo "MAX USER DOWNLOADS REACHED - WAIT TO CONTINUE"
	  wait
	fi
done < <(tail -n +2 $FILENAME)
sleep infinity
