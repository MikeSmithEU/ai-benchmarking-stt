FROM python:3.7-alpine

RUN adduser -D conferatur
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base && pip install --upgrade pip

WORKDIR /home/conferatur
COPY . /home/conferatur/
RUN chmod +x start_gunicorn.sh

RUN pip install '.[api]'

RUN chown -R conferatur:conferatur ./
USER conferatur

EXPOSE 5000
ENTRYPOINT ["./start_gunicorn.sh"]