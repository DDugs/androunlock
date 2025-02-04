#!/usr/bin/env python3
__author__ = "Dhruv Gupta"

import binascii
from optparse import OptionParser

def b2s(byte_data):
    return "".join(map(chr, byte_data))

def read_gesture(gesture_file_path):
    try:
        with open(gesture_file_path, "rb") as gesture_file:
            sha1bytes = [binascii.hexlify(gesture_file.read(1)) for _ in range(20)]
        return b2s(sha1bytes)
    except IOError:
        print("[-] Error: Unable to open gesture file. File not found or permission denied.")
        exit(1)

def match_pattern(dictionary_file_path, sha1hash):
    sha1hash = sha1hash.upper()
    
    with open(dictionary_file_path, "r") as dictionary_file:
        for line in dictionary_file:
            if sha1hash in line:
                pattern = line.split(";", 1)[0]
                print(f"[+] Pattern retrieved from gesture.key file: {pattern}")
                return

def parse_arguments():
    parser = OptionParser(
        usage="python3 %prog -g <gesture.key> -d <dictionary file>",
        description="This program is used to recover Android's pattern password."
    )

    parser.add_option("-g", "--gesture", type="string", dest="gesture_file",
                      help="Path to the gesture.key file")
    parser.add_option("-d", "--dictionary", type="string", dest="dictionary_file",
                      help="Path to the dictionary file containing SHA-1 hashes")

    options, _ = parser.parse_args()

    if not options.gesture_file or not options.dictionary_file:
        parser.print_help()
        exit(1)

    return options

def main():
    options = parse_arguments()
    sha1hash = read_gesture(options.gesture_file)
    match_pattern(options.dictionary_file, sha1hash)

if __name__ == "__main__":
    main()