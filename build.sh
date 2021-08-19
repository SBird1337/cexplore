#!/bin/sh

rsync -u c.local.properties compiler-explorer/etc/config/
docker build -t karathan/cexplore:latest .
