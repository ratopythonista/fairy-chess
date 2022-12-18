FROM python:3.9

WORKDIR /fairy_chess

COPY . /fairy_chess

RUN pip install -e . --no-cache-dir --upgrade
