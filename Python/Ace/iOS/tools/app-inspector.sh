#!/bin/bash
udid=`idevice_id -l`
if [ -z "$udid" ]
then
    echo "Please plug iphone"
    exit 1
else
    echo $udid
fi
app-inspector -u $udid --verbose


