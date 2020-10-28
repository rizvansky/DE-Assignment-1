from PyQt5 import QtWidgets
from helper_widgets import GraphsTabWidget, OptionsWidget
import numpy as np
from methods import EulerMethod, ImprovedEulerMethod, RungeKuttaMethod


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self, euler, improvedEuler, rungeKutta):
        super(ApplicationWindow, self).__init__()

        self.euler = euler
        self.improvedEuler = improvedEuler
        self.rungeKutta = rungeKutta

        self.graphsTabWidget = GraphsTabWidget(self)

        self.optionsWidget = OptionsWidget(self)
        self.optionsWidget.plotButton.clicked.connect(self.plotGraphs)
        self.optionsWidget.methodsCheckboxesWidget.checkboxExact.stateChanged.connect(self.plotGraphs)
        self.optionsWidget.methodsCheckboxesWidget.checkboxEuler.stateChanged.connect(self.plotGraphs)
        self.optionsWidget.methodsCheckboxesWidget.checkboxImprovedEuler.stateChanged.connect(self.plotGraphs)
        self.optionsWidget.methodsCheckboxesWidget.checkboxRungeKutta.stateChanged.connect(self.plotGraphs)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.graphsTabWidget)
        self.mainLayout.addWidget(self.optionsWidget)
        self.mainWidget = QtWidgets.QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.plotGraphs()

    def updateSolutions(self):
        N = int(self.optionsWidget.parametersWidget.parametersValuesWidget.valueN.text())
        x0 = int(self.optionsWidget.parametersWidget.parametersValuesWidget.valueX0.text())
        y0 = int(self.optionsWidget.parametersWidget.parametersValuesWidget.valueY0.text())
        X = int(self.optionsWidget.parametersWidget.parametersValuesWidget.valueX.text())
        diffEquation = self.euler.diffEquation

        self.euler = EulerMethod(diffEquation, N, x0, y0, X)
        self.improvedEuler = ImprovedEulerMethod(diffEquation, N, x0, y0, X)
        self.rungeKutta = RungeKuttaMethod(diffEquation, N, x0, y0, X)

    def setGraph(self, axes, xPoints, yValues, gte, gteMax, nPoints, color, name):
        axes['solutions'].plot(xPoints, yValues, color, label=name)
        axes['solutions'].legend()
        axes['solutions'].set_xlabel('x')
        axes['solutions'].set_ylabel('y')

        axes['gte'].plot(xPoints, gte, color, label=name)
        axes['gte'].legend()
        axes['gte'].set_xlabel('x')
        axes['gte'].set_ylabel('GTE')

        axes['gteMax'].plot(nPoints, gteMax, color, label=name)
        axes['gteMax'].legend()
        axes['gteMax'].set_xlabel('x')
        axes['gteMax'].set_ylabel('GTE Max')

    def plotGraphs(self):
        self.graphsTabWidget.solutionsGraphs.clear()
        self.graphsTabWidget.gteGraphs.clear()
        self.graphsTabWidget.gteMaxGraphs.clear()

        self.updateSolutions()

        axes = {
            'solutions': self.graphsTabWidget.solutionsGraphs.add_subplot(111),
            'gte': self.graphsTabWidget.gteGraphs.add_subplot(111),
            'gteMax': self.graphsTabWidget.gteMaxGraphs.add_subplot(111)
        }

        gteMaxEuler, gteMaxImprovedEuler, gteMaxRungeKutta, nPoints = self.calculateGteMax()

        xPoints = self.euler.xPoints
        if self.optionsWidget.methodsCheckboxesWidget.checkboxExact.isChecked():
            self.setGraph(axes, xPoints, self.euler.yExactValues, np.zeros(shape=[len(self.euler.xPoints)]),
                          np.zeros(shape=[len(nPoints)]), nPoints, 'c', 'Exact')

        if self.optionsWidget.methodsCheckboxesWidget.checkboxEuler.isChecked():
            self.setGraph(axes, xPoints, self.euler.yApproxValues, self.euler.gte, gteMaxEuler, nPoints, 'b',
                          'Euler')

        if self.optionsWidget.methodsCheckboxesWidget.checkboxImprovedEuler.isChecked():
            self.setGraph(axes, xPoints, self.improvedEuler.yApproxValues, self.improvedEuler.gte,
                          gteMaxImprovedEuler, nPoints, 'r', 'Improved Euler')

        if self.optionsWidget.methodsCheckboxesWidget.checkboxRungeKutta.isChecked():
            self.setGraph(axes, xPoints, self.rungeKutta.yApproxValues, self.rungeKutta.gte,
                          gteMaxRungeKutta, nPoints, 'm', 'Runge-Kutta')

        self.graphsTabWidget.solutionsCanvas.draw()
        self.graphsTabWidget.gteCanvas.draw()
        self.graphsTabWidget.gteMaxCanvas.draw()

    def calculateGteMax(self):
        diffEquation = self.euler.diffEquation
        n0 = int(self.optionsWidget.parametersWidget.parametersValuesWidget.valueN0.text())
        nMax = int(self.optionsWidget.parametersWidget.parametersValuesWidget.valueNMax.text())

        gteMaxEuler = np.array([])
        gteMaxImprovedEuler = np.array([])
        gteMaxRungeKutta = np.array([])
        nPoints = range(n0, nMax + 1)

        for N in nPoints:
            euler = EulerMethod(diffEquation, N, self.euler.x0, self.euler.y0, self.euler.X)
            improvedEuler = ImprovedEulerMethod(diffEquation, N, self.euler.x0, self.euler.y0, self.euler.X)
            rungeKutta = RungeKuttaMethod(diffEquation, N, self.euler.x0, self.euler.y0, self.euler.X)

            gteMaxEuler = np.append(gteMaxEuler, np.max(euler.gte))
            gteMaxImprovedEuler = np.append(gteMaxImprovedEuler, np.max(improvedEuler.gte))
            gteMaxRungeKutta = np.append(gteMaxRungeKutta, np.max(rungeKutta.gte))

        return gteMaxEuler, gteMaxImprovedEuler, gteMaxRungeKutta, nPoints
