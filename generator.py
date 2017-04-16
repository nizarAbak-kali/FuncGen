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
        # boucle pour demander la val à generer dans la fonction
        while 1 :
            # on recup la val donnée par l'utilisateur
            val = raw_input("Entrez a (q to quit):")
            # on test si cet val et un q pour quitter la boucle avec un break
            if str(val) == "q":
                break

            else:
                # on ajoute la va à une liste
                self.list.append(val)
                # on créer la fonction lineaire
                # TODO : permettre à l'utilisateur de choisir quelle fonction il veut parmie celle qui sont dispo
                lin = Lineaire(val)
                # on appelle la methode qui ecrit dans le dossier de fonction
                self.write_code(lin)
                # on efface de l'objet lin qui ne sert plus à rien pour economiser de la mémoire
                del lin
            print val
        # boucle pour le choix de quelle fonction on veut
        while 1 :
            val = raw_input("Entrez b (q to quit):")
            if str(val) == "q":
                exit(0)
            else:
                print "recherche dans le dossier"
                # on cherche si il existe une fonction, qui calcule avec la val demandé, dans le dossier
                res = self.search_in_folder(self.function_folder, val)
                # si la val est dans la list ou dans le dossier
                if val in self.list or res:
                    index = 0
                    #on affiche un menu pour choisir quelle fichier charger
                    for i in res :
                        print str(index) + " " + i
                        index = index + 1
                    index_choisi = int(input("lequel charger et lancer ? : "))
                    # on appelle la methode qui charge le fichier et appelle la fonction fn
                    self.launch_file_and_eval(res[index_choisi])

                else:
                    # message si la fonction rechercher n'existe pas
                    print "ce f_b n'est pas encore défini"

    # fonction qui le fichier au chemin donnée
    def launch_file_and_eval(self, path):
        print "pour ce b on peut bien calculer"
        # on ouvre le fichier en mode lecture "r" et on recupere le contenue dans file
        with open(path, "r") as file:
            # on lit le fichier et on ecrit les catactère dans code
            code = file.read()
            # on affiche le code
            print code
            # on recupère le module chargé au chemin path dans la var module
            module = self.importFromURI(path)
            # on affiche la fonction
            print  module.fn
            # on demande la val de x
            val = input("Entrez x :")

            print  "qui vaut"
            #on affiche la val du calcul
            print ">>> " + str(module.fn(val))
            file.close()

    # fonction de recherche d'un nom dans un dossier fournie par un path(chemin)
    def search_in_folder(self,path, name):
        print "script potentiellement interressant"
        list = []
        # on parcours le dossier à l'aide os.walk et on recup le dirpath(chemin vers les sous dossier),
        # le nom du dossier , le nom des fichier (une liste )
        for (dirpath, dirnames, filenames) in os.walk(self.function_folder):
            # pour chaque fichier dans la liste des fichiers
            for file in filenames:
                # on decoupe le nom du dossier à chaque '_' afin de pouvoir comparer le chiffre dans le nom du fichier
                # et la val rechercher
                word_list = str(file).split("_")
                if name == word_list[1]:
                    list.append(dirpath +"/" + file)
        # on retourne la liste des fichiers potentiellement interressant
        return list

    # methode qui ecrit le code
    def write_code(self, func):
        # on recup le nom de la fonction
        func_name = func.get_name()
        func_a = func.get_a()
        # la date et l'heure
        date = str(self.get_date())
        # on fabrique le nom
        name = str(func_name)+"_"+str(func_a)+"_"+date
        # on fabrique le nom + chemin + l'extension
        fullpath = self.function_folder + "/" + name + ".py"
        # on creer le fichier en mode ecriture
        code_file = open(fullpath,"w")
        # on ecrit le code en faisant appelle à la methode __str__ de chaque objet qui les convertie en string
        code_file.write(str(func))
        print "printed this :"
        print str(func)
        # on ferme le fichier
        code_file.close()

    def get_date(self):
        return time.strftime("%Y-%m-%d_%H:%M:%S", time.gmtime())

    # methode d'importation
    def importFromURI(self, uri, absl=False):
        # si le parametre absl et à True alors on veut le chemin abs
        if not absl:
            uri = os.path.normpath(os.path.join(os.path.dirname(__file__), uri))
        # on separe dans le chemin le path et le nom de fichier
        # ensuite du nom de fichier on separe le nom du module et l'extension
        path, fname = os.path.split(uri)
        mname, ext = os.path.splitext(fname)

        no_ext = os.path.join(path, mname)

        # si le module est compilé
        if os.path.exists(no_ext + '.pyc'):
            try:
                return imp.load_compiled(mname, no_ext + '.pyc')
            except:
                pass
        # si le module est du code source
        if os.path.exists(no_ext + '.py'):
            try:
                #on retourne le code source chargé comme module
                return imp.load_source(mname, no_ext + '.py')
            except:
                pass



if __name__ == '__main__':
    gene = Generator()
    line = Lineaire()
    gene.ask()