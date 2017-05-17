import itertools
import time

class slowCompressor:

    def __init__(self):
        self.AD = []
        self.MAX_WORD_LENGTH = 16
        self.MAX_MESSAGE_LENGTH = 1000

        
    def __binseq(self,k):
        return [''.join(x) for x in itertools.product('01', repeat=k)]


    def ASCII_toBinStr(self,string):

        return bin(int.from_bytes(string.encode(), 'big'))[2:]

    def binStrTo_ASCII(self,binString):
        
        n = int('0b'+binString, 2)
        return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

    def __iterate(self,length):
        
        arr = []
        i = 0
        while i < length:
            i += 1
            arr += self.__binseq(i)
            
        return arr

    def __buildAD_super_slow(self,string):
        self.AD = []
        
        iterations = self.__iterate(self.MAX_WORD_LENGTH)
        
        for i in iterations:
            
            isIn = False
            
            for w in self.AD:
                if w in i:
                    isIn = True
                    break
            
            if not isIn:
                if i not in string:
                    self.AD.append(i)
        
    def __isInAntiDict(self,antiDict,word):
        
        if len(word) >= 1:
            suf = word
        else:
            return (False,'')

        for w in antiDict:
            
            s = suf
            
            while len(s) >= 1:
                
                if w == (s + '0'):
                    return (True,'1')
                elif w == (s + '1'):
                    return (True, '0')
                else:
                    s = s[1:]
        
        return (False,'')
        
    def __encodeBits(self,bitString):

        final = ''
        
        for b in bitString:
            if b == '1':
                final += '10'
            else:
                final += '0'
                
        return final
        
    def __decodeBits(self,bitString):
        
        final = ''
        bs = bitString
        
        while len(bs) > 0:
            if bs[0] == '1':
                final += '1'
                bs = bs[2:]
            else:
                final += '0'
                bs = bs[1:]
                
        return final
        
    def __encodeAntiDict(self,antiDict):
        
        if len(antiDict) <= 0:
            return ''
        
        final = ''
        
        for w in antiDict:
            final += self.__encodeBits(w) + '11'
        
        return final[:-2]

    def __decodeAntiDict(self,bitStringArray):
        
        AD = []
        for w in bitStringArray:
            AD.append(self.__decodeBits(w))
            
        return AD
        
    def __encode(self,antiDict,string):
      s = ''
      compressed = ''
      
      for w in string:
        
        notInAD = not self.__isInAntiDict(antiDict,s)[0]
        
        s += w
        
        if notInAD:
            compressed += w
        
      return (len(string),compressed)

    def __decode(self,antiDict,length,compressed):
        s = ''
        i = 0
        
        while len(s) < length:
            
            inAD = self.__isInAntiDict(antiDict,s)
            
            if inAD[0]:
                s += inAD[1]
            else:
                s += compressed[i]
                i += 1
                
        return s

    def __fullEncode(self,string):
        self.__buildAD_super_slow(string)
        eAD = self.__encodeAntiDict(self.AD)
        
        e = self.__encode(self.AD,string)
        
        l = bin(e[0])[2:]
        el = self.__encodeBits(l)
        
        return el + '11' + eAD + '1111' + e[1]

    def __fullDecode(self,compressed):
        
        data = compressed.split('1111',1)
        header = data[0].split('11')
        n = int(self.__decodeBits(header[0]),2)
        AD = self.__decodeAntiDict(header[1:])
        s = data[1]
        
        return self.__decode(AD,n,s)

    def performTest(self,string):
        
        s = string
        t = time.time()
        
        b = self.ASCII_toBinStr(s)
        
        e = self.__fullEncode(b)
        
        d = self.__fullDecode(e)
        
        m = self.binStrTo_ASCII(d)

        good = b == d
        
        v = len(b)/len(e)
        
        return ('Successful: ' + str(good),'Original length: ' + str(len(b)),'Compressed length: ' + str(len(e)),'Compression value: ' + str(v), 'Time elapsed: ' + str(time.time() - t))
        
    def performTestFull(self,string):
        s = string
        t = time.time() #Mark start time of encode
        
        b = self.ASCII_toBinStr(s) #Convert string into binary string
        lenB = len(b)
        
        if lenB > self.MAX_MESSAGE_LENGTH:
            r = 'n'
            r = input('Performing the full compression and decompression test cycle for this string will take VERY long. Continue? (y/n): ')
            if r == 'y':
                print('Performing test, please wait...')
            else:
                return('Test','Aborted')
            
        self.__buildAD_super_slow(b) #Build anti-dictionary from binary string
        eAD = self.__encodeAntiDict(self.AD) #Encode anti-dictionary into binary string
        
        e = self.__encode(self.AD,b) #Encode message using anti-dictionary on binary message
        
        l = bin(e[0])[2:] #Get the length of binary message (as binary value)
        el = self.__encodeBits(l) #Encode binary value
        
        #Final result is  length + anti-dictionary + compressed message all encoded into bit string
        full_e = el + '11' + eAD + '1111' + e[1]
        
        stop = time.time() - t #Stop timer to get elapsed time
        eTime = str(time.time() - t)
        
        t = time.time() #Mark start time of decode
        
        d = self.__decode(self.AD,lenB,e[1])
        
        dTime = str(time.time() - t)
        
        v = len(b)/len(full_e) #Calculate compression ratio (original/compressed)
        v2 = len(b)/len(e[1])
        
        m = self.binStrTo_ASCII(d)
        
        return ('String used:\n' + string,'Original length (of binary string): ' + str(lenB),'Compressed binary string: ' + e[1],'Compressed length: ' + str(len(e[1])),'Anti-dict length: ' + str(len(eAD)),'Total encoded length (with AD): ' + str(len(full_e)),'Compression value WITHOUT AD: ' + str(v2), 'Compression value WITH AD: ' + str(v), 'Compression time: ' + eTime, 'Decoded string result:\n' + m, 'Decoded bits match original bits: ' + str(b == d), 'Decompress time: ' + dTime)
        
    def printTestResults(self,results):
        
        for r in results:
            print(r)
            
    def testAndPrint(self,string):
        r = self.performTestFull(string)
        self.printTestResults(r)

    def testAndPrintShort(self,string):
        r = self.performTest(string)
        self.printTestResults(r)
        
