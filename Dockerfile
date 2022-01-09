FROM ubuntu
LABEL author="coolmoon"
LABEL version="2.0"
LABEL description="用于在电子科技大学清水河校区实现寝室电信宽带网络的全自动接入"
WORKDIR /home
ENV TIME_ZONE Asia/Shanghai
ENV SRUN_USERNAME your_username
ENV SRUN_PASSWORD your_password
ARG DEBIAN_FRONTEND=noninteractive
COPY . .
RUN apt-get update \
	&& apt-get upgrade \
	&& apt-get install wget python3.8 python3-pip \
	&& pip3 install requests selenium \
	&& chmod 777 ./webdriver/chromedriver_linux64 \
	&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	&& dpkg -i google-chrome-stable_current_amd64.deb  \
	&& python3 auto_login.py