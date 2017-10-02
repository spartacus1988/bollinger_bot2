#!/bin/bash
# start_xvfb.sh



/usr/bin/xvfb-run -f /tmp/ubuntu.xvfb.auth -s '-screen 0 700x500x24 -auth /tmp/ubuntu.xvfb.auth' python3 /home/ubuntu/bollinger_bot2/bollinger_bot2.py > /home/ubuntu/bb.log 2>&1 &

