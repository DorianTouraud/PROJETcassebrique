from cl_fonctions import Fonctions
from tkinter import Tk

##Valeurs initiales
viesInit = 3

root = Tk()
root.title("Casse-briques")

fenetre = Fonctions(root,viesInit)
#afficher le ruban Tkinter (frame,score,vies)
fenetre.packRuban()

#executer la fonction attribuant les commandes de deplacement
fenetre.bindings()


root.mainloop()