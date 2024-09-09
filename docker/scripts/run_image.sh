#!/usr/bin/env bash
DATA_DIR=/home/pierre/Data
docker run -it --rm -p 8080:80 \
    -v "$DATA_DIR:/data" \
    -d \
    pv-visualizer
