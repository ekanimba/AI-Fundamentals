
import math
import copy
import numpy as np


mutualDistance = \
    {\
    "A":{"A":0,"B":2,"C":1,"S":11},\
    "B":{"A":2,"B":0,"C":4,"S":5},\
    "C":{"A":1,"B":4,"C":0,"S":8},\
    "S":{"A":11,"B":5,"C":8,"S":0}\
    }
demand = {"A":5,"B":3,"C":7}  
supplierSupply = {"S":500} 
totalDemand = np.sum(list(demand[item] for item in demand))
isOutOfStock = False

maximumTruckcargo = 4
truckLoad = 4

class Node:
    def __init__(self,entitiesDict,supplierDict,truck,recipient,cost,routeHistory):
        self.entities = entitiesDict
        self.supplier = supplierDict
        self.truck = truck
        self.recipient = recipient
        self.accumulatedCost = cost
        self.routeHistory = routeHistory
        
    def setResidence(self,newResidence):
        self.recipient = newResidence
        self.routeHistory.append(newResidence)
    
    def _isSupplied(self):
        for item in self.entities:
            if(self.entities[item] > 0):
                return False
        return True
    
    def _delivery(self,recipent):
        self.entities[recipent] -= self.truck
        self.truck = 0
        if(self.entities[recipent] < 0):
            self.truck += self.entities[recipent] * (-1)
            self.entities[recipent] = 0
    
    def loadUp(self):
        global isOutOfStock,maximumTruckcargo
        newTruckLoad = maximumTruckcargo
        if(self.supplier["S"] == 0):
            isOutOfStock = True
            return
        if(self.supplier["S"] < newTruckLoad):
            newTruckLoad = self.supplier["S"]
        self.supplier["S"] -= newTruckLoad
        self.truck = newTruckLoad
        
    def addCost(self,cost):
        self.accumulatedCost += cost
    
    def calculateCost(_from, _to):
        global mutualDistance
        return mutualDistance[_from][_to]
    
    def isTruckEmpty(self):
        return (self.truck == 0)
    
    
    def explore(node):
        expandedNodes = []
        if(node.isTruckEmpty()): 
            newNode = copy.deepcopy(node)
            newNode.setResidence("S")
            
            newNode.addCost(Node.calculateCost(node.recipient,newNode.recipient))
            newNode.loadUp()
            expandedNodes.append(newNode)
            
            return expandedNodes
        for item in node.entities:
            if (node.entities[item] > 0 and node.entities[item] != node.recipient):
                newNode = copy.deepcopy(node)
                newNode.setResidence(item)
                
                newNode.addCost(Node.calculateCost(node.recipient,newNode.recipient))
                newNode._delivery(item)
                expandedNodes.append(newNode)
                
        return expandedNodes
    
    def findBestHeuristicIndex(nodeList):
        global totalDemand
        last_left = math.inf
        lowestHeurNode = None
        for node in nodeList:
            current_left = totalDemand - evaluateDemand(node.entities)
            if(current_left < last_left):
                lowestHeurNode = node
                last_left = current_left
        return nodeList.index(lowestHeurNode)

    def printNode(self):
        print(self.entities,"|truck: ",self.truck,"|recipient: ",self.recipient,"|cost: ",self.accumulatedCost,"|")


def evaluateDemand(demandLeftDict):
    return np.sum(list(demandLeftDict[item] for item in demandLeftDict))

def blindSearch(mode):
    print(mode, "search algorithm ")
    global mutualDistance,demand,truckLoad,isOutOfStock
    isOutOfStock = False
    position = 0
    if(mode == "BFS"):
        position = 0
    else:
        position = -1
    queue = []
    routeHistory = []
    truckResidence = "S"
    cost = 0
    queue.append(Node(copy.deepcopy(demand),copy.deepcopy(supplierSupply),0,truckResidence,0,[truckResidence]))
    queue[0].loadUp()
    
    while(1):
        currentNode = queue.pop(position)
        if(currentNode._isSupplied()):
            currentNode.printNode()
            print("Path: ",currentNode.routeHistory)
            break
        tmp = Node.explore(currentNode)
        if (isOutOfStock):
            currentNode = tmp[0]
            print("Path: ",currentNode.routeHistory)
            break
        queue.extend(tmp)

def heuresticSearch():
    print("heurestic Search algorithm")
    global mutualDistance,demand,truckLoad,isOutOfStock
    isOutOfStock = False
    queue = []
    routeHistory = []
    truckResidence = "S"
    cost = 0
    queue.append(Node(copy.deepcopy(demand),copy.deepcopy(supplierSupply),0,truckResidence,0,[truckResidence]))
    queue[0].loadUp()
    
    while(1):
        currentNode = queue.pop(Node.findBestHeuristicIndex(queue))
        if(currentNode._isSupplied()):
            currentNode.printNode()
            print("Path: ",currentNode.routeHistory)
            break

        tmp = Node.explore(currentNode)
        if(isOutOfStock):
            currentNode = tmp[0]
            print("out of stock while: heurestic "," search ", "|stock status: ",currentNode.supplier,currentNode.entities,"|Total Cost: ", currentNode.accumulatedCost,"| recipient: ", currentNode.recipient)
            print("Path: ",currentNode.routeHistory)
            break
        queue.extend(tmp)

if __name__ == '__main__':
    #blindSearch("BFS")
    blindSearch("DFS")
    #heuresticSearch()

'''
what to characterictics heurestic has to be acceptable: acceptance no higher than the actual distance. create simplified problem of cost direct line. can not give higher than that
BFs
if it never overestimates the cost of reaching the goal,
 the cost it estimates to reach the goal is not higher than the lowest possible cost from the current point in the path
'''
