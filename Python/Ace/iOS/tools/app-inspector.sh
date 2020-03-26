#!/bin/bash
udid=`idevice_id -l`
app-inspector -u $udid --verbose


