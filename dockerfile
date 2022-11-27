FROM python:3.9

WORKDIR /fairy_chess

COPY /fairy_chess /fairy_chess

RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt
