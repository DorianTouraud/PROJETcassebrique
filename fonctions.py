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

def score_vies(frame, score_init, vies_init):
    global DisplayScore, DisplayVies, score, vies
    score = score_init
    vies = vies_init
    DisplayScore = Label(frame, text=f"SCORE : {score}")
    DisplayScore.pack(side='left', padx=7, pady=5)
    DisplayVies = Label(frame, text=f"VIES : {vies}")
    DisplayVies.pack(side='left', padx=7, pady=5)


def perte_vie(frame):
    ruban = frame.ruban
    ruban.vies -= 1
    ruban.DisplayVies.config(text=f"VIES : {ruban.vies}")

    if ruban.vies <= 0:
        DisplayJeu.create_text(LARGEUR_FENETRE/2, HAUTEUR_FENETRE/2,text="GAME OVER", fill="white", font=("Arial", 40, "bold"))
        return False  # stop le jeu
    return True



def boutonDemarrer(frame,canva):
    global DisplayDemarrer
    DisplayDemarrer = Button(frame,text='Démarrer',command=initialiserPartie) #ne pas mettre () après appel de initialiserPartie
    DisplayDemarrer.pack(side = 'right',padx=7,pady=5)

#la fonction reprend la fonction destroy de tkinter
def boutonQuitter(frame,mainframe):
    DisplayQuitter = Button(frame,text='Quitter',command=mainframe.destroy)
    DisplayQuitter.pack(side = 'right',padx=7,pady=5)

def packRuban(frame, canva, score, vies):
    DisplayRuban = Frame(frame, padx=10, pady=10, bg='cadetblue4')
    DisplayRuban.score = score
    DisplayRuban.vies = vies

    DisplayRuban.DisplayScore = Label(DisplayRuban, text=f"SCORE : {score}")
    DisplayRuban.DisplayScore.pack(side='left', padx=7, pady=5)

    DisplayRuban.DisplayVies = Label(DisplayRuban, text=f"VIES : {vies}")
    DisplayRuban.DisplayVies.pack(side='left', padx=7, pady=5)

    boutonQuitter(DisplayRuban, frame)
    boutonDemarrer(DisplayRuban, canva)
    DisplayRuban.pack(side='top')

    frame.ruban = DisplayRuban  # on le garde en référence

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
def bindings():
    #Binds de la raquette
    DisplayJeu.focus_set()
    DisplayJeu.bind("<KeyPress-Left>", obj_raquette.appui_gauche)
    DisplayJeu.bind("<KeyRelease-Left>", obj_raquette.relache_gauche)
    DisplayJeu.bind("<KeyPress-Right>", obj_raquette.appui_droite)
    DisplayJeu.bind("<KeyRelease-Right>", obj_raquette.relache_droite)


#Briques
liste_brique = []
couleurs = ["red", "orange", "yellow", "green", "blue"]
def initialiserBriques():
    for i in range(5):
        ligne_brique = []
        for j in range(8):
            x = 75 + j * 130
            y = 50 + i * 58
            couleur = couleurs[i % len(couleurs)]
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
    DisplayJeu.master.ruban.vies = 3
    DisplayJeu.master.ruban.DisplayVies.config(text="VIES : 3")
    initialiserBriques()
    initialiserRaquette()
    initialiserBalle()
    DisplayDemarrer.config(text='jeu en cours', state='disabled')
    miseaJour(DisplayJeu.master)


"""
Mettre à jour la fenetre et les entrees
"""
def miseaJour(frame):
    obj_balle.bouger(DisplayJeu, obj_raquette, liste_brique)
    obj_raquette.mise_a_jour(DisplayJeu)
    # Si la balle est tombée sous le bas du canvas
    if obj_balle.y - obj_balle.rayon >= HAUTEUR_FENETRE:
        if not perte_vie(frame):
            return  # stop la boucle si GAME OVER
        frame.after(1000, miseaJour, frame)
    else:
        frame.after(10, miseaJour, frame)

