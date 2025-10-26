#####################################################################################################
# Objectif : Fichier principal pour lancer le jeu Casse-Briques
# Auteurs : Dorian Touraud et Victor Saunier
# Date de début du projet : 06/10/2025
# ToDo : 
# Lien Github : https://github.com/DorianTouraud/PROJETcassebrique
#####################################################################################################

from cl_fonctions import Fonctions
from tkinter import Tk

#Valeurs initiales du casse brique
viesInit = 3

#creation de la fenetre tkinter
root = Tk()
root.title("Casse-briques")

#initialiser le casse brique
fenetre = Fonctions(root,viesInit)

#afficher le ruban Tkinter (frame,score,vies)
fenetre.packRuban()

#executer la fonction attribuant les commandes de deplacement
fenetre.bindings()

#lancer la boucle d actualisation de la fenetre tkinter
root.mainloop()