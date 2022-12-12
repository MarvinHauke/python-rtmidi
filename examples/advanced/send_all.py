#!/usr/bin/env python3
"""Send all notes and CCs with all possible values an all 16 channels."""

import argparse
import logging
import sys
import time

from rtmidi.midiutil import open_midioutput
from rtmidi.midiconstants import *


log = logging.getLogger("midi-send-all")

argp = argparse.ArgumentParser()
argp.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
argp.add_argument("-d", "--delay", type=float, default=0.05, help="Delay between messages")
argp.add_argument("-V", "--velocity", type=int, default=127, help="Note on velocity")
argp.add_argument("-o", "--off-velocity", type=int, default=64, help="Note off velocity")
argp.add_argument("port", nargs="?", help="MIDI output port")

args = argp.parse_args()

logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO)

midiout, name = open_midioutput()

for chan in range(16):
    for note in range(128):
        log.debug(f"Sending NOTE ON, ch={chan+1}, note={note}, vel={args.velocity}.")
        midiout.send_message([NOTE_ON | chan, note, args.velocity])
        time.sleep(args.delay)
        log.debug(f"Sending NOTE OFF, ch={chan+1}, note={note}, vel={args.off_velocity}.")
        midiout.send_message([NOTE_OFF | chan, note, args.off_velocity])
        time.sleep(args.delay)

for chan in range(16):
    for cc in range(128):
        for val in range(128):
            log.debug(f"Sending CONTROL_CHANGE, ch={chan+1}, cc={cc}, val={val}.")
            midiout.send_message([CONTROL_CHANGE | chan, cc, val])
            time.sleep(args.delay)

log.debug("Done.")
