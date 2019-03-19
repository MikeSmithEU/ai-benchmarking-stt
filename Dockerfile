FROM python:3.7-alpine

RUN adduser -D benchmarkstt
RUN apk --update add python py-pip openssl ca-certificates py-openssl wget
RUN apk --update add --virtual build-dependencies libffi-dev openssl-dev python-dev py-pip build-base
RUN pip install --upgrade pip

WORKDIR /home/benchmarkstt
COPY . /home/benchmarkstt/

RUN pip install '.[test]'

RUN chown -R benchmarkstt:benchmarkstt ./
USER benchmarkstt

EXPOSE 8080
ENTRYPOINT ["gunicorn", "-b", ":8080", "--access-logfile", "-", "--error-logfile", "-", "benchmarkstt.api.gunicorn"]
