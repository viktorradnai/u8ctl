#!/usr/bin/python

import sys
import logging
import argparse
import subprocess
from argparse import RawTextHelpFormatter

logger = logging.getLogger(__name__)

# See http://www.2writers.com/eddie/tutsysex.htm for the details of the checksum
# logger.info(roland_checksum(0x401100, 0x4163)) should return 11
def roland_checksum(addr, data):
    bsum = 0

    chars = [ x for x in "{0:06x}{1:02x}".format(addr, data) ]

    while len(chars):
        bsum += int("{1}{0}".format(chars.pop(), chars.pop()), 16)

    checksum = 128 - (bsum % 128)
    logger.debug("roland_checksum(%x, %x) = %x", addr, data, checksum)
    return checksum


def send_sysex(args, port, cmd, addr, data):
    s = ""

    device = 0x10
    model = 0x21
    if cmd == 'set': cmdid = 0x12
    elif cmd == 'get': cmdid = 0x11
    else: raise Exception("Unknown comand: {0}".format(cmd))

    a = [ x for x in "f041{0:02x}{1:04x}{2:02x}{3:06x}{4:02x}{5:02x}f7".format(device, model, cmdid, addr, data, roland_checksum(addr, data)) ]
    logger.debug(a)
    while len(a):
        s += "{1}{0} ".format(a.pop(1), a.pop(0))

    cmdline = "amidi -p '{0}' -S '{1}'".format(port, s)
    print(cmdline)
    if not args.noop: subprocess.call(cmdline, shell=True)


def auto_int(x):
    return int(x, 0)


def parse_cmdline():

    parser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter, description='''
    Sends System Exclusive (sysex) messages for a Roland U-8 audio interface in the form of:
        41h 10h 00h 21h 12h 21h 02h 21h 27h 1fh 17h

Known device addresses and functions:

    The first two bytes are 0x2102, the last byte is as follows:

        Last Byte   Type    Function
        0x03        int     Mic/gtr/inst volume
        0x04        int     Mic/gtr/inst pan (0: mic, 127: gtr, 63: both)
        0x07        bool    Mic/gtr/inst mute
        0x21        int     Aux/digital volume
        0x22        int     Aux/digital pan
        0x25        bool    Aux/digital mute
        0x28        int     Wave out 1 (master) vol
        0x29        int     Wave out 1 (master) pan
        0x2a        bool    Wave out 1 (master) mute
        0x2b        int     Wave out 2 (effect) volume
        0x2c        int     Wave out 2 (effect) pan
        0x2d        bool    Wave out 2 (effect) mute
        0x3c        int     Master volume
        0x3d        bool    Master mute

    Each address can take a value between 0 and 127 (or 0x7f in hexadecimal),
    but for "bool" addresses only care if the value is 0 or non-zero.
    ''',
    epilog="Note: You may use the `amidi -l` command to determine the port for the -p option, the correct port is called \"U-8 Control\"."
    )
    parser.add_argument('-v', '--verbose', action='store_true', help="Enable verbose output")
    parser.add_argument('-q', '--quiet', action='store_true', help="Output errors only")
    parser.add_argument('-n', '--noop', action='store_true', help="Dry run, only print command")
    parser.add_argument('-p', '--port', help="Alsa Midi port to send data to")
    parser.add_argument('-b', '--base-address', type=auto_int, default=0x210200, help="Base address (first four digits of the address) to write to")
    parser.add_argument('command', help="Command, either 'set' or 'get'", choices=[ 'get', 'set'])
    parser.add_argument('address', type=auto_int, help="Address to write to")
    parser.add_argument('value', type=auto_int, help="Value to write ")

    args = parser.parse_args()

    if args.verbose: loglevel = logging.DEBUG
    elif args.quiet: loglevel = logging.ERROR
    else:            loglevel = logging.INFO

    logging.basicConfig(level=loglevel, format='%(asctime)s %(levelname)s %(message)s')

    return args


def main():
    args = parse_cmdline()
    send_sysex(args, args.port, args.command, args.base_address + args.address, args.value)
    sys.exit(0)


# call main()
if __name__ == '__main__':
    main()
