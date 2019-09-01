#!/bin/sh
docker container stop cexplore || true && docker container rm cexplore || true
docker container run -d --name "cexplore" --restart=always -it -p 10240:10240 karathan/cexplore:latest