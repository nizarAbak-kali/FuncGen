#!/usr/bin/python

# -*- coding: <utf-8> -*-

from function import Function


class Lineaire(Function):

    def __init__(self, a=0, nom="lineaire"):
        Function.__init__(nom, a)
        self.name = nom
        self.a = a

    def __str__(self):
        str = "def {1}_{0}(x): \n" \
              "\t return {0}*x \n".format(self.a,self.name)
        return str