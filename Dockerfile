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

FROM slim as full

ENV SRUN_METHOD=browser

RUN apk info --depends google-chrome | \
	apk add && \
	pip install selenium && \
	python /src/cli.py -u 

CMD python /src/cli.py --method $SRUN_METHOD --userid $SRUN_USERNAME --password $SRUN_PASSWORD $EXTRA_ARGS