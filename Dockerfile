FROM python:3.11-alpine as slim

LABEL author="coolmoon327"
LABEL version="5.0"
LABEL description="电子科技大学寝室电信网络自动登录"

WORKDIR /src
ENV TZ Asia/Shanghai
ENV SRUN_USERNAME your_username
ENV SRUN_PASSWORD your_password
ENV SRUN_METHOD=request
ENV EXTRA_ARGS=

ADD ["uestc_telecom/", "cft_dep", "/src/" ]

RUN pip install requests

CMD python /src/cli.py --method $SRUN_METHOD --userid $SRUN_USERNAME --password $SRUN_PASSWORD $EXTRA_ARGS

FROM python:3.11-bookworm as full

LABEL author="coolmoon327"
LABEL version="5.0"
LABEL description="电子科技大学寝室电信网络自动登录"

WORKDIR /src
ENV TZ Asia/Shanghai
ENV SRUN_USERNAME your_username
ENV SRUN_PASSWORD your_password
ENV SRUN_METHOD=browser
ENV EXTRA_ARGS=

ADD ["uestc_telecom/", "cft_dep", "/src/" ]

SHELL ["/bin/bash", "-c"]

RUN pip install requests

RUN curl -fSsL https://dl.google.com/linux/linux_signing_key.pub | \
	gpg --dearmor | \
	tee /usr/share/keyrings/google-chrome.gpg >> /dev/null && \
	echo deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main | \
	tee /etc/apt/sources.list.d/google-chrome.list && \
	apt update

RUN apt-cache depends google-chrome-stable | apt-get install --assume-yes --fix-missing && \
	pip install selenium && \
	python /src/cli.py -u 

CMD python /src/cli.py --method $SRUN_METHOD --userid $SRUN_USERNAME --password $SRUN_PASSWORD $EXTRA_ARGS