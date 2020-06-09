import Neuron
import InterfaceGUI
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


defModes = 1
defMeans = [-8, 8]
defVariance = [-1, 1]
defSamples = 10
x_lim = (-10, 10)
y_lim = (-10, 10)

# init
fig, ax = plt.subplots()
ax.set(xlim=x_lim, ylim=y_lim)
plt.subplots_adjust(bottom=0.25)

class1 = InterfaceGUI.Visualization(ax, "ro", defMeans, defSamples, defVariance, defModes)
class1.display_inputs(plt, 0)

class2 = InterfaceGUI.Visualization(ax, "bo", defMeans, defSamples, defVariance, defModes)
class2.display_inputs(plt, 0.45)

neuron = Neuron.Neuron(ax, x_lim, 1)


def heaviside_true_output():
    return np.concatenate((
        np.zeros(class1.samples * class1.modes),
        np.ones(class2.samples * class2.modes)
    ))


def sigmoid_true_output():
    return heaviside_true_output()


def sinus_true_output():
    return np.concatenate((
        np.negative(np.ones(class1.samples * class1.modes)),
        np.ones(class2.samples * class2.modes)
    ))


def tanh_true_output():
    return sinus_true_output()


def sign_true_output():
    return sinus_true_output()


def relu_true_output():
    return np.concatenate((
        np.zeros(class1.samples * class1.modes),
        np.ones(class2.samples * class2.modes)
    ))


def train(_):
    neuron.weights = np.random.uniform(0, 1, 3)
    neuron.train(
        np.concatenate((class1.points, class2.points), axis=0),
        tanh_true_output(), neuron.tanh, neuron.tanh_derivative,
        iterations=400
    )
    neuron.draw()
    plt.draw()


def draw(_):
    class1.draw()
    class2.draw()
    neuron.clear()
    plt.draw()



buttonT = Button(plt.axes((0, 1 - 0.075, 0.1, 0.075)), "train")
buttonT.on_clicked(train)


buttonD = Button(plt.axes((0.1, 1 - 0.075, 0.1, 0.075)), "draw")
buttonD.on_clicked(draw)

plt.show()
