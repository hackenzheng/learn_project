#!/usr/bin/env bash
docker build --network=host -f Dockerfile -t metrics:0.1 .
