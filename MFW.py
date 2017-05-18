import FactorDAWG as FD

class MFW():
    def __init__(self, string_or_bytearray):
        if type(string_or_bytearray) is str:
            # Create factor dawg class
            self.__fDAWG = FD.FactorDAWG(string_or_bytearray)
            # Create minimal forbidden words automation
            self.MFWA = []
            self.__paths = []
            self.__build__()
            self.Transducer = []
        elif type(string_or_bytearray) is bytearray:
            self.__fDAWG = None
            self.MFWA = []
            self.__paths = []
            self.decodeFromByteArray(string_or_bytearray)
            self.Transducer = []

    # Checks whether word is in MFWA
    def isInAntiDict(self, string):

        state = 0

        for l in string:
            a = int(l)
            if self.MFWA[state][a] == -1:
                return True

            state = self.MFWA[state][a]

        return False

    def isInMFW(self, string):

        state = 0
        for l in string:
            a = int(l)
            if state == -2:
                return False
            if self.MFWA[state][a] == -1:
                return False
            state = self.MFWA[state][a]
        if self.MFWA[state][a] == -2:
            return True
        return False

    def Encode(self,string):
        #from page 8 of Crochemore "Data Compression using Antidictionaries" (antidict.pdf)
        outputTape = ""
        state = 0
        for l in string:
            a = int(l)
            if self.Transducer[state][a] == -1:
                return outputTape
            if self.Transducer[state][0] != -1 or self.Transducer[state][1] != -1:
                    if self.Transducer[state][0] != -1 and self.Transducer[state][1] != -1:
                        #has two outgoing edges
                        outputTape += l
                    else:
                        #has one outgoing edge
                        #add nothing to output tape
                        pass
        return outputTape


    def Decode(self,string, length): #currently exact copy of encode, no idea what I am doing.
        outputTape = ""
        state = 0
        for l in string:
            a = int(l)
            if self.Transducer[state][a] == -1:
                return outputTape
            if self.Transducer[state][0] != -1 or self.Transducer[state][1] != -1:
                    if self.Transducer[state][0] != -1 and self.Transducer[state][1] != -1:
                        #has two outgoing edges
                        outputTape += l
                    else:
                        #has one outgoing edge
                        #add nothing to output tape
                        pass
        return outputTape

    def createTransducer(self):
        sink = len(self.MFWA) - 1
        self.Transducer = []
        for state in range(len(self.MFWA) - 1):
            temp = self.MFWA[state][:]
            for i in range(2):
                if temp[i] == sink:
                    temp[i] = -1
            self.Transducer.append(temp)
        return


    #Builds a MFW automaton for testing whether word is in anti-dictionary

    def __build__(self):
        # Each node contains data: adj, dist, prev and path
        # dist is distance to source, prev is previous node index, adj is the adjacency list
        # a binary string representing the path to the node

        nodes = []
        queue = []
        rawG = self.__fDAWG.delta

        # Read graph into node array
        c = 0
        for i in rawG:
            # cur node index, dist to source, prev node index, (node on input '0', node on input '1')
            nodes.append([c, -1, -1, (i[0], i[1])])
            c += 1

        # Initialize source node
        nodes[0][0] = 0

        queue.append(nodes[0])  # Add source node to queue

        while queue:
            n = queue.pop()

            # Queue adjacency list nodes and update their data
            if n[3][0] != -1:
                child = nodes[n[3][0]]

                # If distance has not been set, enqueue
                if child[1] < 0:
                    child[1] = n[1] + 1  # Update distance
                    child[2] = n[0]  # Update previous
                    queue.append(child)  # Add to queue

            if n[3][1] != -1:

                child = nodes[n[3][1]]
                if child[1] < 0:
                    child[1] = n[1] + 1
                    child[2] = n[0]
                    queue.append(child)

        sink = len(rawG)
        for s in range(0, len(rawG)):

            self.MFWA.append([-1, -1])

            if rawG[s][0] == -1 and (s == 0 or rawG[self.__fDAWG.getSuf(s)][0] != -1):
                self.MFWA[s][0] = sink
            else:
                self.MFWA[s][0] = rawG[s][0]

            if rawG[s][1] == -1 and (s == 0 or rawG[self.__fDAWG.getSuf(s)][1] != -1):
                self.MFWA[s][1] = sink
            else:
                self.MFWA[s][1] = rawG[s][1]

        self.MFWA.append([-2, -2])

    def encodeAsByteArray(self):  # outputs dfa as bytearray
        OutArray = bytearray()
        numEntries = len(self.MFWA)+2#+1 is for the end state, -1
        intSize = 0
        temp = numEntries - 1  # top index
        while temp > 0:  # figures out how large each integer needs to be to index all entries
            intSize += 1
            temp = temp >> 8
        NewEndstate = (1 << (intSize * 8)) - 1  # highest possible value given intsize
        OutArray.extend(intSize.to_bytes(1, byteorder='big'))
        for tup in self.MFWA:
            for i in tup:
                if (i == -1):  # can't store -1, so will instead be stored as top possible value.
                    i = NewEndstate
                if(i == -2): #same
                    i = NewEndstate - 1
                OutArray.extend(i.to_bytes(intSize, byteorder= 'big'))
        return OutArray

    def decodeFromByteArray(self, ByteArray):
        intSize = int(ByteArray[0])
        pos = 1  # start right after where intSize is stored
        size = len(ByteArray)
        endState = (1 << (intSize * 8)) - 1
        while pos < size:
            first = int.from_bytes(ByteArray[pos:pos+intSize], byteorder='big')
            #first integer is made from intsize bytes starting at pos
            second = int.from_bytes(ByteArray[pos+intSize:pos+(2*intSize)], byteorder='big')
            #second made from intsize bytes starting at pos+intsize
            if first >= endState - 1:
                first = first - (endState + 1) #-1 if endstate, -2 is endstate-1
            if second >= endState - 1:
                second = second - (endState + 1) #-1 if endstate, -2 is endstate-1
            self.MFWA.append((first, second))
            pos += intSize * 2
