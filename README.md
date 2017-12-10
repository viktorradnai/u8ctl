# u8ctl - Tools to Control a Roland ED U-8


## Usage

This is a work in progress. See `u8ctl.py -h` for usage instructions.

Examples:

`./u8ctl.py  -d hw:2,0,1 set 0x3c 127`

This sets the master volume to maximum.

`./u8ctl.py  -d hw:2,0,1 set 0x2d 1`

This mutes the 'effect' channel (reverb). Note that 1 = mute on, 0 = mute off.

`./u8ctl.py  -d hw:2,0,1 set 0x29 63`

This pans the computer audio to the center. Note that 0 = left, 63 = center, 127 = right.


## Requirements

Linux and ALSA are required. `u8ctl.py` sends MIDI messages using the `amidi` command, which is part of ALSA.

Currently the snd-usb-audio kernel module needs to be patched with the included `u8-audio-for-linux-4.11.patch` and recompiled to enable sound from the U-8.

