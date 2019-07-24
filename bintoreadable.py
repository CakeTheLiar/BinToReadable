<<<<<<< Updated upstream
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 20:51:12 2017

@author: CakeTheLiar
"""
import struct
import json
    
def readInt(file):
    return struct.Struct("i").unpack_from(file.read(4))[0]

def readUlong(file):
    return struct.Struct("Q").unpack_from(file.read(8))[0]

def readBool(file):
    return struct.Struct("?").unpack_from(file.read(1))[0]

def readChar(file):
    return struct.Struct("c").unpack_from(file.read(1))[0]

def readShort(file):
    return struct.Struct("h").unpack_from(file.read(2))[0]

def readLEB128(file):
    result = 0
    shift = 0
    while True:
        byte = readChar(file)
        byte_cpy = ord(byte)
        mask = int(1 << 7)
        result |= (byte_cpy & ~mask) << shift
        if(byte_cpy & mask != mask):
            break
        shift += 7
    return result
        

def readString(file):
    length = readLEB128(file)
    s = []
    for i in range(length):
          s.append(readChar(file))  
    return "".join(chr(ord(x)) for x in s)


    

def parseType(file):
    t = dict()
    t["StreamVersion"] = readInt(file)
    t["VTable"] = readUlong(file)
    t["Name"] = readString(file)
    if readBool(file):
        t["Size"] = readInt(file)
    else:
        t["Size"] = 0
    t["RTTI"] = readUlong(file)
    
    return t

def parseFunc(file):
    f = dict()
    f["StreamVersion"] = readInt(file)
    f["Begin"] = readUlong(file)
    f["End"] = readUlong(file)
    if readBool(file):
        f["ShortName"] = readString(file)
    else:
        f["ShortName"] = ""
    if readBool(file):
        f["FullName"] = readString(file)
    else:
        f["FullName"] = ""
    f["Id"] = readUlong(file)
    
    return f

def readBin(path):
    with open(path, "rb") as file:
        streamVersion = readInt(file)
        fileVersion = struct.Struct("iiii").unpack_from(file.read(4*4))
        typesCount = readInt(file)
        
        types = []
        for i in range(typesCount):
            types.append(parseType(file))
        
        funcCount = readInt(file)
        
        funcs = []
        for i in range(funcCount):
            funcs.append(parseFunc(file))
        
    return { "StreamVersion": streamVersion, 
             "FileVersion": fileVersion, 
             "TypesCount": typesCount,
             "Types": types,
             "FunctionsCount": funcCount,
             "Functions": funcs
         }
        
def writeJson(path, content):
    with open(path, "w") as file:
        file.truncate()
        json.dump(content, file, indent=4)
    
    
if __name__ == "__main__":
    filename = "NetScriptFramework.SkyrimSE"
    content = readBin(filename + ".bin")
    writeJson(filename + ".json", content)
        

=======

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
>>>>>>> Stashed changes
