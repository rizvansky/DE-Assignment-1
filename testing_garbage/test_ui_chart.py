from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar


class SolverApplication(QtWidgets.QMainWindow):
    def __init__(self):
        super(SolverApplication, self).__init__()

        self.table_widget = MyTableWidget(self)
        layout.addWidget(self.table_widget)

        self.setObjectName("MainWindow")
        self.resize(1024, 768)

        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")

        self.chart = QtWidgets.QLabel(self.centralWidget)
        self.chart.setGeometry(QtCore.QRect(110, 50, 761, 461))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.chart.setFont(font)
        self.chart.setText("")
        self.chart.setPixmap(QtGui.QPixmap("../../../wallpapers/nebula_purple.jpg"))
        self.chart.setScaledContents(True)
        self.chart.setObjectName("chart")

        self.showChartButton = QtWidgets.QPushButton(self.centralWidget)
        self.showChartButton.setGeometry(QtCore.QRect(240, 610, 511, 101))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.showChartButton.setFont(font)
        self.showChartButton.setObjectName("showChartButton")
        self.setCentralWidget(self.centralWidget)

        self.menuBar = QtWidgets.QMenuBar(self)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1020, 30))
        self.menuBar.setObjectName("menuBar")
        self.menuFile = QtWidgets.QMenu(self.menuBar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName("menuEdit")
        self.setMenuBar(self.menuBar)

        self.statusBar = QtWidgets.QStatusBar(self)
        self.statusBar.setObjectName("statusBar")
        self.setStatusBar(self.statusBar)

        self.actionNew = QtWidgets.QAction(self)
        self.actionNew.setObjectName("actionNew")
        self.actionSave = QtWidgets.QAction(self)
        self.actionSave.setObjectName("actionSave")
        self.actionCopy = QtWidgets.QAction(self)
        self.actionCopy.setObjectName("actionCopy")
        self.actionPaste = QtWidgets.QAction(self)
        self.actionPaste.setObjectName("actionPaste")

        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionSave)
        self.menuEdit.addAction(self.actionCopy)
        self.menuEdit.addAction(self.actionPaste)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.showChartButton.clicked.connect(self.showChart)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.showChartButton.setText(_translate("MainWindow", "Show chart"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Create a new file"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setStatusTip(_translate("MainWindow", "Save a file"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setStatusTip(_translate("MainWindow", "Copy"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionPaste.setText(_translate("MainWindow", "Paste"))
        self.actionPaste.setStatusTip(_translate("MainWindow", "Paste"))

    def createChart(self):
        directory = 'charts'
        chartName = 'plot1.jpg'
        savePath = os.path.join(directory, chartName)

        a = np.random.randint(low=-5, high=25, size=[32])
        plt.figure()
        plt.plot(a)
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.savefig(savePath)
        return savePath

    def showChart(self):
        self.chart.setPixmap(QtGui.QPixmap(self.createChart()))


class MyTableWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super(QtWidgets.QWidget, self).__init__(parent)
        # colours for the methods in the graph
        self.colours = ['b-', 'g-', 'r-', 'k-']
        # initialize the figures for the graphs
        figure1 = plt.figure()
        figure2 = plt.figure()
        figure3 = plt.figure()
        self.figures = [figure1, figure2, figure3]
        # the layout for graphs
        layout = QtWidgets.QVBoxLayout(self)
        # the tab widget for the tabs
        tabs = QtWidgets.QTabWidget()
        # initialization of tabs
        tab_solutions = QtWidgets.QWidget()
        tab_LTE = QtWidgets.QWidget()
        tab_GTE = QtWidgets.QWidget()
        # resize the tab widget
        tabs.resize(300, 200)
        # add tabs to the tab widget
        tabs.addTab(tab_solutions, "Solutions")
        tabs.addTab(tab_LTE, "LTE")
        tabs.addTab(tab_GTE, "GTE")
        # create the Box Layout for the tab with the solutions
        tab_solutions.layout = QtWidgets.QVBoxLayout(self)
        # create the canvas the figure of the solutions renders into
        self.canvas_solutions = FigureCanvasQTAgg(figure1)
        # add the canvas and the toolbar to the layout of the tab with the solutions
        tab_solutions.layout.addWidget(NavigationToolbar(self.canvas_solutions, self))
        tab_solutions.layout.addWidget(self.canvas_solutions)
        # set the layout for the tab with the solutions
        tab_solutions.setLayout(tab_solutions.layout)
        # create Box Layout for the tab with the LTE
        tab_LTE.layout = QtWidgets.QVBoxLayout(self)
        # create the canvas the figure with the LTE renders into
        self.canvas_LTE = FigureCanvasQTAgg(figure2)
        # add the canvas and the toolbar to the layout of the tab with the LTE
        tab_LTE.layout.addWidget(NavigationToolbar(self.canvas_LTE, self))
        tab_LTE.layout.addWidget(self.canvas_LTE)
        # set the layout for the tab with the LTE
        tab_LTE.setLayout(tab_LTE.layout)
        # create Box Layout for the tab with the change of the GTE maximum
        tab_GTE.layout = QtWidgets.QVBoxLayout(self)
        # create the canvas the figure with the change of the GTE maximum renders into
        self.canvas_GTE = FigureCanvasQTAgg(figure3)
        # add the canvas and the toolbar to the layout of the tab with the change of the GTE maximum
        tab_GTE.layout.addWidget(NavigationToolbar(self.canvas_GTE, self))
        tab_GTE.layout.addWidget(self.canvas_GTE)
        # set the layout for the tab with the the change of the GTE maximum
        tab_GTE.setLayout(tab_GTE.layout)
        # add the tabs to the general layout
        layout.addWidget(tabs)
        # set layout for the class
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    solverWindow = SolverApplication()
    solverWindow.show()
    sys.exit(app.exec_())
