import MFW
import FactorDAWG as FD
import slowCompressor as SC


def main():

    inputstring = input("Welcome! Please enter in an input string in binary: ")
    if not isBinStr(inputstring):
        print("That was not a binary string. Goodbye.")
        return
    #inputstring = "110110"
    sc = SC.slowCompressor()

    fw = MFW.MFW(inputstring)
    fw.isInAntiDict('010101')
    #print(fw.MFWA)
    fd = FD.FactorDAWG(inputstring)

    #print(fd.delta)

    #Main Menu
    while True:
        menu_input = input("\nMenu options:\nA: print compressed string\nB: print MFW and factorDAWG\nC: Test if a string is accepted by the MFW\nPlease enter one of the above options(A, B, C, or 'exit' to exit): \n")

        if (menu_input.capitalize() == "A"):
            print(sc.testAndPrint(inputstring))
        elif (menu_input.capitalize() == "B"):
            print("Each pair represents a state. First number in each pair is the next state on input 0, second number is next state on input 1. -1 means there is no edge for this input.\nMFW : ", fw.MFWA, "\nfactorDAWG : ", fd.delta)
        elif (menu_input.capitalize() == "C"):
            while True:
                tempinput = input("Enter a binary string to test (any nonbinary to exit to menu): ")
                if isBinStr(tempinput):
                    print(fw.isInMFW(tempinput))
                else:
                    break
        elif (menu_input == "exit"):
            print("Goodbye!")
            break
        else:
            print("Invalid input, please try again")

    #inputstring = ASCII_toBinStr("All the parks are full of flamingos and booze drums cranberry candycanes")
    #inputstring = '1000101010011'



    #fw.createTransducer()
    ##length, compressed = encode(fw, inputstring)
    ##binoutput = decode(fw, length, compressed)
    ##print(binoutput)

    #ba = binStrMFWto_ByteArray(inputstring, fw)
    #newstring, newfw = binStrMFWfrom_ByteArray(ba)
    ##print(newstring)
    #a = binStrTo_ByteArray('10100100100100100011111010110101')
    #b = binStrFrom_ByteArray(a)

def isBinStr(string):
    if string == '':
        return False
    for i in string:
        if not (i == '0' or i == '1'):
            return False
    return True

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
        if (mfw.isInMFW(suf + '0')):
            return (True, '1')
        elif (mfw.isInMFW(suf + '1')):
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