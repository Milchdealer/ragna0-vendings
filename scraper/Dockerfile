FROM python:3-slim

ENV RAGNA0_SQLITE_PATH="/data/ragna0.db"

RUN mkdir /ragna0 \
	&& mkdir /data \
	&& useradd ragna0 --home-dir /ragna0 \
	&& chown ragna0 /ragna0 -R \
	&& chown ragna0 /data -R

USER ragna0
WORKDIR /ragna0

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src .

CMD python3 main.py
