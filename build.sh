#!/bin/sh

cp c.local.properties c++.local.properties compiler-explorer/etc/config/
docker build -t karathan/cexplore:latest .
