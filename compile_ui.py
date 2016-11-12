#!/usr/bin/python3

from PyQt5 import uic


def c(d, f):
    f = f[:-3] + "_ui" + f[-3:]
    return d, f


uic.compileUiDir("ui", map=c)
