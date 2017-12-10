#!/bin/bash

DEVICE_NUMBER=$1

# The control chip seems to hang up after a while unless this is set.
# Symptom is that there is sound but nothing can be changed. If button 1 was flashing, it freezes as well.
amixer -c2 set 'MIDI Input Mode' 'High Load'

# Master volume to maximum
./u8ctl.py set 0x3c 127 -p hw:$DEVICE_NUMBER,0,1

# Input volumes set to a sensible level
./u8ctl.py set 0x03 100 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x21 100 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x28 100 -p hw:$DEVICE_NUMBER,0,1
# Effect channel set to 50% volume
./u8ctl.py set 0x2b 64 -p hw:$DEVICE_NUMBER,0,1

# Pan controls centered
./u8ctl.py set 0x04 63 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x22 63 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x29 63 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x2c 63 -p hw:$DEVICE_NUMBER,0,1

# Unmute everything except effect channel
./u8ctl.py set 0x07 0 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x25 0 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x2a 0 -p hw:$DEVICE_NUMBER,0,1
./u8ctl.py set 0x2d 1 -p hw:$DEVICE_NUMBER,0,1
