import numpy as np


class SolutionMethod:
    def __init__(self, diffEquation):
        self.diffEquation = diffEquation
        self.h = 0
        self.xPoints = np.array([])
        self.yExactValues = np.array([])
        self.yApproxValues = np.array([])
        self.gte = np.array([])

    def setXPoints(self, x0, X, N):
        self.xPoints = np.array([x0])

        self.h = (X - x0) / N
        for i in range(1, N):
            self.xPoints = np.append(self.xPoints, x0 + self.h * i)

    def calculateYExactValues(self, x0, y0, N):
        self.yExactValues = np.array([y0])

        C = np.exp(-y0 / x0) - x0

        for i in range(1, N):
            self.yExactValues = np.append(self.yExactValues, self.diffEquation.exactSolution(self.xPoints[i], C))

    def calculateGTE(self, N):
        self.gte = np.array([0])

        for i in range(1, N):
            self.gte = np.append(self.gte, np.abs(self.yExactValues[i] - self.yApproxValues[i]))


class EulerMethod(SolutionMethod):
    def __init__(self, diffEquation):
        SolutionMethod.__init__(self, diffEquation)

    def solve(self, x0, y0, X, N):
        self.h = (X - x0) / N
        self.setXPoints(x0, X, N)
        self.calculateYExactValues(x0, y0, N)
        self.calculateYApproxValues(y0, N, self.h)
        self.calculateGTE(N)

    def calculateYApproxValues(self, y0, N, h):
        self.yApproxValues = np.array([y0])

        for i in range(1, N):
            self.yApproxValues = np.append(self.yApproxValues, self.yApproxValues[i - 1] +
                                           h * self.diffEquation.f(self.xPoints[i - 1], self.yApproxValues[i - 1]))


class ImprovedEulerMethod(SolutionMethod):
    def __init__(self, diffEquation):
        SolutionMethod.__init__(self, diffEquation)

    def k1(self, i):
        return self.diffEquation.f(self.xPoints[i], self.yApproxValues[i])

    def k2(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h, self.yApproxValues[i] + self.h * self.k1(i))

    def solve(self, x0, y0, X, N):
        self.h = (X - x0) / N
        self.setXPoints(x0, X, N)
        self.calculateYExactValues(x0, y0, N)
        self.calculateYApproxValues(y0, N, self.h)
        self.calculateGTE(N)

    def calculateYApproxValues(self, y0, N, h):
        self.yApproxValues = np.array([y0])

        for i in range(N - 1):
            self.yApproxValues = np.append(self.yApproxValues,
                                           self.yApproxValues[i] + h / 2 * (self.k1(i) + self.k2(i)))


class RungeKuttaMethod(SolutionMethod):
    def __init__(self, diffEquation):
        SolutionMethod.__init__(self, diffEquation)

    def k1(self, i):
        return self.diffEquation.f(self.xPoints[i], self.yApproxValues[i])

    def k2(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h / 2, self.yApproxValues[i] + self.h / 2 * self.k1(i))

    def k3(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h / 2, self.yApproxValues[i] + self.h / 2 * self.k2(i))

    def k4(self, i):
        return self.diffEquation.f(self.xPoints[i] + self.h, self.yApproxValues[i] + self.h * self.k3(i))

    def solve(self, x0, y0, X, N):
        self.h = (X - x0) / N
        self.setXPoints(x0, X, N)
        self.calculateYExactValues(x0, y0, N)
        self.calculateYApproxValues(y0, N, self.h)
        self.calculateGTE(N)

    def calculateYApproxValues(self, y0, N, h):
        self.yApproxValues = np.array([y0])

        for i in range(N - 1):
            self.yApproxValues = np.append(self.yApproxValues, self.yApproxValues[i] + h / 6 * (self.k1(i) +
                                                                    2 * self.k2(i) + 2 * self.k3(i) + self.k4(i)))
