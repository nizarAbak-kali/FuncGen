#!/usr/bin/python

# -*- coding: <utf-8> -*-

from function import Function

class Affine(Function):

    def __init__(self, a=0, b=0, nom="affine"):
        Function.__init__(nom, a, b)

    def __str__(self):
        str = "def {2}_{0}_{1}(x): \n" \
              "    return {0}*x+{1} \n" \
              "{2}_{0}_{1}(x)".format(self.a,self.b,self.name)
        return str