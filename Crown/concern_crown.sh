#!/bin/bash

scp -r ./service/* root@192.168.31.2:Crown/

ssh root@192.168.31.2 -t " echo '' && date && echo '' && \
    \
    cd /root/Crown/ ; bash connect.sh && sleep 3 && see2 "
