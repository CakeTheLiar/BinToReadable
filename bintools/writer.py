import ctypes
import struct
import json

def writeInt(file, val: ctypes.c_int):
    file.write(struct.pack('i', val))

def writeUlong(file, val: ctypes.c_ulong):
    file.write(struct.pack('Q', val))

def writeBool(file, val: bool):
    file.write(struct.pack('?', val))

def writeByte(file, val: ctypes.c_ubyte):
    file.write(struct.pack('c', val))

def writeShort(file, val: ctypes.c_short):
    file.write(struct.pack('h', val))

def writeChar(file, val: ctypes.c_char):
    file.write(struct.pack('c', bytes(val)))

def writeLEB128(file, length: int):
    while True:
        byte = length & 0x7F
        length >>= 7
        if length != 0:
            byte |= 0x80
        writeChar(file, ctypes.c_char(byte))

        if length == 0:
            return

def writeString(file, text: str):
    length = len(text)
    writeLEB128(file, length)
    file.write(text.encode())


def writeType(file, val: dict):
    writeInt(file, val["StreamVersion"])
    writeUlong(file, val["VTable"])
    writeString(file, val["Name"])
    if val["Size"] != 0:
        writeBool(file, True)
        writeInt(file, val["Size"])
    else:
        writeBool(file, False)
    writeUlong(file, val["RTTI"])


def writeFunc(file, val: dict):
    writeInt(file, val["StreamVersion"])
    writeUlong(file, val["Begin"])
    writeUlong(file, val["End"])
    if val["ShortName"] != "":
        writeBool(file, True)
        writeString(file, val["ShortName"])
    else:
        writeBool(file, False)
    if val["FullName"] != "":
        writeBool(file, True)
        writeString(file, val["FullName"])
    else:
        writeBool(file, False)
    writeUlong(file, val["Id"])


def writeBin(path, val: dict):
    with open(path, "wb") as file:
        writeInt(file, val["StreamVersion"])
        for v in val["FileVersion"]:
            writeInt(file, v)
        writeInt(file, val["TypesCount"])
        for t in val["Types"]:
            writeType(file, t)
        writeInt(file, val["FunctionsCount"])
        for v in val["Functions"]:
            writeFunc(file, v)

def writeJson(path, content: dict):
    with open(path, "w") as file:
        file.truncate()
        json.dump(content, file, indent=4)