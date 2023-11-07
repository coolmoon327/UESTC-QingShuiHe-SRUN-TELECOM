FROM ubuntu:jammy
LABEL author="coolmoon327"
LABEL version="4.4"
LABEL description="用于在电子科技大学清水河校区实现寝室电信宽带网络的全自动接入"
WORKDIR /home
ENV TZ Asia/Shanghai
ENV SRUN_USERNAME your_username
ENV SRUN_PASSWORD your_password
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
	&& apt-get -f -y install \
	&& apt-get install python3.10 python3-pip --assume-yes --fix-missing 

RUN pip install requests selenium argparse

RUN apt-get autoclean && apt-get clean && apt-get autoremove

COPY . .

RUN python3.10 setup_cft.py

RUN chmod 777 ./webdriver/chromedriver-linux64/chromedriver \
	&& chmod 777 ./webdriver/chrome-headless-shell-linux64/chrome-headless-shell 

CMD python3.10 auto_login.py
