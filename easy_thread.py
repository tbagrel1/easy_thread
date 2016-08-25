# -*- coding: utf-8 -*-

from time import sleep

if True:  # Ajout du module threadTBAG
    from threading import *

    # Définition des classes et fonctions :
    def static(dict_var_val):
        def staticf(f):
            def decorated(*args, **kwargs):
                f(*args, **kwargs)
            for var, val in dict_var_val.items():
                setattr(decorated, var, val)
            return decorated
        return staticf

    class aThread(Thread):
        def __init__(self, threadID, name, command):
            Thread.__init__(self)
            self.threadID = threadID
            self.name = name
            self.command = command

        def run(self):
            print("Starting " + self.name + " : " + str(self.threadID) + 
                  " { " + self.command + " }")
            exec(self.command)
            print("Exiting " + self.name + " : " + str(self.threadID) + 
                  " { " + self.command + " }")

    @static({"c": 0})
    def toThread(name, command):
        exec("Thread_" + str(toThread.c) + " = aThread(" + str(toThread.c) + 
             ", \"" + name + "\", \"" + command + "\")")
        exec("Thread_" + str(toThread.c) + ".daemon = True")
        exec("Thread_" + str(toThread.c) + ".start()")
        toThread.c += 1

# Exemple

def affichern(n):
    for i in range(n):
        print(i)
        sleep(1)

def affichern2(n):
    for i in range(n):
        print(i**2)
        sleep(1)

toThread("afficher_n", "affichern(10)")
toThread("afficher_n2", "affichern2(10)")

sleep(5)

