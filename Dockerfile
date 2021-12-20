FROM ubuntu:18.04

WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt update
RUN apt install python3 python3-pip -y
RUN python3 -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "bash", "main.sh" ]
