import numpy as np


class SolutionMethod:
    def __init__(self, diffEquation, N, x0, y0, X):
        self.diffEquation = diffEquation
        self.N = N
        self.h = (X - x0) / N
        self.x0 = x0
        self.y0 = y0
        self.X = X
        self.xPoints = self.setXPoints()

        self.yExactValues = np.array([y0])
        self.calculateYExactValues()

        self.yApproxValues = np.array([y0])

    def setXPoints(self):
        xPoints = np.array([self.x0])

        for i in range(1, self.N):
            xPoints = np.append(xPoints, self.x0 + self.h * i)

        return xPoints

    def calculateYExactValues(self):
        C = np.exp(-self.y0 / self.x0) - self.x0

        for i in range(1, self.N):
            self.yExactValues = np.append(self.yExactValues, self.diffEquation.exactSolution(self.xPoints[i], C))

    def calculateGTE(self):
        gte = np.array([0])

        for i in range(1, self.N):
            gte = np.append(gte, np.abs(self.yExactValues[i] - self.yApproxValues[i]))

        return gte


class EulerMethod(SolutionMethod):
    def __init__(self, diffEquation, N, x0, y0, X):
        SolutionMethod.__init__(self, diffEquation, N, x0, y0, X)

        self.calculateYApproxValues()

        self.gte = self.calculateGTE()

    def calculateYApproxValues(self):
        for i in range(1, self.N):
            self.yApproxValues = np.append(self.yApproxValues, self.yApproxValues[i - 1] +
                                           self.h * self.diffEquation.f(self.xPoints[i - 1], self.yApproxValues[i - 1]))


class ImprovedEulerMethod(SolutionMethod):
    def __init__(self, diffEquation, N, x0, y0, X):
        SolutionMethod.__init__(self, diffEquation, N, x0, y0, X)

        self.calculateYApproxValues()

        self.gte = self.calculateGTE()

    def k1(self, i):
        return self.diffEquation.f(self.xPoints[i], self.yApproxValues[i])

    def k2(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h, self.yApproxValues[i] + self.h * self.k1(i))

    def calculateYApproxValues(self):
        for i in range(self.N - 1):
            self.yApproxValues = np.append(self.yApproxValues,
                                           self.yApproxValues[i] + self.h / 2 * (self.k1(i) + self.k2(i)))


class RungeKuttaMethod(SolutionMethod):
    def __init__(self, diffEquation, N, x0, y0, X):
        SolutionMethod.__init__(self, diffEquation, N, x0, y0, X)

        self.calculateYApproxValues()

        self.gte = self.calculateGTE()

    def k1(self, i):
        return self.diffEquation.f(self.xPoints[i], self.yApproxValues[i])

    def k2(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h / 2, self.yApproxValues[i] + self.h / 2 * self.k1(i))

    def k3(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h / 2, self.yApproxValues[i] + self.h / 2 * self.k2(i))

    def k4(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h, self.yApproxValues[i] + self.h * self.k3(i))

    def calculateYApproxValues(self):
        for i in range(self.N - 1):
            self.yApproxValues = np.append(self.yApproxValues, self.yApproxValues[i] + self.h / 6 * (self.k1(i) +
                                                                2 * self.k2(i) + 2 * self.k3(i) + self.k4(i)))
