#!/bin/sh

mv c.local.properties compiler-explorer/etc/config/
docker build -t karathan/cexplore:staging .
