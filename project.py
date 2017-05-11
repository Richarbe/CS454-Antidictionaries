import itertools
import time

MAX_WORD_LENGTH = 16

TEST_MESSAGE = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse gravida, nulla sed tincidunt volutpat, lorem ex mollis ipsum, vel ornare nisi justo in lacus. Ut id consequat turpis. Ut convallis tellus ligula, ut lobortis tortor volutpat eu. Vivamus posuere maximus ligula, sed bibendum dolor aliquam eu. Nulla sed gravida urna, et imperdiet dolor. Pellentesque a elit ac nisi maximus laoreet. Integer fringilla consectetur lacus, quis malesuada metus sollicitudin at. Nunc leo eros, tempor quis cursus vel, iaculis dapibus tortor. Etiam neque lorem, molestie ac blandit et, lobortis a ex. Nunc congue tortor quam, at iaculis diam ultrices vitae. Phasellus pulvinar sodales convallis. Curabitur eleifend nunc nulla, at imperdiet odio rhoncus non. Pellentesque volutpat malesuada lectus quis malesuada. Sed vel sodales ipsum. Sed fringilla neque ac ex dictum, a ultricies felis suscipit. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Ut vulputate massa ligula, at dapibus est accumsan in. Morbi vitae feugiat nulla. Phasellus convallis fermentum nibh, sed condimentum orci malesuada vitae. Etiam placerat elementum massa in accumsan. Morbi eleifend cursus metus, bibendum tincidunt ipsum ultrices eleifend. Vestibulum non purus arcu. Curabitur bibendum metus a mi aliquam dignissim. Nunc commodo eros dui, vitae porta eros volutpat eget. Sed eu leo quis elit semper eleifend. Donec a erat eu augue porttitor faucibus molestie vel urna. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam ac condimentum sapien. Aenean mattis ultrices lacinia. Donec ullamcorper lobortis ultricies. Nulla sed arcu et nunc molestie gravida. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Sed eu eros a elit interdum mattis sit amet at mauris. Praesent condimentum felis ut urna convallis, ac lobortis massa fringilla. Aenean eu metus enim. Suspendisse in accumsan urna, eget sollicitudin nulla. Nunc non quam at quam ullamcorper dignissim. Nunc consectetur purus justo, nec aliquet sem accumsan sed. Nullam tellus mi, pharetra sit amet pellentesque nec, pulvinar in libero. Phasellus non volutpat elit. Proin pretium facilisis nunc, a convallis metus pulvinar vitae. Sed imperdiet lobortis tellus in tincidunt. Sed scelerisque in enim a feugiat. In sollicitudin tellus odio, at commodo erat blandit non. Aliquam erat volutpat. Morbi ut mollis leo. Etiam id orci nec mi maximus interdum. Vivamus elementum lorem et ex tincidunt sollicitudin. Sed a accumsan tortor. Morbi feugiat turpis in ipsum blandit vestibulum id quis eros. Nunc enim eros, rhoncus a mi rutrum, facilisis varius erat. Praesent fringilla massa eget augue iaculis fringilla. Morbi scelerisque sollicitudin diam, sed malesuada massa volutpat nec. Sed viverra diam varius diam vulputate, non semper lectus porta. Vivamus at condimentum risus, vitae consectetur ex. Sed consectetur eros nec elementum feugiat.'

#------------------------------------------------------------------------------------------------------

class DAWG():
    
    def __init__(self):
        self.delta = []
        self.solid = []
        
    def newState(self):
        self.solid.append([-1,-1])
        self.delta.append([-1,-1])
        
    def solidTransaction(self,state,nextState,val):
        if(self.delta[state] != -1):
            self.delta[state][val] = nextState
            self.solid[state][val] = True
        else:
            self.delta[state] = [-1,-1]
            self.delta[state][val] = nextState
            self.solid[state][val] = True

    def nonSolidTransaction(self,state,nextState,val):
        if(self.delta[state] != -1):
            self.delta[state][val] = nextState
            self.solid[state][val] = False
        else:
            self.delta[state] = [None,None]
            self.delta[state][val] = nextState
            self.solid[state][val] = True
          
    def factorDAWG(self,string):
        self.newState()
        p = 0
        suf = [-1]*(len(string)*2) #suf is an array twice the elngth of the input string, initialized to -1's
        curState = 0
        
        for a in string:
            i = int(a)
            self.newState()
            q = curState+1
            self.solidTransaction(p,q,i)
            
            w = suf[p]
            
            while ((w != -1) and (self.delta[w][i] == -1)):
                self.nonSolidTransaction(w,q,i)
                w = suf[w]
            
            if(w != -1):
                v = -1
            else:
                v = self.delta[w][i]
                
            if w == -1:
                suf[q] = 0
            elif self.solid[w][i]:
                suf[q] = v
            else:
                self.newState()
                qp = curState+1
                
                self.delta[qp] = self.delta[v][:]
                self.solid[qp][0] = False
                self.solid[qp][0] = False
                
                self.delta[w][i] = qp
                suf[q] = qp
                suf[qp] = suf[v]
                suf[v] = qp
                
                w = suf[w]
                
                while w != -1 and self.solid[w][i]:
                    self.delta[w][i] = qp
                    w = suf[w]
                
            p = q
        print("help")
            
    

#DFA class, allows creating a DFA for alphabet {0,1} and testing binary strings for acceptance
class DFA():
    
    #Initialize DFA with option of setting the delta function: a list of transitions for each state
    #on alphabet {0,1}. Ex. dfa = DFA([(0,3),(1,2),(0,1),(2,1)])
    #State 0 goes to 0 on 0, goes to 3 on 1,
    #State 1 goes to 0 on 0, goes to 2 on 1,
    #State 2 goes to 0 on 0, goes to 1 on 1
    #State 3 goes to 2 on 0, goes to 1 on 1
    def __init__(self,delta):
        #The index represents state, delta return new value
        self.delta = []
        if delta is not None:
            self.setDelta(delta)
    
    #Set delta function for DFA
    def setDelta(self,delta):
        self.delta = []
        for s in delta:
            self.delta.append([s[0],s[1],False])
    
    #Changes the specified state,
    #t0 is state to go to on 0
    #t1 is state to go to on 1
    #final is whether it is an accepting state (True or False)
    def changeState(self,state,t0,t1,final):
        self.delta[state] = [t0,t1,final]
    
    #Sets the specified state(s) to be an accepting state
    def setToAccept(self,states):
        
        if(isinstance( states, int )):
            self.delta[states][2] = True
        else:
            for s in states:
                self.delta[s][2] = True
    
    #Adds a state to the DFA
    #t0 is the state to go to on input 0, t1 is for input 1
    #f is True, if the state is final state, false otherwise
    def addState(self,t0,t1,f):
        self.delta.append((t0,t1,f))
        print(self.delta)
    
    #State is current state, value is transition value. Returns the new state
    def transition(self,state,value):
        s = self.delta[state]
        return s[value]
        
    #Tests binary string and returns true if string is accepted
    def result(self,string,printSteps):
        
        s = 0
        if printSteps == None:
            printSteps = False
        
        for i in range(0,len(string)):
            s = self.transition(s,int(string[i]))
            if printSteps:
                print(s)
        return bool(self.delta[s][2])
    
    #Prints out the DFA to clearly show its states and their transitions
    def print(self):
        
        i = 0
        for s in self.delta:
            if(s[2]):
                print("State {0}: 0->{1} and 1->{2} (Accepting)".format(i,s[0],s[1]))
            else:
                print("State {0}: 0->{1} and 1->{2}".format(i,s[0],s[1]))
            i += 1
#----------------END OF CLASS: DFA----------------------------------------------------------------------


def binseq(k):
    return [''.join(x) for x in itertools.product('01', repeat=k)]


def ASCII_toBinStr(string):

    return bin(int.from_bytes(string.encode(), 'big'))[2:]

def binStrTo_ASCII(binString):
    
    n = int('0b'+binString, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode()

def iterate(length):
    
    arr = []
    i = 0
    while i < length:
        i += 1
        arr += binseq(i)
        
    return arr

def buildAD_super_slow(string):
    AD = []
    
    #length = len(string)
    #if length > MAX_WORD_LENGTH:
    #    length = MAX_WORD_LENGTH
    
    iterations = iterate(MAX_WORD_LENGTH)
    
    for i in iterations:
        
        isIn = False
        
        for w in AD:
            if w in i:
                isIn = True
                break
        
        if not isIn:
            if i not in string:
                AD.append(i)
                
    return AD

def notInAntiDict(antiDict,word):
    
    if len(word) >= 1:
        suf = word
    else:
        return True

    for w in antiDict:
        
        s = suf
        
        while len(s) >= 1:
            
            if w == (s + '0') or w == (s + '1'):
                return False
            else:
                s = s[1:]
    
    return True
    
def isInAntiDict(antiDict,word):
    
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
    
def encodeBits(bitString):

    final = ''
    
    for b in bitString:
        if b == '1':
            final += '10'
        else:
            final += '0'
            
    return final
    
def decodeBits(bitString):
    
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
    
def encodeAntiDict(antiDict):
    
    if len(antiDict) <= 0:
        return ''
    
    final = ''
    
    for w in antiDict:
        final += encodeBits(w) + '11'
    
    return final[:-2]

def decodeAntiDict(bitStringArray):
    
    AD = []
    for w in bitStringArray:
        AD.append(decodeBits(w))
        
    return AD
    
def encode(antiDict,string):
  s = ''
  compressed = ''
  
  for w in string:
    
    notInAD = not isInAntiDict(antiDict,s)[0]
    
    s += w
    
    if notInAD:
        compressed += w
    
  return (len(string),compressed)

def decode(antiDict,length,compressed):
    s = ''
    i = 0
    
    while len(s) < length:
        
        inAD = isInAntiDict(antiDict,s)
        
        if inAD[0]:
            s += inAD[1]
        else:
            s += compressed[i]
            i += 1
            
    return s

def fullEncode(string):
    AD = buildAD_super_slow(string)
    eAD = encodeAntiDict(AD)
    
    e = encode(AD,string)
    
    l = bin(e[0])[2:]
    el = encodeBits(l)
    
    return el + '11' + eAD + '1111' + e[1]

def fullDecode(compressed):
    
    data = compressed.split('1111',1)
    header = data[0].split('11')
    n = int(decodeBits(header[0]),2)
    AD = decodeAntiDict(header[1:])
    s = data[1]
    
    return decode(AD,n,s)

def performTest(stringLength,maxWordLength):
    MAX_WORD_LENGTH = maxWordLength
    
    s = TEST_MESSAGE[0:stringLength]
    
    t = time.time()
    
    b = ASCII_toBinStr(s)
    
    e = fullEncode(b)
    
    d = fullDecode(e)
    
    m = binStrTo_ASCII(d)
    
    v = len(b)/len(e)
    
    return ('Original length: ' + str(len(b)),'Compressed length: ' + str(len(e)),'Compression value: ' + str(v), 'Time elapsed: ' + str(time.time() - t))
    
def performTestFull(stringLength,maxWordLength):
    MAX_WORD_LENGTH = maxWordLength #Set global var
    s = TEST_MESSAGE[0:stringLength] #Create string of specific length
    t = time.time() #Mark start time
    
    b = ASCII_toBinStr(s) #Convert string into binary string
    
    AD = buildAD_super_slow(b) #Build anti-dictionary from binary string
    eAD = encodeAntiDict(AD) #Encode anti-dictionary into binary string
    
    e = encode(AD,b) #Encode message using anti-dictionary on binary message
    
    l = bin(e[0])[2:] #Get the length of binary message (as binary value)
    el = encodeBits(l) #Encode binary value
    
    #Final result is  length + anti-dictionary + compressed message all encoded into bit string
    full_e = el + '11' + eAD + '1111' + e[1]
    
    stop = time.time() - t #Stop timer to get elapsed time
    
    v = len(b)/len(full_e) #Calculate compression ratio (original/compressed)
    
    return ('Original length: ' + str(len(b)),'Compressed length: ' + str(len(e[1])),'Anti-dict length: ' + str(len(eAD)),'Total compressed length: ' + str(len(full_e)),'Compression value: ' + str(v), 'Time elapsed: ' + str(time.time() - t))
    
def printTestResults(results):
    
    for r in results:
        print(r)
        
def testAndPrint(strLength,maxWordLength):
    r = performTest(strLength,maxWordLength)
    printTestResults(r)

def main():
    d = DAWG()
    d.factorDAWG("111")

if __name__ == "__main__":
    main()