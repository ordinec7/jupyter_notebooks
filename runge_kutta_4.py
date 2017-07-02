
# module run_kut4
""" X,Y = integrate(F,x,y,xStop,h).
    4th-order Runge--Kutta method for solving the
    initial value problem {y}' = {F(x,{y})}, where
        {y}     = {y[0],y[1],...y[n-1]}.
        x, y    = initial conditions.
        xStop   = terminal value of x.
        h       = increment of x used in integration.
        F       = user-supplied function that returns the
                array F(x,y) = {y'[0],y'[1],...,y'[n-1]}.
"""

from numpy import array, transpose
from progress_bar import ProgressBar


def integrate(F,t,y,tEnd,h, **opt):
    def run_kut4(F,t,y,h):
        K0 = h*F(t,y)
        K1 = h*F(t + h/2.0, y + K0/2.0)
        K2 = h*F(t + h/2.0, y + K1/2.0)
        K3 = h*F(t + h, y + K2)
        return (K0 + 2.0*K1 + 2.0*K2 + K3)/6.0

    step = 0
    initialStep = 0
    if opt and opt["step"]:
        initialStep = opt["step"]

    T = [t]
    Y = [y]
    progress = ProgressBar('Runge Kutta 4', t, tEnd)
    while t < tEnd:
        y = y + run_kut4(F,t,y,h)
        t = t + h
        if initialStep == 0 or t >= step:
            T.append(t)
            Y.append(y)
            step += initialStep

        progress.setValue(t)
    return array(T), transpose(array(Y))





