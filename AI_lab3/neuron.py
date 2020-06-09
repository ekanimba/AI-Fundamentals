
import math
import numpy as np

class Neuron:
    def __init__(self,_input,act_func, weights, learn_rate):
        self.inputs = _input
        self.act_func = act_func
        self.weights = weights
        self.learn_rate = learn_rate
    
    def setInput(self,_input):
        self.inputs = _input
    
    def setWeight(self,weights):
        self.weights = weights
    
    def setLearnRate(self,learn_rate):
        self.learn_rate = learn_rate
    def setActivationFunction(self,new_func):
        self.act_func = new_func

    def step_func(s,isDerivative):
        if(isDerivative):
            return 1
        else:
            return 0 if s< 0 else 1

    def sig_func(s,isDerivative):
        base = 1/(1+math.exp(-s))
        if(isDerivative):
            return base*(1-base)
        else:
            return base

    def sin_func(s,isDerivative):
        if(isDerivative):
            return math.cos(s)
        else:
            return math.sin(s)

    def tanh_func(s,isDerivative):
        if(isDerivative):
            return 1-(math.tanh(s)**2)
        else:
            return math.tanh(s)

    def sign_func(s,isDerivative):
        result = 1
        if(isDerivative):
            return result
        else:
            result = -1 if s<0  else 1
            return result

    def relu_func(s,isDerivative):
        if(isDerivative):
            return 1 if s> 0 else 0
        else:
            return s if s> 0 else 0

    def leaky_relu_func(s,isDerivative):
        if(isDerivative):
            return 1 if s> 0 else 0.01
        else:
            return s if s> 0 else 0.01

    Functions = {
        "step_func": step_func,
        "sig_func":sig_func,
        "sin_func":sin_func,
        "tanh_func":tanh_func,
        "sign_func":sign_func,
        "relu_func":relu_func,
        "leaky_func":leaky_relu_func
    }

    def calculateSum(self):
        _sum = np.dot(self.inputs,self.weights[1:])
        return _sum

    def calculateValue(self,isDerivative,val):
        out = Neuron.Functions[self.act_func](val,isDerivative)
        return out

    def calculateOutput(self,isDerivative):
        s = self.calculateSum() + self.weights[0]
        out = Neuron.Functions[self.act_func](s,isDerivative)
        return out

    def calculateError(self,real):
        return (real - self.calculateOutput(False))#(d-y)

    def calculateCorrection(self,error):
        #  ∆wj = η(d−y)f′(wTxj)xj
        fPrime = self.calculateOutput(True) #f'(wTxj)
        correction = []
        correction.append(self.learn_rate * error * self.calculateOutput(True) * 1.0)#for bias
        for element in self.inputs:
            correction.append(self.learn_rate * error * self.calculateOutput(True) * element)
        #returns table of ∆wj-corrections per weight
        return correction

    def performCorrection(self,error):
        correction = self.calculateCorrection(error)
        w = self.weights
        for i in range(len(w)):
            w[i] += correction[i]
        self.setWeight(w)
        
    def getRealValue(isDataCorrect,function):
        if function == ("step_func")\
            or function == ("sig_func")\
            or function == ("sin_func")\
            or function == ("relu_func")\
            or function == ("leaky_func"):
            return 1 if isDataCorrect else 0
        elif function == ("tanh_func")\
            or function == ("sign_func"):
            return 1 if isDataCorrect else -1
        
    def isAccurate(self, side1,side2):
        self.setInput(side1)
        result1 = self.calculateOutput(False)
        self.setInput(side2)
        result2 = self.calculateOutput(False)
        return result1 > result2

    def train(self, redXY,blueXY, treshold):
        loops = 0
        while(True):
            loops += 1
            acc = 0
            for i in range(len(redXY[0])):
                _side1 = [redXY[0][i],redXY[1][i]]
                _side2 = [blueXY[0][i],blueXY[1][i]]
                self.setInput(_side1)
                real = Neuron.getRealValue(True,self.act_func)
                self.performCorrection(self.calculateError(real))
                self.setInput(_side2)
                real = Neuron.getRealValue(False,self.act_func)
                self.performCorrection(self.calculateError(real))
                if self.isAccurate(_side1,_side2): acc+=1
            if ((loops) > 1000) or (acc == 100): 
                print("accuracy: ",acc,"  on: ",self.act_func)
                print("new w",self.weights)
                break
        return loops
