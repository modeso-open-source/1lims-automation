FROM selenium/standalone-chrome:latest

USER root
RUN apt-get update && apt-get install -y python3 python3-pip

COPY requirements.txt .
COPY run.sh .
RUN chmod +x run.sh
RUN pip3 install -r requirements.txt
