FROM python:3.8
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y git
RUN pip install tweepy==3.10 wget==3.2 python-dateutil==2.8.2
WORKDIR /app
CMD git clone https://github.com/dxx8200/tweetprj.git . && python ./main.py