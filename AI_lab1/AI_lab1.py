
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox,Button
import itertools


fig, ax = [],[]
RED_COLOR = 0
BLUE_COLOR = 1
color_type = ('ro','bo')
samples = [500,500]
mean = [[[-5,-5],[5,5]],[[10,10],[-10,-10]]]
cov = [[[[1, 2], [0.5, 2]],[[1, 2], [0.5, 2]]],[[[1, 0.3], [2, 0.5]],[[1, 2], [5, 6]]]]
dataClass = []
classesNo = [1,1]
meanRange = [-100,100]
covRange = (-2,2)

def draw(ID):
    global mean
    global cov
    global samples
    global dataClass
    global classesNo
    x,y = [],[]
    for i in range(classesNo[ID]):
        print(cov)
        print(cov[ID][i])
        _x,_y = np.random.multivariate_normal(mean[ID][i], cov[ID][i], samples[ID]).T
        x.extend(_x)
        y.extend(_y)
    print (len(x),len(y))
    return plt.plot(x, y, color_type[ID])

def initsRegenerate(ID):
    global mean
    global cov
    mean.pop(ID)
    mean.insert(ID,[])
    cov.pop(ID)
    cov.insert(ID,[])
    for i in range(classesNo[ID]):
        mean[ID].insert(i,randomMultivariateMean(meanRange[0],meanRange[1]))
        cov[ID].insert(i,randomCov(covRange[0],covRange[1]))

def randomMultivariateMean(_min,_max):
    newmean = np.random.uniform(_min,_max,2)
    return [newmean[0],newmean[1]]

def randomCov(_min,_max):
    x,y = [],[]
    x = np.random.uniform(_min,_max,2)
    y = np.random.uniform(_min,_max,2)
    covariance = [[x[0],x[1]],[y[0],y[1]]]
    return covariance

def plotDataUpdate(ID):
    x,y = [],[]
    global classesNo
    global mean
    global cov
    global samples
    global dataClass
    try:
        for i in range(classesNo[ID]):
            _x,_y = np.random.multivariate_normal(mean[ID][i], cov[ID][i], samples[ID]).T
            x.extend(_x)
            y.extend(_y)
    except:
        print("Incorrect data input!")
    dataClass[ID][0].set_xdata(x)
    dataClass[ID][0].set_ydata(y)
    ax.relim()
    ax.autoscale_view()
    plt.draw()



def initPlots():
    global fig,ax
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.29)
    plt.autoscale(enable=True, axis='both', tight=True)
    initsRegenerate(RED_COLOR)
    initsRegenerate(BLUE_COLOR)
    return fig,ax
    
class Index(object):
    ind = 0
    def REDregenerate(self,event):
        self.ind +=1
        initsRegenerate(RED_COLOR)
        plotDataUpdate(RED_COLOR)
    def BLUEregenerate(self,event):
        self.ind -=1
        initsRegenerate(BLUE_COLOR)
        plotDataUpdate(BLUE_COLOR)

def initUserInterface():
    
    RED_boxAxis = plt.axes([0.15, 0.05, 0.32, 0.05])
    RED_sampleBoxAxis = plt.axes([0.15, 0.11, 0.32, 0.05])
    BLUE_boxAxis = plt.axes([0.61, 0.05, 0.32, 0.05])
    BLUE_sampleBoxAxis = plt.axes([0.61, 0.11, 0.32, 0.05])
    meanBoxAxis = plt.axes([0.4, 0.17, 0.32, 0.05])
   
    RED_axButton = plt.axes([0.15, 0.17, 0.15, 0.05])
    BLUE_axButton = plt.axes([0.78, 0.17, 0.15, 0.05])

    RED_button = Button(RED_axButton, 'Regen Red',color = 'red')
    BLUE_button = Button(BLUE_axButton, 'Regen Blue',color = 'blue')

    
    RED_textBox = TextBox(RED_boxAxis, 'Modes\nRED', initial=str(classesNo[RED_COLOR]))
    RED_textBox.label.set_wrap(True)
    meantextBox = TextBox(meanBoxAxis, 'Mean\nRange', initial=str(meanRange))
    meantextBox.label.set_wrap(True)
    RED_sampletextBox = TextBox(RED_sampleBoxAxis, 'Samples\nRED', initial=str(samples[RED_COLOR]))
    RED_sampletextBox.label.set_wrap(True)
    BLUE_textBox = TextBox(BLUE_boxAxis, 'Modes\nBLUE', initial=str(classesNo[BLUE_COLOR]))
    BLUE_textBox.label.set_wrap(True)
    BLUE_sampletextBox = TextBox(BLUE_sampleBoxAxis, 'Samples\nBLUE', initial=str(samples[BLUE_COLOR]))
    BLUE_sampletextBox.label.set_wrap(True)

    RED_textBox.on_submit(lambda value: updateNewNo(RED_COLOR,RED_textBox.text))
    BLUE_textBox.on_submit(lambda value: updateNewNo(BLUE_COLOR,BLUE_textBox.text))
    meantextBox.on_submit(lambda value: updateNewMean(meantextBox.text))
    RED_sampletextBox.on_submit(lambda value: updateNewSamples(RED_COLOR,RED_sampletextBox.text))
    BLUE_sampletextBox.on_submit(lambda value: updateNewSamples(BLUE_COLOR,BLUE_sampletextBox.text))
    callback = Index()
    RED_button.on_clicked(callback.REDregenerate)
    BLUE_button.on_clicked(callback.BLUEregenerate)
    plt.show()
    return callback,RED_button,BLUE_button

def updateNewNo(ID, input):
    newNo = 0
    global classesNo
    try:
        newNo = int(input)
        classesNo[ID] = newNo
    except:
        print("Error!")
    initsRegenerate(ID)
    
def updateNewMean(input):
    newMeanRange = [0,0]
    global meanRange
    try:
        newMeanRange = eval(input)
        meanRange = newMeanRange
    except:
        print("Error!")
    initsRegenerate(BLUE_COLOR)
    initsRegenerate(RED_COLOR)
    
    
def updateNewSamples(ID, input):
    newSamples = 1
    global samples
    try:
        newSamples = int(input)
        samples[ID] = newSamples
    except:
        print("Error!")

    
if __name__ == '__main__':
    initPlots()
    dataClass = [draw(RED_COLOR),draw(BLUE_COLOR)]
    initUserInterface()
    plt.show()
