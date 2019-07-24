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
        

