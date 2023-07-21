#!/usr/bin/env python3
from pysat.solvers import Glucose3

from Agent import *  # See the Agent.py file

#### All your code can go here.

def adjroom(cLoc): #returns a list of lists
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

def tup(room): #turns room list into room tuple for set hashing.
    return (room[0], room[1])
#### You can change the main function as you wish. Run this program to see the output. Also see Agent.py code.


def main():
    g = Glucose3()
    ag = Agent()
    cur = ag.FindCurrentLocation()
    
    action = ["Up", "Down", "Right", "Left"]

    undetrooms = set()
    for x in range(1,6):
        for y in range(1,6):
            undetrooms.add((x,y))
    saferooms = {(1,1)}
    minerooms = set()
    undetrooms = undetrooms - saferooms
    visitedrooms = {(1,1)}
    newadj = list()
    n = set()

    g.add_clause([1])
    q = [(1,1)]
    if(ag.PerceiveCurrentLocation() != 0):
        print("Gold could not be detected after visiting all the safe rooms.")
        return

    while(q):
        cur = list(q.pop())
        visitedrooms.add(tuple(cur))
        adj = adjroom(cur)

        q_temp = list()
        q_temp.append(tuple(ag.FindCurrentLocation()))

        parent = dict()
        parent[tuple(ag.FindCurrentLocation())] = None

        bfs_visit = set()
        bfs_visit.add(tuple(ag.FindCurrentLocation()))

        while (q_temp):
            curr = q_temp.pop()
            if curr == tuple(cur):
                break
            adjRooms = adjroom([curr[0],curr[1]])
            for room in adjRooms:
                if (tuple(room) not in bfs_visit) and (tuple(room) in saferooms):
                    bfs_visit.add(tuple(room))
                    parent[tuple(room)] = curr
                    q_temp.append(tuple(room))

        bfs_path = []

        while curr != tuple(ag.FindCurrentLocation()):
            bfs_path.append(list(curr))
            curr = parent[tuple(curr)]

        bfs_path.append(ag.FindCurrentLocation())
        bfs_path.reverse()

        q_temp.clear()
        parent.clear()
        bfs_visit.clear()

        moves = []

        for i in range(len(bfs_path) - 1):
            if [bfs_path[i+1][0] - bfs_path[i][0], bfs_path[i+1][1] - bfs_path[i][1]] == [0,1]:
                moves.append(0)
            elif [bfs_path[i+1][0] - bfs_path[i][0], bfs_path[i+1][1] - bfs_path[i][1]] == [0,-1]:
                moves.append(1)
            elif [bfs_path[i+1][0] - bfs_path[i][0], bfs_path[i+1][1] - bfs_path[i][1]] == [1,0]:
                moves.append(2)
            elif [bfs_path[i+1][0] - bfs_path[i][0], bfs_path[i+1][1] - bfs_path[i][1]] == [-1,0]:
                moves.append(3)

        for x in moves:
            ag.TakeAction(action[x])

        bfs_path.clear()
        moves.clear()
        
        if(len(adj) == 2): #corner room
            if(ag.PerceiveCurrentLocation() == 1): #at least one will be in a safe room
                if tup(adj[0]) in saferooms:
                    minerooms.add(tup(adj[1]))
                    cl = -((adj[1][1] - 1) * 5 + adj[1][0])
                    g.add_clause([cl])
                else:
                    minerooms.add(tup(adj[0]))
                    cl = -((adj[0][1] - 1) * 5 + adj[0][0])
                    g.add_clause([cl])
            else:
                for x in range(2):
                    saferooms.add(tup(adj[x]))
                    cl = (adj[x][1] - 1) * 5 + adj[x][0]
                    g.add_clause([cl])

        elif(len(adj) == 3): #edge rooms that are not corners
            if(ag.PerceiveCurrentLocation() == 0):
                for x in range(3):
                    saferooms.add(tup(adj[x]))
                    cl = (adj[x][1] - 1) * 5 + adj[x][0]
                    g.add_clause([cl])
            elif(ag.PerceiveCurrentLocation() == 1):
                newadj.clear()
                for x in range(3):
                    if tup(adj[x]) not in saferooms:
                        newadj.append(adj[x]) #don't know what they contain cause they are not in safe set
                if(len(newadj) == 1): #contains just one square that is not safe, hence it contains the mine
                    minerooms.add(tup(newadj[0]))
                    cl = -((newadj[0][1] - 1) * 5 + newadj[0][0])
                    g.add_clause([cl])
                else:
                    if tup(newadj[0]) in minerooms: #we know one mine location, so the other has to be safe since percept is one.
                        saferooms.add(tup(newadj[1]))
                        cl = (newadj[1][1] - 1) * 5 + newadj[1][0]
                        g.add_clause([cl])
                    elif tup(newadj[1]) in minerooms:
                        saferooms.add(tup(newadj[0]))
                        cl = (newadj[0][1] - 1) * 5 + newadj[0][0]
                        g.add_clause([cl])
                    else: #we have no precise info about either of the two squares, so we add prolog statements to the kb.
                        cl0 = (newadj[0][1] - 1) * 5 + newadj[0][0]
                        cl1 = (newadj[1][1] - 1) * 5 + newadj[1][0]
                        g.add_clause([cl0, cl1])
                        g.add_clause([-cl0, -cl1])
            else:
                newadj.clear()
                for x in range(3):
                    if tup(adj[x]) not in saferooms:
                        newadj.append(adj[x])
                for x in range(2):
                    cl = -((newadj[x][1] - 1) * 5 + newadj[x][0])
                    g.add_clause([cl])

        else: #centre square rooms
            if(ag.PerceiveCurrentLocation() == 0):
                for x in range(4):
                    saferooms.add(tup(adj[x]))
                    cl = (adj[x][1] - 1) * 5 + adj[x][0]
                    g.add_clause([cl])
            elif(ag.PerceiveCurrentLocation() == 1):
                newadj.clear()
                for x in range(4):
                    if tup(adj[x]) not in saferooms:
                        newadj.append(adj[x])
                if(len(newadj) == 1):
                    minerooms.add(tup(newadj[0]))
                    cl = -((newadj[0][1] - 1) * 5 + newadj[0][0])
                    g.add_clause([cl])
                elif(len(newadj) == 2): #but percept is 1. note that newadj does NOT include any of the safe rooms
                    if tup(newadj[0]) in minerooms:
                        saferooms.add(tup(newadj[1]))
                        cl = (newadj[1][1] - 1)*5 + newadj[1][0] 
                        g.add_clause([cl]) 
                    elif tup(newadj[1]) in minerooms:
                        saferooms.add(tup(newadj[0]))
                        cl = (newadj[0][1] - 1)*5 + newadj[0][0] 
                        g.add_clause([cl])
                    else:
                        cl0 = (newadj[0][1] - 1) * 5 + newadj[0][0]
                        cl1 = (newadj[1][1] - 1) * 5 + newadj[1][0]
                        g.add_clause([cl0, cl1])
                        g.add_clause([-cl0, -cl1])
                else:
                    if tup(newadj[0]) in minerooms:
                        saferooms.add(tup(newadj[1]))
                        cl = (newadj[1][1] - 1)*5 + newadj[1][0] 
                        g.add_clause([cl])
                        saferooms.add(tup(newadj[2]))
                        cl = (newadj[2][1] - 1)*5 + newadj[2][0] 
                        g.add_clause([cl])
                    elif tup(newadj[1]) in minerooms:
                        saferooms.add(tup(newadj[0]))
                        cl = (newadj[0][1] - 1)*5 + newadj[0][0] 
                        g.add_clause([cl])
                        saferooms.add(tup(newadj[2]))
                        cl = (newadj[2][1] - 1)*5 + newadj[2][0] 
                        g.add_clause([cl])
                    elif tup(newadj[2]) in minerooms:
                        saferooms.add(tup(newadj[1]))
                        cl = (newadj[1][1] - 1)*5 + newadj[1][0] 
                        g.add_clause([cl])
                        saferooms.add(tup(newadj[2]))
                        cl = (newadj[0][1] - 1)*5 + newadj[0][0] 
                        g.add_clause([cl])
                    else: 
                        cl0 = (newadj[0][1] - 1) * 5 + newadj[0][0]
                        cl1 = (newadj[1][1] - 1) * 5 + newadj[1][0]
                        cl2 = (newadj[2][1] - 1) * 5 + newadj[2][0]
                        g.add_clause([-cl0,-cl1,-cl2])
                        g.add_clause([cl0,cl1])
                        g.add_clause([cl0,cl2])
                        g.add_clause([cl2,cl1])
            elif(ag.PerceiveCurrentLocation() == 2):
                newadj.clear()
                for x in range(4):
                    if tup(adj[x]) not in saferooms: #newadj must have at least 2 rooms that are not declared safe
                        newadj.append(adj[x])
                if(len(newadj) == 2): #not safe definitely contain the mines.
                    minerooms.add(tup(newadj[0]))
                    cl = -((newadj[0][1]-1)*5 + newadj[0][0])
                    g.add_clause([cl])
                    minerooms.add(tup(newadj[1]))
                    cl = -((newadj[1][1]-1)*5 + newadj[1][0])
                    g.add_clause([cl])
                else:
                    cl0 = (newadj[0][1] - 1) * 5 + newadj[0][0]
                    cl1 = (newadj[1][1] - 1) * 5 + newadj[1][0]
                    cl2 = (newadj[2][1] - 1) * 5 + newadj[2][0]
                    #exactly two rooms contain a mine logic clauses -> exactly one room does NOT contain a mine.
                    g.add_clause([cl0, cl1, cl2])
                    g.add_clause([-cl0, -cl1])
                    g.add_clause([-cl0, -cl2])
                    g.add_clause([-cl2, -cl1])
            else:
                newadj.clear()
                for x in range(4):
                    if tup(adj[x]) not in saferooms:
                        newadj.append(adj[x])
                for x in range(3):
                    minerooms.add(tup(newadj[x]))
                    cl = -((newadj[x][1]- 1) * 5 + newadj[x][0])
                    g.add_clause([cl])
        
        #to check if room is safe: (cl is room)
        # g.solve(assumptions = [-cl]) == false
        # to check if room is unsafe:
        # g.solve(assumptions = [cl]) == false
        undetrooms = undetrooms - saferooms - minerooms
        newsafe = set()
        flag = 1
        while flag == 1:
            flag = 0
            for x in undetrooms:
                y = (x[1] - 1)*5 + x[0]
                if(g.solve(assumptions = [-y]) == False):
                    r = (y%5 if y%5 != 0 else 5, (y-1)//5 + 1)
                    saferooms.add(r)
                    newsafe.add(r)
                    undetrooms = undetrooms - {r}
                    flag = 1
                if(g.solve(assumptions = [y]) == False):
                    r = (y%5 if y%5 != 0 else 5, (y-1)//5 + 1)
                    minerooms.add(r)
                    undetrooms = undetrooms - {r}
                    flag = 1
        
        for x in range(len(adj)):
            n.add((adj[x][0], adj[x][1]))
        for x in (saferooms - visitedrooms).intersection(n):
            q.append(x)
        for x in newsafe:
            q.append(x)
        n.clear()
        newsafe.clear()

    flag = 0
    gx = 0 
    gy = 0
    for x in range (2,5):
        for y in range (2,5):
            if ((x+1, y) in minerooms) and ((x-1, y) in minerooms) and ((x, y+1) in minerooms) and ((x, y-1) in minerooms): 
                gx = x
                gy = y
                flag = 1
    if flag == 1:
        print("Gold is present in room [", gx,",",gy,"].")
    else:
        print("Gold could not be detected after visiting all the safe rooms.")
    # print(minerooms)
    # print(undetrooms)
    # print(visitedrooms)
    # print(saferooms)

if __name__=='__main__':
    main()
