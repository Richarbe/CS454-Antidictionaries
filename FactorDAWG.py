class FactorDAWG():
    
    #Create empty arrays to store state and transition data
    def __init__(self,string):
        #Stores pair for each state, where state 0 has index 0.
        #Example: delta = [[0,2],[2,1],[1,0]], q0: 0->q0, 1->q2, q1: 0->q2, 1->q1 etc.
        self.delta = []
        #A pair indicating whether transition is solid or weak on inputs 1 and 0
        #Example, solid on 0 and weak on 1: [True,False]
        self.__solid = [] 
        #A list to hold generated suffix data
        self.__suf = []

        #Build the data from string
        self.__build(string)
        
    #Performs suf[index] = value, if index is out of range, appends value to suf
    def __setSuf(self,index,value):
        if len(self.__suf) > index:
            self.__suf[index] = value
        else:
            self.__suf.append(value)
    
    #Returns the value at specified index. If index is out of range, returns -1
    def __getSuf(self,index):
        if len(self.__suf) > index:
            return self.__suf[index]
        else:
            self.__suf.append(-1)
            return -1
    
    #Creates a new empty state with no transitions (indicated by [-1,-1])
    def __newState(self):
        
        self.delta.append([-1,-1])
        self.__solid.append([False,False])
        
        return len(self.delta) - 1 #Returns number of new state
    
    #Adds a solid transition on value, from state to next state.
    #Example __solidTransaction(1,2,0): Solid transition from state 1 to state 2, on input 0
    def __solidTransaction(self,state,nextState,val):
        if(len(self.delta) > state):
            self.delta[state][val] = nextState
            self.__solid[state][val] = True
        else:
            self.__newState() #Create new state
            self.delta[state][val] = nextState
            self.__solid[state][val] = True

    def __nonsolidTransaction(self,state,nextState,val):
        if(len(self.delta) > state):
            self.delta[state][val] = nextState
            self.__solid[state][val] = False
        else:
            self.__newState() #Create new state
            self.delta[state][val] = nextState
            self.__solid[state][val] = False
          
    def __build(self,string):
        
        #Initialize delta, solid and suf arrays
        self.delta = []
        self.__solid = [] 
        self.__suf = [-1]
        
        
        p = self.__newState() #Set p to initial state
        
        for i in string:
            a = int(i) #Converts letter  i of string into a value a
            q = self.__newState()
            self.__solidTransaction(p,q,a)
            
            w = self.__getSuf(p)
            
            #While w is not nil, and  delta(w, a) = nil:
            while ((w != -1) and (self.delta[w][a] == -1)):
                self.__nonsolidTransaction(w,q,a)
                w = self.__getSuf(w)
            
            v = self.delta[w][a]
            
            if w == -1: #If w i nil
                self.__setSuf(q,0)
            elif self.__solid[w][a]: #IF delta(w, a) = v is a solid transaction
                self.__setSuf(q,v)
            else:
                #Perform SPLIT algorithm
                qp = self.__newState() #Create new state, q'
                
                #q' has same transactions as v except that they are all non-solid
                self.delta[qp][0] = self.delta[v][0]
                self.delta[qp][1] = self.delta[v][1]
                #Set q' transactions to non solid
                self.__solid[qp][0] = False
                self.__solid[qp][1] = False
                
                #change delta(w, a) = q into a solid transaction delta(w, a) = q'
                self.delta[w][a] = qp
                
                self.__setSuf(q,qp)
                self.__setSuf(qp,self.__getSuf(v))
                self.__setSuf(v,qp)
                
                w = self.__getSuf(w)
                
                #while w != nil and delta(w, a) is a solid transaction do:
                while w != -1 and self.__solid[w][a]:
                    self.delta[w][a] = qp
                    w = self.__getSuf(w)
                
            p = q
