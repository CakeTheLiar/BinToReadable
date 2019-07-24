import ctypes
import struct
import json

def readInt(file) -> ctypes.c_int32:
    return struct.Struct("i").unpack_from(file.read(4))[0]

def readUlong(file) -> ctypes.c_ulong:
    return struct.Struct("Q").unpack_from(file.read(8))[0]

def readBool(file) -> bool:
    return struct.Struct("?").unpack_from(file.read(1))[0]

def readByte(file) -> int:
    return ord(struct.Struct("c").unpack_from(file.read(1))[0])

def readShort(file) -> ctypes.c_short:
    return struct.Struct("h").unpack_from(file.read(2))[0]

def readChar(file) -> chr:
    return chr(ord(struct.Struct("c").unpack_from(file.read(1))[0]))

def readLEB128(file):
    result = 0
    shift = 0
    while True:
        byte = readByte(file)
        mask = int(1 << 7)
        result |= (byte & ~mask) << shift
        if(byte & mask != mask):
            break
        shift += 7
    return result
        

def readString(file):
    length = readLEB128(file)
    s = []
    for i in range(length):
            s.append(readChar(file))  
    return "".join(s)

def parseType(file) -> dict:
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

def parseFunc(file) -> dict:
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

def readBin(path) -> dict:

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

def readJson(path) -> dict:
    with open(path, "r") as file:
         content = json.load(file)

    return content
