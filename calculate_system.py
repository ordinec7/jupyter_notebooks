
from runge_kutta_4 import integrate as rk4
from runge_kutta_5_adpt import integrate as rk5

# import matplotlib.pyplot as plt

from functools import reduce

from numpy import save as np_save
from numpy import load as np_load
from numpy import array

from os import remove as rm

import re


class EquationCalculator(object):

    def __init__(self, func, initial, **arg):
        self.reset_variables()

        self.func = func
        self.initial = initial

        self.method = arg['method'] if ('method' in arg) else 'rk5a'
        self.ignore_cache = arg['ignore_cache'] if 'ignore_cache' in arg else True
        self.time_scale = arg['time_scale'] if 'time_scale' in arg else 1.0
        self.step_size = arg['step_size'] if 'step_size' in arg else 1.0e-6
        self.tolerance = arg['tolerance'] if 'tolerance' in arg else 1.0e-10
        self.tEnd = arg['t_end'] if 't_end' in arg else 50.0
        self.pb = arg['pb'] if 'pb' in arg else True

        if self.func is not None:
            self.generate_cache_name()

    def reset_variables(self):
        self.tStart = 0.0
        self.tEnd = 50.0
        self.step_size = 1.0e-6
        self.tolerance = 1.0e-10

        self.t = None
        self.v = None

    def caclulate(self):
        if self.ignore_cache is False and self.read_cache():
            print("Found cache in '%s'" % self.cache_name)
            return

        if self.method == 'rk5a':
            self.t, self.v = rk5(self.func, self.tStart * self.time_scale, self.initial, self.tEnd * self.time_scale, self.step_size, self.tolerance, step=0.01, pb=self.pb)
        elif self.method == 'rk4':
            self.t, self.v = rk4(self.func, self.tStart * self.time_scale, self.initial, self.tEnd * self.time_scale, self.step_size * 20000.0, step=0.01, pb=self.pb)
        else:
            raise ValueError('Incorrect method name: %s. (Supported: rk5a, rk4).' % self.method)

        self.t = self.t / self.time_scale

        self.save_cache()

    def plot(self, plot, x_name, x, y_name, y, line_opt):
        plot.set_xlabel(x_name)
        plot.set_ylabel(y_name)
        plot.grid(b=True)

        x_arr = self.arr_from_token(x)
        y_arr = self.arr_from_token(y)

        plot.plot(x_arr, y_arr, line_opt)

    def arr_from_token(self, token):
        name, index, start, end = dissasembly_arr_token(token)

        arr = self.t if name is 't' else self.v
        if index is not None:
            arr = arr[index]

        if start < end:
            length = len(arr)
            arr = arr[int(length * start):int(length * end)]

        return arr

    # cache

    def read_cache(self):
        try:
            f = open(self.cache_name, 'rb')
            data = np_load(f)
            f.close()

            if data is not None:
                self.t, self.v = data
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def save_cache(self):
        f = open(self.cache_name, 'wb')
        np_save(f, array([self.t, self.v]))
        f.close()

    def delete_cache(self):
        rm(self.cache_name)

    def generate_cache_name(self):
        def hash(x,y):
            return (29497513917 + x * 275426100873 + y * 71753153873) % 1000000000.0

        value = int(reduce(hash, self.initial))
        self.cache_name = 'cache/eq_cache_' + self.func.__name__ + '_' + self.method + '_'+ str(value)


def dissasembly_arr_token(token, **args):
    match = re.match(r'\.([tv])(\d*)(?:\[([.\d]*):([.\d]*)\])?$', token)

    if match is None:
        return None

    name, index, start, end = match.groups()
    index = int(index) if index is not '' else None
    start = max(0.0, min(1.0, float(start or 0.0)))
    end = max(0.0, min(1.0, float(end or 1.0)))

    if 'output' in args and args['output'] is True:
        print(match)
        print(match.groups() if match is not None else 'No groups')
        print(name, index, start, end)

    return name, index, start, end


if __name__ == '__main__':
    print('Testing dissasembly_arr_token')
    cases = ['.t', '.v', 'sd', 'v[1:0]', '.t[0]', '.t[0:1]', '.v[0.521351:52135]', '.k[ewq4:452s]', '.v[0.7:1]', '.v[:0.0]', '.v2[0.2:0.5]', '.t2']
    for token in cases:
        print('Testing: %s' % token)
        dissasembly_arr_token(token, output=True)
        print(' ')



