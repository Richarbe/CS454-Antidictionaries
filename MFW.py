import FactorDAWG as FD

class MFW():

    def __init__(self, string):

        #Create factor dawg class
        self.__fDAWG = FD.FactorDAWG(string)
        #Create minimal forbidden words automation
        self.MFWA = []
        self.__build__()

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
