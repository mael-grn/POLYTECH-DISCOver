#!/bin/bash

LOG_FILE=flutter_verbose.log

flutter run \
  -d web-server \
  --web-port 8080 \
  --verbose \
  2>&1 | tee "$LOG_FILE"
