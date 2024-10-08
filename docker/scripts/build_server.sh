#!/usr/bin/env bash
CURRENT_DIR=`dirname "$0"`

cd $CURRENT_DIR/..
DEPLOY_DIR="$PWD"
cd ..
ROOT_DIR="$PWD"

docker run --rm          \
    -e TRAME_CLIENT_TYPE=vue2 \
    -v "$DEPLOY_DIR:/deploy" \
    -v "$ROOT_DIR:/local-app"  \
    kitware/trame:py3.10-glvnd build
