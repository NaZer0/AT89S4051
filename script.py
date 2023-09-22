#mosi - out
#miso - in
# Библиотека для работы с пинами ввода-вывода
from machine import Pin
from array import *
# Библиотека для работы с временем
import time
 
# Светодиод в режим выхода на 25 пине
mosi = Pin(2, Pin.OUT)
miso = Pin(3, Pin.PullDown)
clock = Pin(4, Pin.OUT) 
rst = Pin(5, Pin.OUT)

def SendBit (bit) :

    mosi.value(bit)
    clock.value(True)
    time.msleep(50)
    clock.value(False)

def ReciveBit () :

    temp = 0
    clock.value(True)
    time.msleep(50)
    temp = miso.value()
    clock.value(False)
    return temp

def SendByte (Byte) :

    for b in range(8):
        bit = Byte>>b
        bit = bit & 0x01
        SendBit(bit)

def ReciveByte () :
    Byte = 0
    for b in range(8):
        bit = ReciveBit()
        Byte << 1
        Byte = Byte | bit

    return Byte
    
def ProgramEnable ():
    Byte1 = 0xAC
    Byte2 = 0x53
    Byte3 = 0x00
    Byte4 = 0x00

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)
    SendByte(Byte4)

def ChipErase ():
    Byte1 = 0xAC
    Byte2 = 0x80
    Byte3 = 0x00
    Byte4 = 0x00

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)
    SendByte(Byte4)

 def WriteCodeByte (Address, Byte):
    addr1 = (Address >> 8) & 0x0f
    addr2 = Address & 0xff

    Byte = Byte & 0xff
    
    Byte1 = 0x40
    Byte2 = addr1
    Byte3 = addr2
    Byte4 = Byte

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)
    SendByte(Byte4)   

 def ReadCodeByte (Address):
    addr1 = (Address >> 8) & 0x0f
    addr2 = Address & 0xff
    
    Byte1 = 0x20
    Byte2 = addr1
    Byte3 = addr2

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)

    Byte = ReciveByte()

    return Byte

def WriteCodePage (Address, Data) :
    addr1 = (Address >> 8) & 0x0f
    addr2 = Address & 0xE0

    Byte1 = 0x50
    Byte2 = addr1
    Byte3 = addr2

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)

    for i in range(32) :
        SendByte(Data[i])

def ReadCodePage (Address) :
    addr1 = (Address >> 8) & 0x0f
    addr2 = Address & 0xE0

    Byte1 = 0x30
    Byte2 = addr1
    Byte3 = addr2

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)

    Data = [0] * 32

    for i in range(32) :
        Data[i] = ReciveByte()

    return Data

def ReadAtmelSignatureByte (Address) :
    addr = Address & 0x1F

    Byte1 = 0x28
    Byte2 = 0x00
    Byte3 = addr

    SendByte(Byte1)
    SendByte(Byte2)
    SendByte(Byte3)

    Byte4 = ReciveByte() 

    return Byte4

miso.value(0)
clock.value(0)
rst.value(0)

while (True) :
    rst.on()
    ProgramEnable()
    Bute1 = ReadAtmelSignatureByte(0x00)
    Bute2 = ReadAtmelSignatureByte(0x01)
    Bute3 = ReadAtmelSignatureByte(0x02)

    if ((Bute1 == 0x1E) and (Bute2 == 0x43) and (Bute3 == 0xff)) :
        print("AT89S4051")
    
