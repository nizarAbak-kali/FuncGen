#!/usr/bin/python
# coding=utf-8
#import funType
from user import home

from funType import Lineaire
import time
from funType.AffineFunc import Affine
from funType.Lineaire import Lineaire
import os
import sqlite3
import importlib

##https://stackoverflow.com/questions/301134/dynamic-module-import-in-python

## https://stamat.wordpress.com/2013/06/30/dynamic-module-import-in-python/
"""
Je voudrais un code C_01 comme ceci :

    L=[]
    condi = 1
    N=0

    while condi = 1 repeat :
          "Entrez a :"
              L.append(a)
              N=N+1
                Générer un code  Code_a_N.py qui définit f_a(x) = a*x, et qu'on enregistre dans le dossier   /Documents/Juju
                  voulez-vous continuez ? Si oui condi = 1, si non condi = 0

          "Entrez b:"
                Si b est dans L, au numéro n,
                    import Code_b_n
                    print "pour ce b on peut bien calculer f_b(2), qui vaut",  Code_b_n.f_b(2)
                Sinon (si b n'est pas dans L), print "ce f_b n'est pas encore défini"


"""

home = os.path.expanduser("~")
function_folder = os.path.dirname("function_generated/")
print function_folder



class Generator:

    def __init__(self):
        self.list = []

    # fonction pour demander poliment a puis on genere
    def ask(self):

        while 1 :
            val = raw_input("Entrez a (q to quit):")
            if str(val) == "q":
                break
            else:
                self.list.append(val)
                lin = Lineaire(val)
                self.write_code(lin)
            print val

        while 1 :
            val = raw_input("Entrez b (q to quit):")
            if str(val) == "q":
                exit(0)
            else:
                print "recherche dans le dossier"
                res = self.search_in_folder(function_folder, val)
                if val in self.list or res:
                    index = 0
                    for i in res :
                        print str(index) + " " + i
                        index = index + 1
                    index_choisi = int(input("lequel charger et lancer ? : "))
                    
                    self.launch_file_and_eval(res[index_choisi])

                else :
                    print "ce f_b n'est pas encore défini"

    def launch_file_and_eval(self, path):
        print "pour ce b on peut bien calculer"
        with open(path, "r") as file:
            
            code = file.read()
            print code
            print  "qui vaut"
            print ">>> " + eval(code)
            file.close()



    def search_in_folder(self,path, name):
        print "script potentiellement interressant"
        list = []
        for (dirpath, dirnames, filenames) in os.walk(function_folder):
            for file in filenames:
                if name in file:
                    list.append(dirpath+"/"+file)
        return list

    def write_code(self, func):
        func_name = func.get_name()
        func_a = func.get_a()
        date = str(self.get_date())
        name = str(func_name)+"_"+str(func_a)+"_"+date

        fullpath = function_folder +"/"+ name + ".py"
        code_file = open(fullpath,"w")
        code_file.write(str(func))

        print "printed this :"
        print str(func)
        code_file.close()

    def get_date(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S",time.gmtime())


if __name__ == '__main__':
    gene = Generator()
    line = Lineaire()

    gene.ask()