FROM python:3.10
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip install tweepy==4.13 wget==3.2 python-dateutil==2.8.2
WORKDIR /app
CMD rm -rf /app && mkdir /app && cd /app && git clone https://github.com/dxx8200/tweetprj.git . && python ./main.py