#!/usr/bin/python
# -*- coding: utf-8 -*-

# class pour definir de maniere generale une fonctiton

class Function():
    def __init__(self, name="toto", a=0 ,b=0):
        self.name=name
        self.a = a
        self.b = b
    def get_name(self):
        return self.name
    def get_a(self):
        return self.a
    def get_b(self):
        return self.b

    def set_name(self, name):
        self.name = name
    def set_a(self, a):
        self.a = a
    def set_b(self, b):
        self.b = b