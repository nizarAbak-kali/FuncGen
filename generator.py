#!/usr/bin/python
# coding=utf-8

import imp
import os
import time

from funType import Lineaire
from funType.Lineaire import Lineaire

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
                Sinon (si b n'est pas dans L), print "ce f_b n'est pas encore défini
                "
"""




class Generator:

    def __init__(self):
        self.list = []

        # TODO : change this to let the user give his own function directory
        home = os.path.expanduser("~")
        if os.path.isdir("function_generated/"):
            print "function folder already exist !!"
        else:
            print "function folder does not exist !!"
            os.mkdir("function_generated")
        self.function_folder = os.path.dirname("function_generated/")


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
                res = self.search_in_folder(self.function_folder, val)
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
            module = self.importFromURI(path)
            print  module.fn
            val = input("Entrez x :")

            print  "qui vaut"
            print ">>> " + str(module.fn(val))
            file.close()



    def search_in_folder(self,path, name):
        print "script potentiellement interressant"
        list = []
        for (dirpath, dirnames, filenames) in os.walk(self.function_folder):
            for file in filenames:
                word_list = str(file).split("_")
                if name == word_list[1]:
                    list.append(dirpath+"/"+file)
        return list

    def write_code(self, func):
        func_name = func.get_name()
        func_a = func.get_a()
        date = str(self.get_date())
        name = str(func_name)+"_"+str(func_a)+"_"+date

        fullpath = self.function_folder + "/" + name + ".py"
        code_file = open(fullpath,"w")
        code_file.write(str(func))

        print "printed this :"
        print str(func)
        code_file.close()

    def get_date(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S",time.gmtime())

    def importFromURI(self, uri, absl=False):
        if not absl:
            uri = os.path.normpath(os.path.join(os.path.dirname(__file__), uri))
        path, fname = os.path.split(uri)
        mname, ext = os.path.splitext(fname)

        no_ext = os.path.join(path, mname)

        if os.path.exists(no_ext + '.pyc'):
            try:
                return imp.load_compiled(mname, no_ext + '.pyc')
            except:
                pass
        if os.path.exists(no_ext + '.py'):
            try:
                return imp.load_source(mname, no_ext + '.py')
            except:
                pass



if __name__ == '__main__':
    gene = Generator()
    line = Lineaire()
    gene.ask()