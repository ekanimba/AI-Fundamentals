import math
import numpy as np
from neuron import *
import random

class ShallowNetwork:
    
    def __init__(self,noInputs,neuronTable,functionTable, learn_rate):

        self.neuronTable = neuronTable
        self.learn_rate = learn_rate
        self.functionTable = functionTable
        self.network = []
        np.seterr('raise')
        
        for layer in range(len(neuronTable)):
            self.network.append([])
            for node in range(neuronTable[layer]):
                if(layer == 0):
                    w = [random.uniform(0,1) for i in range(noInputs+1)]
                    inp = [1 for i in range(noInputs)]
                    
                    self.network[layer].append(Neuron(inp,functionTable[layer],w,learn_rate))
                else:
                    w = [random.uniform(0,1) for i in range(neuronTable[layer-1]+1)]
                    inp = [1 for i in range(neuronTable[layer-1])]
                    
                    self.network[layer].append(Neuron(inp,functionTable[layer],w,learn_rate))
        

    def setNetworkInput(self,inputTable):
        self.setLayerInputs(inputTable,0)

    def setLayerInputs(self,inputTable,layer):

        for node in self.network[layer]:
            node.setInput(inputTable)

    def getLayerOutputs(self,layer):
        _output = []
        for node in self.network[layer]:
            _output.append(node.calculateOutput(False))
        return _output

    def getNetworkOutput(self,initialInput):
        _outTable = initialInput 
        for layer in range(len(self.neuronTable)):
            self.setLayerInputs(_outTable,layer)
            _outTable = self.getLayerOutputs(layer)
        return _outTable

    def refreshHiddenAndOutputLayer(self):
        for layer in range(len(self.neuronTable)):
            if layer == 0: 
                _outTable = self.getLayerOutputs(layer)
                continue
            self.setLayerInputs(_outTable,layer)
            _outTable = self.getLayerOutputs(layer)
            
    
    def getLayerSums(self,layer):
        _sums = []
        for node in self.network[layer]:
            _sums.append(node.calculateSum())
        return _sums

    def getLayerCorrection(self,layer,errors):
        weights = []
        for i in range(len(self.network[layer])):
            weights.append(self.network[layer][i].calculateCorrection(errors[i]))
        return weights

    def performLayerCorrection(self,layer,errors):
        
        for i in range(len(self.network[layer])):
            self.network[layer][i].performCorrection(errors[i])

    def backPropagate(self,reals):

        layer = len(self.network) - 1
        _currentErr = []
        _previousErr = []
        self.refreshHiddenAndOutputLayer()
        _errors = []
        while(layer >= 0):
            if(layer == len(self.network)-1):
               
                i = 0
                for node in self.network[layer]:
                    _currentErr.append(node.calculateError(reals[i])) 
                    i=+1
        
                _errors.insert(0,_currentErr)
                _previousErr = _currentErr 
                _currentErr = []
                layer -= 1
                continue
            for i in range(len(self.network[layer])):
              
                _nodeError_i = 0
                for j in range(len(self.network[layer+1])):
                    W_ij = self.network[layer+1][j].weights[i+1]
                    derFunc = self.network[layer+1][j].calculateOutput(True)
                    delta_j = _previousErr[j]
                    _nodeError_i += W_ij * derFunc * delta_j 
                _currentErr.append(_nodeError_i)
              
            _errors.insert(0,_currentErr)
            _previousErr = _currentErr
            _currentErr = []
            layer -= 1

        return _errors

    def performNetworkCorrection(self,errors):
       
        layer = len(self.network) - 1
      
        while(layer >= 0):
            for i in range(len(self.network[layer])):
                self.network[layer][i].performCorrection(errors[layer][i])
            layer -= 1

    def getRealValue(self,function,correctXY):
        _reals = [Neuron.getRealValue(correctXY[0],function),
                  Neuron.getRealValue(correctXY[1],function)]
        return _reals

    def train(self,redXY,bluXY,iter):
        redCount = len(redXY[0])
        bluCount = len(bluXY[0])
        loops = 0
        while(True):
   
            for i in range(redCount):
                self.setNetworkInput([redXY[0][i],redXY[1][i]])
                _reals = [Neuron.getRealValue(True,self.functionTable[-1]) for i in range(len(self.network[-1]))] 
                _reals[-1] = Neuron.getRealValue(False,self.functionTable[-1])
                
                _errors = self.backPropagate(_reals)
           
                self.performNetworkCorrection(_errors)
           
            for i in range(bluCount):
                self.setNetworkInput([bluXY[0][i],bluXY[1][i]])
                __reals = [Neuron.getRealValue(True,self.functionTable[-1]) for i in range(len(self.network[-1]))]
                _reals[0] = Neuron.getRealValue(False,self.functionTable[-1])
                
                _errors = self.backPropagate(_reals)
                self.performNetworkCorrection(_errors)
   
            if(loops > iter): break
            loops +=1
        
        return iter
        