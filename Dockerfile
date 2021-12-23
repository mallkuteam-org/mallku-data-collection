FROM ubuntu:18.04

RUN adduser mallku
WORKDIR /usr/src/app
COPY requirements.txt ./

RUN apt update && apt install python3 python3-pip -y && rm -rf /var/lib/apt/lists/*
RUN python3 -m pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

USER mallku
CMD [ "bash", "main.sh" ]
