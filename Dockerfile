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
	&& apt-get install --assume-yes --fix-missing \
	python3.10 python3-pip unzip xvfb libxi6 libgconf-2-4 jq libjq1 libonig5 libxkbcommon0 libxss1 libglib2.0-0 libnss3 \ 
	libfontconfig1 libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0 libpango-1.0-0 libgdk-pixbuf2.0-0 libxcomposite1 \
	libxcursor1 libxdamage1 libxtst6 libappindicator3-1 libasound2 libatk1.0-0 libc6 libcairo2 libcups2 libxfixes3 \
	libdbus-1-3 libexpat1 libgcc1 libnspr4 libgbm1 libpangocairo-1.0-0 libstdc++6 libx11-6 libx11-xcb1 libxcb1 libxext6 \
	libxrandr2 libxrender1 gconf-service ca-certificates fonts-liberation libappindicator1 lsb-release xdg-utils\
	&& apt-get autoclean && apt-get clean && apt-get autoremove

RUN pip install requests selenium argparse

COPY . .

RUN python3.10 setup_cft.py

RUN chmod 777 ./webdriver/chromedriver-linux64/chromedriver \
	&& chmod 777 ./webdriver/chrome-headless-shell-linux64/chrome-headless-shell 

CMD python3.10 auto_login.py
