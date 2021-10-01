#!/usr/bin/env python3

from DXHelper import DXHelper
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("-l", "--list", action="store_true", help="List all of the open ports available")
    parser.add_argument("-d", "--dump",  nargs=2, help="Dump the voice data of the synth to a file")
    parser.add_argument("-e", "--export", nargs=2, help="Export the saved voice data to the synth")

    args = parser.parse_args()

    dx_helper = DXHelper()

    if args.list:
        dx_helper.get_available_midi_ports()
    elif args.dump:
        dx_helper.dump(args.dump)
    elif args.export:
        dx_helper.export(args.export)



if __name__ == "__main__":
    main()