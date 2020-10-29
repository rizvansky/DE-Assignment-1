from PyQt5 import QtWidgets, QtGui
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT


class GraphsTabWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(GraphsTabWidget, self).__init__(parent)

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.solutionsPageWidget = QtWidgets.QWidget()
        self.gtePageWidget = QtWidgets.QWidget()
        self.gteMaxPageWidget = QtWidgets.QWidget()

        self.solutionsGraphs = plt.figure(1)
        self.solutionsCanvas = FigureCanvasQTAgg(self.solutionsGraphs)
        self.solutionsToolbar = NavigationToolbar2QT(self.solutionsCanvas, self)

        self.gteGraphs = plt.figure(2)
        self.gteCanvas = FigureCanvasQTAgg(self.gteGraphs)
        self.gteToolbar = NavigationToolbar2QT(self.gteCanvas, self)

        self.gteMaxGraphs = plt.figure(3)
        self.gteMaxCanvas = FigureCanvasQTAgg(self.gteMaxGraphs)
        self.gteMaxToolbar = NavigationToolbar2QT(self.gteMaxCanvas, self)

        self.tabWidget = QtWidgets.QTabWidget()
        self.setTabWidget()

        self.mainLayout.addWidget(self.tabWidget)
        self.setLayout(self.mainLayout)

    def setTabWidget(self):
        solutionsPageLayout = QtWidgets.QVBoxLayout()
        solutionsPageLayout.addWidget(self.solutionsToolbar)
        solutionsPageLayout.addWidget(self.solutionsCanvas)
        self.solutionsPageWidget.setLayout(solutionsPageLayout)

        gtePageLayout = QtWidgets.QVBoxLayout()
        gtePageLayout.addWidget(self.gteToolbar)
        gtePageLayout.addWidget(self.gteCanvas)
        self.gtePageWidget.setLayout(gtePageLayout)

        gteMaxPageLayout = QtWidgets.QVBoxLayout()
        gteMaxPageLayout.addWidget(self.gteMaxToolbar)
        gteMaxPageLayout.addWidget(self.gteMaxCanvas)
        self.gteMaxPageWidget.setLayout(gteMaxPageLayout)

        self.tabWidget.resize(800, 600)
        self.tabWidget.addTab(self.solutionsPageWidget, "Solution graphs")
        self.tabWidget.addTab(self.gtePageWidget, "Local errors")
        self.tabWidget.addTab(self.gteMaxPageWidget, "Max GTE graphs")


class ParametersNamesWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ParametersNamesWidget, self).__init__(parent)

        self.labelX0 = QtWidgets.QLabel('x0')
        self.labelX = QtWidgets.QLabel('X')
        self.labelY0 = QtWidgets.QLabel('y0')
        self.labelN = QtWidgets.QLabel('n')
        self.labelN0 = QtWidgets.QLabel('N0')
        self.labelNMax = QtWidgets.QLabel('N Max')

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.labelX0)
        self.mainLayout.addWidget(self.labelX)
        self.mainLayout.addWidget(self.labelY0)
        self.mainLayout.addWidget(self.labelN)
        self.mainLayout.addWidget(self.labelN0)
        self.mainLayout.addWidget(self.labelNMax)
        self.setLayout(self.mainLayout)


class ParametersValuesWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ParametersValuesWidget, self).__init__(parent)

        self.valueX0 = QtWidgets.QLineEdit('1')
        self.valueX = QtWidgets.QLineEdit('8')
        self.valueY0 = QtWidgets.QLineEdit('0')
        self.valueN = QtWidgets.QLineEdit('70')
        self.valueN0 = QtWidgets.QLineEdit('10')
        self.valueNMax = QtWidgets.QLineEdit('100')

        self.valueX0.setValidator(QtGui.QIntValidator())
        self.valueX.setValidator(QtGui.QIntValidator())
        self.valueY0.setValidator(QtGui.QIntValidator())
        self.valueN.setValidator(QtGui.QIntValidator())
        self.valueN0.setValidator(QtGui.QIntValidator())
        self.valueNMax.setValidator(QtGui.QIntValidator())

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.valueX0)
        self.mainLayout.addWidget(self.valueX)
        self.mainLayout.addWidget(self.valueY0)
        self.mainLayout.addWidget(self.valueN)
        self.mainLayout.addWidget(self.valueN0)
        self.mainLayout.addWidget(self.valueNMax)
        self.setLayout(self.mainLayout)


class ParametersWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(ParametersWidget, self).__init__(parent)

        self.parametersNamesWidget = ParametersNamesWidget(self)
        self.parametersValuesWidget = ParametersValuesWidget(self)

        self.mainLayout = QtWidgets.QHBoxLayout()
        self.mainLayout.addWidget(self.parametersNamesWidget)
        self.mainLayout.addWidget(self.parametersValuesWidget)
        self.setLayout(self.mainLayout)


class MethodsCheckboxesWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(MethodsCheckboxesWidget, self).__init__(parent)

        self.checkboxExact = QtWidgets.QCheckBox('Exact')
        self.checkboxEuler = QtWidgets.QCheckBox('Euler')
        self.checkboxImprovedEuler = QtWidgets.QCheckBox('ImprovedEuler')
        self.checkboxRungeKutta = QtWidgets.QCheckBox('RungeKutta')

        self.checkboxExact.setChecked(True)
        self.checkboxEuler.setChecked(True)
        self.checkboxImprovedEuler.setChecked(True)
        self.checkboxRungeKutta.setChecked(True)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.checkboxExact)
        self.mainLayout.addWidget(self.checkboxEuler)
        self.mainLayout.addWidget(self.checkboxImprovedEuler)
        self.mainLayout.addWidget(self.checkboxRungeKutta)
        self.setLayout(self.mainLayout)


class OptionsWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(OptionsWidget, self).__init__(parent)

        self.parametersWidget = ParametersWidget(self)
        self.methodsCheckboxesWidget = MethodsCheckboxesWidget(self)
        self.plotButton = QtWidgets.QPushButton('Plot solutions')

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addWidget(self.parametersWidget)
        self.mainLayout.addWidget(self.methodsCheckboxesWidget)
        self.mainLayout.addWidget(self.plotButton)

        self.setLayout(self.mainLayout)
        self.setFixedWidth(200)
