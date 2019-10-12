
# This image provides aws cli tools
# This is usefull for creating k8s cron jobs for managing AWS
FROM alpine:latest

LABEL "com.Acme.security.utils.aws-cli"="security@example.com"
LABEL "MAINTAINER"="Infrastructure Security <security@example.com>"

WORKDIR /app

# get the essentials
RUN apk add --update \
    ca-certificates \
    bash  \
    python \
    python-dev \
    py-pip

# get latest pip
RUN pip install --upgrade pip

# clean up
RUN rm -rf /var/cache/apk/*

# make some required directories
RUN mkdir -p /var/run/aws
RUN mkdir -p /root/.aws

# install our app
COPY ./scripts.d /app
ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

CMD [ "python", "/app/handler.py" ]

