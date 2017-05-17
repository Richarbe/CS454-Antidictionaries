import MFW

def main():
    #inputstring = ASCII_toBinStr("All the parks are full of flamingos and booze drums cranberry candycanes")
    inputstring = '101010100010101111010101'
    fw = MFW.MFW(inputstring)
    #length, compressed = encode(fw, inputstring)
    #binoutput = decode(fw, length, compressed)
    #print(binoutput)

    ba = binStrMFWto_ByteArray(inputstring, fw)
    newstring, newfw = binStrMFWfrom_ByteArray(ba)
    print(newstring)
    a = binStrTo_ByteArray('10100100100100100011111010110101')
    b = binStrFrom_ByteArray(a)


def encode(mfw, string):
    s = ''
    compressed = ''

    for w in string:

        notInAD = not mfw.isInAntiDict(s)

        s += w

        if notInAD:
            compressed += w

    return (len(string), compressed)


def decode(mfw, length, compressed):
    s = ''
    i = 0

    while len(s) < length:

        inAD = isInAntiDictLookAhead(mfw, s)

        if inAD[0]:
            s += inAD[1]
        else:
            s += compressed[i]
            i += 1

    return s

def isInAntiDictLookAhead(mfw, word):
    if len(word) >= 1:
        suf = word
    else:
        return (False, '')

    while len(suf) >= 1:
        if (mfw.isInAntiDict(suf + '0')):
            return (True, '1')
        elif (mfw.isInAntiDict(suf + '1')):
            return (True, '0')
        else:
            suf = suf[1:]

    return (False, '')


def ASCII_toBinStr(string):
    return bin(int.from_bytes(string.encode(), 'big'))[2:]


def binStrTo_ASCII(binString):
    n = int('0b' + binString, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def binStrTo_ByteArray(string):
    return int(string, 2).to_bytes((len(string)+7) // 8, 'big')

def binStrFrom_ByteArray(ByteArray):
    return bin(int.from_bytes(ByteArray, 'big'))[2:]

def binStrMFWto_ByteArray(binString, mfw):
    messagebytes = binStrTo_ByteArray(binString)
    dictionarybytes = mfw.encodeAsByteArray()
    output = bytearray()
    output.extend(len(messagebytes).to_bytes(4, byteorder='big'))
    output.extend(messagebytes)
    output.extend(dictionarybytes)
    return output

def binStrMFWfrom_ByteArray(ByteArray):
    len_message = int.from_bytes(ByteArray[0:4], byteorder='big')
    binStr = binStrFrom_ByteArray(ByteArray[4:len_message+4])
    mfw = MFW.MFW(ByteArray[len_message+4:])
    return binStr, mfw

if __name__ == "__main__":
    main()