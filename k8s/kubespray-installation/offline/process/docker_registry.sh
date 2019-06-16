#!/usr/bin/env bash
docker run -d \
    -p 5000:5000 \
    --restart=always \
    --name my-registry \
    -v path/to/registry:/var/lib/registry \
    registry:latest
