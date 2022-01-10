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
	&& apt-get install wget python3.8 python3-pip --assume-yes \
	&& apt-get install fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcairo2 libcups2 libcurl3-gnutls libdbus-1-3 libdrm2 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libx11-6 libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils --assume-yes \
	&& pip3 install requests selenium \
	&& chmod 777 ./webdriver/chromedriver_linux64 \
	&& wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
	# && apt-get -f -y install \
	&& dpkg -i google-chrome-stable_current_amd64.deb  
CMD python3 auto_login.py