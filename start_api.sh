#!/usr/bin/env bash

DATA_FOLDER=`pwd`/data

docker run -d -v $DATA_FOLDER:/data:ro --restart=on-failure -p 10080:80 ragna0-vending-api