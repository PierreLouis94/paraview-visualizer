#!/usr/bin/env bash
DATA_DIR=/home/pierre-louis-bonvin/Data
docker run -it --rm -p 8080:80 \
    -v "$DATA_DIR:/data" \
    pv-visualizer
