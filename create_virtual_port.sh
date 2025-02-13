#!/bin/bash
set -euo pipefail

socat PTY,link=/tmp/vcomport0,raw,echo=0 PTY,link=/tmp/vcomport1,raw,echo=0 &

echo "Success: Created Virtual Port at /tmp/vcomport1"

while true; do
    temp=$(echo "scale=2; $RANDOM/32768 * 100" | bc)
    weight=$(echo "scale=2; $RANDOM/32768 * 100" | bc)
    echo "<temp>: $temp, <weight>: $weight," > /tmp/vcomport0
    sleep 1
done