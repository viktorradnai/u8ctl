# u8ctl - Utility to Control a Roland ED U-8

The Roland Edirol U-8 USB Digital Studio is an USB 1.1 audio and MIDI interface with a built in effect unit, that can also be used as a standalone digital mixer and a MIDI control surface.
It was sold around 1998-2000 and the only full-featured device driver for it is for the Windows 98 operating system.

*If you have the original driver CD that came with the U-8, please get in touch with me. It would be hugely helpful for mapping out the workings of the unit.*

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

