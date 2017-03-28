#!/usr/bin/python
# -*- coding: <utf-8> -*-
#import funType
from funType import Lineaire

import time

from funType.AffineFunc import Affine
from funType.Lineaire import Lineaire

N = 0

class Generator:

    def __init__(self):
        self.list = []


    # fonction pour demander poliment a puis on genere
    def ask(self):
        while 1 :
            val = input("Entrez a (q to quit):")
            self.list.append(val)
            print val
    def write_code(self, func):
        print str(func)


if __name__ == '__main__':
    gene = Generator()
    line = Lineaire()

    gene.ask()
