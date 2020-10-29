from equation import DifferentialEquation
from methods import EulerMethod, ImprovedEulerMethod, RungeKuttaMethod
from app_window import ApplicationWindow
from PyQt5 import QtWidgets
import sys
import numpy as np


def f(x, y):
    return y / x - x * np.exp(y / x)


def exactSolution(x, C):
    return -x * np.log(x + C)


if __name__ == "__main__":
    diffEq = DifferentialEquation(f=f, exactSolution=exactSolution)
    euler = EulerMethod(diffEquation=diffEq)
    improvedEuler = ImprovedEulerMethod(diffEquation=diffEq)
    rungeKutta = RungeKuttaMethod(diffEquation=diffEq)

    app = QtWidgets.QApplication(sys.argv)
    solverWindow = ApplicationWindow(euler, improvedEuler, rungeKutta)
    solverWindow.show()
    sys.exit(app.exec_())
