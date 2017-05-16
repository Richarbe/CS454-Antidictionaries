import FactorDAWG as FD

class MFW():

    def __init__(self, string_or_bytearray):
        if type(string_or_bytearray) is str:
            #Create factor dawg class
            self.__fDAWG = FD.FactorDAWG(string_or_bytearray)
            #Create minimal forbidden words automation
            self.MFWA = []
            self.__build__()
        elif type(string_or_bytearray) is bytearray:
            self.__fDAWG = None
            self.MFWA = []
            self.decodeFromByteArray(string_or_bytearray)

    #Checks whether word is in MFWA
    def isInAntiDict(self,string):
        
        state = 0
        
        for l in string:
            a = int(l)
            if self.MFWA[state][a] == -1:
                return True
            
            state = self.MFWA[state][a]
        
        return False
        
    #Builds a MFW automaton for testing whether word is in anti-dictionary
    def __build__(self):
        #Each node contains data: adj, dist, prev and path
        #dist is distance to source, prev is previous node index, adj is the adjacency list
        #a binary string representing the path to the node
        
        nodes = []
        queue = []
        rawG = self.__fDAWG.delta

        #Read graph into node array
        c = 0
        for i in rawG:
            #cur node index, dist to source, prev node index, (node on input '0', node on input '1')
            nodes.append([c,-1,-1,(i[0],i[1])])
            c += 1

        #Initialize source node
        nodes[0][0] = 0

        queue.append(nodes[0])#Add source node to queue

        while queue:
            n = queue.pop()

            #Queue adjacency list nodes and update their data
            if n[3][0] != -1:
                child = nodes[n[3][0]]

                #If distance has not been set, enqueue
                if child[1] < 0:
                    child[1] = n[1] + 1   #Update distance
                    child[2] = n[0] #Update previous
                    queue.append(child)   #Add to queue

            if n[3][1] != -1:
                
                child = nodes[n[3][1]]
                if child[1] < 0:
                    child[1] = n[1] + 1
                    child[2] = n[0]
                    queue.append(child)

        for n in nodes:
            self.MFWA.append(n[3])

    def encodeAsByteArray(self): #outputs dfa as bytearray
        OutArray = bytearray()
        numEntries = len(self.MFWA)+1#+1 is for the end state, -1
        intSize = 0
        temp = numEntries-1#top index
        while temp > 0: #figures out how large each integer needs to be to index all entries
            intSize += 1
            temp = temp >> 8
        NewEndstate = (1 << (intSize * 8)) - 1 #highest possible value given intsize
        OutArray.extend(intSize.to_bytes(1, byteorder = 'big'))
        for tup in self.MFWA:
            for i in tup:
                if(i == -1): #can't store -1, so will instead be stored as top possible value.
                    i = NewEndstate
                OutArray.extend(i.to_bytes(intSize, byteorder= 'big'))
        return OutArray

    def decodeFromByteArray(self, ByteArray):
        intSize = int(ByteArray[0])
        pos = 1 #start right after where intSize is stored
        size = len(ByteArray)
        endState = (1 << (intSize * 8)) - 1
        while pos < size:
            first = int.from_bytes(ByteArray[pos:pos+intSize], byteorder='big')
            #first integer is made from intsize bytes starting at pos
            second = int.from_bytes(ByteArray[pos+intSize:pos+(2*intSize)], byteorder='big')
            #second made from intsize bytes starting at pos+intsize
            if first == endState:
                first = -1
            if second == endState:
                second = -1
            self.MFWA.append((first, second))
            pos += intSize * 2

