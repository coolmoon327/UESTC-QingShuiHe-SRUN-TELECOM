FROM ubuntu
LABEL author="coolmoon327"
LABEL version="4.3"
LABEL description="用于在电子科技大学清水河校区实现寝室电信宽带网络的全自动接入"
WORKDIR /home
ENV TIME_ZONE Asia/Shanghai
ENV SRUN_USERNAME your_username
ENV SRUN_PASSWORD your_password
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
	&& apt-get -f -y install \
	&& apt-get install wget python3.8 python3-pip libssl-dev --assume-yes --fix-missing\
	&& apt-get install fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libcurl3-gnutls libdbus-1-3 libdrm2 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils --assume-yes --fix-missing

RUN pip3 install requests selenium 

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb --no-check-certificate \
	&& dpkg -i google-chrome-stable_current_amd64.deb \
	&& rm -rf google-chrome-stable_current_amd64.deb

RUN apt-get autoclean && apt-get clean && apt-get autoremove

COPY . .

RUN chmod 777 ./webdriver/chromedriver_linux64 \
	&& rm -rf ./webdriver/chromedriver.exe \
	&& rm -rf ./webdriver/chromedriver_mac64 \
	&& rm -rf ./webdriver/chromedriver_mac64_m1

CMD python3 auto_login.py