# -*- coding: utf-8 -*-
"""
@author: CakeTheLiar
"""

from bintools import reader, writer
import sys
import getopt
import os.path
from enum import Enum
    
class __Mode(Enum):
    ENCODE = 1
    DECODE = 2

def main(argv):
    inputfile = ""
    outputfile = ""
    mode: __Mode = None

    try:
        opts, args = getopt.getopt(argv,"hedi:o:",["ifile=","ofile=","encode","decode"]) #help, encode, decode, inputfile, outputfile
    except getopt.GetoptError:
        print("bintoreadable.py [-e/-d] -i <inputfile> -o <outputfile>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print("bintoreadable.py (-e/-d) -i <inputfile> [-o <outputfile>]")
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-e", "--encode"):
            if mode != None:
                print("-e and -d can not be used together")
                sys.exit(2)
            mode = __Mode.ENCODE
        elif opt in ("-d", "--decode"):
            if mode != None:
                print("-e and -d can not be used together")
                sys.exit(2)
            mode = __Mode.DECODE

    if inputfile == "":
        print("no input file was given")
        sys.exit(2)

    if outputfile == "":
        baseName = inputfile[:inputfile.rfind(".")]
        if mode == __Mode.ENCODE:
            outputfile = baseName + ".bin"
        elif mode == __Mode.DECODE:
            outputfile = baseName + ".json"
        else:
            print("no mode was given. use [-e/-d]")
            sys.exit(2)
        print("no output file was given. defaulting to {}".format(outputfile))

    if not os.path.isfile(inputfile):
        print("input file {} was not found".format(outputfile))
        sys.exit(2)

    if mode == __Mode.ENCODE:
        encode(inputfile, outputfile)
    elif mode == __Mode.DECODE:
        decode(inputfile, outputfile)


def encode(inputfile, outputfile):
    print("parsing file {}".format(inputfile))
    content = reader.readJson(inputfile)
    print("finished parsing")
    print("writing to {}".format(outputfile))
    writer.writeBin(outputfile, content)

def decode(inputfile, outputfile):
    print("parsing file {}".format(inputfile))
    content = reader.readBin(inputfile)
    print("finished parsing")
    print("writing to {}".format(outputfile))
    writer.writeJson(outputfile, content)


if __name__ == "__main__":
    main(sys.argv[1:])
