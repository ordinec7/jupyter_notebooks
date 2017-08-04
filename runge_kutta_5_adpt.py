# module run_kut5
""" X,Y = integrate(F,x,y,xStop,h,tol=1.0e-6).
    Adaptive Runge--Kutta method for solving the
    initial value problem {y}' = {F(x,{y})}, where
    {y} = {y[0],y[1],...y[n-1]}.
    x,y   = initial conditions
    xStop = terminal value of x
    h     = initial increment of x used in integration
    tol   = per-step error tolerance
    F     = user-supplied function that returns the
            array F(x,y) = {y'[0],y'[1],...,y'[n-1]}.
"""

from math import sqrt
from numpy import array, sum, zeros, transpose
from progress_bar import ProgressBar


def integrate(F,t,y,tEnd,h,tol=1.0e-6, **opt):
    C = array([37.0/378, 0.0, 250.0/621, 125.0/594, 0.0, 512.0/1771])
    D = array([2825.0/27648, 0.0, 18575.0/48384, 13525.0/55296, 277.0/14336, 1.0/4])
    n = len(y)

    def run_kut5(F,t,y,h):
        # Runge--Kutta-Fehlberg formulas
        K = zeros((6,n))
        K[0] = h*F(t,y)
        K[1] = h*F(t + 1./5*h, y + 1./5*K[0])
        K[2] = h*F(t + 3./10*h, y + 3./40*K[0] + 9./40*K[1])
        K[3] = h*F(t + 3./5*h, y + 3./10*K[0] - 9./10*K[1] + 6./5*K[2])
        K[4] = h*F(t + h, y - 11./54*K[0] + 5./2*K[1] - 70./27*K[2] + 35./27*K[3])
        K[5] = h*F(t + 7./8*h, y + 1631./55296*K[0] + 175./512*K[1] + 575./13824*K[2] + 44275./110592*K[3] + 253./4096*K[4])
        # Initialize arrays {dy} and {E}
        E = zeros(n)
        dy = zeros(n)
        # Compute solution increment {dy} and per-step error {E}
        for i in range(6):
            dy = dy + C[i]*K[i]
            E = E + (C[i] - D[i])*K[i]
        # Compute RMS error e
        e = sqrt(sum(E**2)/n)
        return dy,e

    step = 0.0
    initialStep = 0
    if opt and opt["step"]:
        initialStep = opt["step"]

    pb = opt["pb"] if "pb" in opt else True
    if pb:
        progress = ProgressBar('Runge Kutta 5 Adaptive', t, tEnd)

    T = [t]
    Y = [y]
    tEnd += h * 10
    while t < tEnd:
        dy,e = run_kut5(F,t,y,h)
        # Accept integration step if error e is within tolerance
        if e <= tol:
            y = y + dy
            t = t + h
            if initialStep == 0 or t >= step:
                T.append(t)
                Y.append(y)
            if pb:
                progress.setValue(t)

        # Compute next step size from Eq. (7.24)
        if e != 0.0:
            h = 0.9*h*(tol/e)**0.2

    return array(T), transpose(array(Y))


if __name__ == '__main__':
    print('No testing here')

