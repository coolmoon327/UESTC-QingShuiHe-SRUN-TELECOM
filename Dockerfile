FROM ubuntu:jammy
LABEL author="coolmoon327"
LABEL version="5.0"
LABEL description="电子科技大学寝室电信网络自动登录"
WORKDIR /home
ENV TZ Asia/Shanghai
ENV SRUN_USERNAME your_username
ENV SRUN_PASSWORD your_password
ENV SRUN_METHOD=request
ENV EXTRA_ARGS=
ARG DEBIAN_FRONTEND=noninteractive

COPY . .

RUN apt-get update \
	&& apt-get install --assume-yes --fix-missing python3.10 python3-pip \
	&& apt-get install --assume-yes --fix-missing $(cat cft_dep) \
	&& apt-get autoclean && apt-get clean && apt-get autoremove

RUN pip install requests selenium

RUN python3.10 uestc_telecom/cli.py -u

CMD python3.10 uestc_telecom/cli.py --method $SRUN_METHOD --userid $SRUN_USERNAME --password $SRUN_PASSWORD $EXTRA_ARGS
