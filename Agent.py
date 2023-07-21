"""
Logical Agent for programming assignment 2.
"""

class Agent:
    def __init__(self):
        self._mineFieldWorld = [
                 ['','','M','',''], # Rooms [1,5] to [5,5]
                 ['','M','G','M',''], # Rooms [1,4] to [4,4]
                 ['','','M','','M'], # Rooms [1,3] to [4,3]
                 ['','','','',''], # Rooms [1,2] to [4,2] 
                 ['','','M','',''],  # Rooms [1,1] to [4,1]
                ] # This is the mine field world shown in the assignment question.
                  # A different instance of the mine field world will be used for evaluation.
        self._curLoc = [1,1]
        self._isAlive = True

    def _FindIndicesForLocation(self,loc):
        x,y = loc
        i,j = 5-y, x-1
        return i,j

    def _CheckForMine(self):
        mf = self._mineFieldWorld
        i,j = self._FindIndicesForLocation(self._curLoc)
        if 'M' in mf[i][j]:
            print(mf[i][j])
            self._isAlive = False
            print('Agent is DEAD.')
        return self._isAlive

    def TakeAction(self,action): # The function takes an action and returns whether the Agent is alive
                                # after taking the action.
        validActions = ['Up','Down','Left','Right']
        assert action in validActions, 'Invalid Action.'
        if self._isAlive == False:
            print('Action cannot be performed. Agent is DEAD. Location:{0}'.format(self._curLoc))
            return False

        index = validActions.index(action)
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        move = validMoves[index]
        newLoc = []
        for v, inc in zip(self._curLoc,move): #Loop will iterate twice
            z = v + inc #increment location index
            z = 5 if z>5 else 1 if z<1 else z #Ensure that index is between 1 and 5
            newLoc.append(z)
        self._curLoc = newLoc
        print('Action Taken: {0}, Current Location {1}'.format(action,self._curLoc))
        return self._CheckForMine()
    
    def _FindAdjacentRooms(self):
        cLoc = self._curLoc
        validMoves = [[0,1],[0,-1],[-1,0],[1,0]]
        adjRooms = []
        for vM in validMoves:
            room = []
            valid = True
            for v, inc in zip(cLoc,vM):
                z = v + inc
                if z<1 or z>5:  #Check whether index is between 1 and 5
                    valid = False
                    break
                else:
                    room.append(z)
            if valid==True:
                adjRooms.append(room)
        return adjRooms
                
        
    def PerceiveCurrentLocation(self): #This function perceives the current location. 
                                        #It detects whether mine is present in adjacent rooms.
        percept = None
        mf = self._mineFieldWorld
        if self._isAlive == False:
            print('Agent cannot perceive. Agent is DEAD. Location:{0}'.format(self._curLoc))
            return None

        adjRooms = self._FindAdjacentRooms()
        count=0
        for room in adjRooms:
            i,j = self._FindIndicesForLocation(room)
            if 'M' in mf[i][j]:
                count+=1
        percept = count
        return percept
    
    def FindCurrentLocation(self):
        return self._curLoc

def main():
    ag = Agent()
    print('curLoc',ag.FindCurrentLocation())
    print('Percept ',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Right')
    print('Percept',ag.PerceiveCurrentLocation())
    ag.TakeAction('Up')
    print('Percept',ag.PerceiveCurrentLocation())

if __name__=='__main__':
    main()  