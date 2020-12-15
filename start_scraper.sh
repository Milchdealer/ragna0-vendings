#!/usr/bin/env bash

DATA_FOLDER=`pwd`/data

docker run --rm -v $DATA_FOLDER:/data ragna0
