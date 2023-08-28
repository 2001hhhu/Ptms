import numpy as np
import matplotlib.pyplot as plt
import time
from math import *

plt.ion()

class chart_1:

    def __init__(self):
        self.x_1 = []
        self.y_1 = []
        self.ax = plt.figure(1)
        self.t = [0]
        self.t_now = 0
        self.m = [sin(self.t_now)]



    def show(self):
        for i in range(200):
            self.t_now = i * 0.1
            self.t.append(self.t_now)
            self.m.append(sin(self.t_now))
            plt.plot(self.t,self.m,'-r')
            plt.pause(0.1)


# if __name__ == '__main__':
#     chart = chart_1()
#     chart.show()
