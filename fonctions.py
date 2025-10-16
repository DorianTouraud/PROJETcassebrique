"""
fonctions d'interface tkinter

"""
from tkinter import * 
""" Tk, Label, Button, Frame, Canvas"""
from cl_brique import Brique
from cl_raquette import Raquette
from cl_balle import Balle


'''
FONCTIONS contenues dans le ruban
Score   Vies    [Démarrer]  [Quitter]
'''
def score_vies(frame,score,vies):
    DisplayScore = Label(frame, text = str("SCORE : "+str(score)))
    DisplayScore.pack(side='left',padx=7,pady=5)
    DisplayVies = Label(frame, text = str("VIES : "+str(vies)))
    DisplayVies.pack(side='left',padx=7,pady=5)

def boutonDemarrer(frame,canva):
    global DisplayDemarrer
    DisplayDemarrer = Button(frame,text='Démarrer',command=initialiserPartie) #ne pas mettre () après appel de initialiserPartie
    DisplayDemarrer.pack(side = 'right',padx=7,pady=5)

#la fonction reprend la fonction destroy de tkinter
def boutonQuitter(frame,mainframe):
    DisplayQuitter = Button(frame,text='Quitter',command=mainframe.destroy)
    DisplayQuitter.pack(side = 'right',padx=7,pady=5)

def packRuban(frame,canva,score,vies):
    DisplayRuban = Frame(frame, padx=10,pady=10)
    DisplayRuban['bg'] = 'cadetblue4'
    score_vies(DisplayRuban,score,vies)
    boutonQuitter(DisplayRuban,frame)
    boutonDemarrer(DisplayRuban,canva)
    DisplayRuban.pack(side='top')

'''
FONCTIONS de creation et gestion du CANVAS
'''
LARGEUR_FENETRE = 1200
HAUTEUR_FENETRE = 780


def packZoneDeJeu(frame):
    global DisplayJeu
    DisplayJeu = Canvas(frame,width=LARGEUR_FENETRE, height=HAUTEUR_FENETRE, bg='gray26')
    DisplayJeu.pack(side='bottom')

def renvoiCanvas():
    return DisplayJeu

def afficherBrique(canva):
    return Brique.afficher(canva)

'''
FONCTIONS d'initalisation
'''
def bindings(frame):
    #Binds de la raquette
    DisplayJeu.focus_set()
    frame.bind("<KeyPress-Left>", Raquette.appui_gauche)
    frame.bind("<KeyRelease-Left>", Raquette.relache_gauche)
    frame.bind("<KeyPress-Right>", Raquette.appui_droite)
    frame.bind("<KeyRelease-Right>", Raquette.relache_droite)


#Briques
liste_brique = []
def initialiserBriques():
    for i in range(10):
        ligne_brique = []
        for j in range(12):
            x = 50 + j * 92.7
            y = 50 + i * 35
            couleur = ["red", "orange", "yellow", "green", "blue", "blue", "green", "yellow", "orange", "red"][i]
            obj_brique = Brique((i,j), x, y, couleur=couleur)
            obj_brique.afficher(DisplayJeu) #solution remplacer canva par DisplayJeu
            #Canvas.create_rectangle(x,y, x + Brique.largeur, y + Brique.hauteur, couleur)
            ligne_brique.append(obj_brique)
        liste_brique.append(ligne_brique)


#Raquette
raquette_x = (LARGEUR_FENETRE - 80) / 2
obj_raquette = Raquette(raquette_x)
def initialiserRaquette():
    obj_raquette.afficher(DisplayJeu)

#Balle
balle_x = obj_raquette.x + obj_raquette.largeur / 2
balle_y = obj_raquette.y - 8 - 1
obj_balle = Balle(balle_x, balle_y)
def initialiserBalle():
    obj_balle.afficher(DisplayJeu)


"""
Initialiser toutes les fonctions de Briques et de Boules
"""
def initialiserPartie():
    initialiserBriques()
    initialiserRaquette()
    DisplayDemarrer.config(text='jeu en cours', state='disabled')

"""
Mettre à jour la fenetre et les entrees
"""
def miseaJour(frame):
    obj_balle.bouger(DisplayJeu, obj_raquette, liste_brique)
    obj_raquette.mise_a_jour(DisplayJeu)
    frame.after(10, miseaJour(frame))  