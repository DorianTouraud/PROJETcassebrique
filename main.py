import fonctions
from tkinter import Tk, Frame, Canvas

root = Tk()


root.title("Casse-briques")
#afficher le ruban Tkinter (frame,score,vies)

fonctions.packZoneDeJeu(root)
fonctions.packRuban(root,fonctions.renvoiCanvas,0,3)
fonctions.bindings()


root.mainloop()