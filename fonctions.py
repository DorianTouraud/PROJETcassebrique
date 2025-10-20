#####################################################################################################
# Objectif : Gestion de l'interface graphique, du ruban, des scores, vies et initialisation du jeu
# Auteurs : Dorian Touraud et Victor Saunier
# Date : 20/10/2025
# ToDo : Ajouter un menu pause ou paramètres
#####################################################################################################


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
        DisplayJeu.create_text(LARGEUR_FENETRE/2, HAUTEUR_FENETRE/2, text="GAME OVER", fill="white", font=("Arial", 40, "bold"))
        # Arrêter la balle
        from fonctions import obj_balle, obj_raquette
        obj_balle.active = False
        obj_raquette.vers_gauche = False
        obj_raquette.vers_droite = False
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
    DisplayRuban.combo_stack = []  # pile pour les lignes touchées

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
largeur_mur = 8 * 120 + 7 * 10
marge_x = (LARGEUR_FENETRE - largeur_mur) / 2

def initialiserBriques():
    for i in range(5): 
        ligne_brique = []
        for j in range(8): 
            x = marge_x + j * 130
            y = 50 + i * 58
            couleur = couleurs[i % len(couleurs)]
            obj_brique = Brique((i,j), x, y, couleur=couleur)
            obj_brique.afficher(DisplayJeu) #solution remplacer canva par DisplayJeu
            #Canvas.create_rectangle(x,y, x + Brique.largeur, y + Brique.hauteur, couleur)
            ligne_brique.append(obj_brique)
        liste_brique.append(ligne_brique)

def ajouter_score_ligne(frame, ligne_idx):
    ruban = frame.ruban

    # Si la pile est vide ou si on casse une brique sur la même ligne que le sommet
    if ruban.combo_stack and ruban.combo_stack[-1] == ligne_idx:
        ruban.combo_stack.append(ligne_idx)
    else:
        # Nouvelle ligne : reset  pile et empile la ligne actuelle
        ruban.combo_stack = [ligne_idx]

    # Calcul du multiplicateur : 1 + 0.5 par brique consécutive sur la même ligne
    multiplicateur = 1 + (len(ruban.combo_stack) - 1) * 0.5
    points = int(100 * multiplicateur)

    ruban.score += points
    ruban.DisplayScore.config(text=f"SCORE : {ruban.score}")



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
    obj_balle.active = True 
    initialiserBriques()
    initialiserRaquette()
    initialiserBalle()
    DisplayDemarrer.config(text='jeu en cours', state='disabled')
    miseaJour(DisplayJeu.master)


"""
Mettre à jour la fenetre et les entrees
"""
def miseaJour(frame):
    if not obj_balle.active:
        return  # le jeu est fini, on arrête la boucle
    obj_balle.bouger(DisplayJeu, obj_raquette, liste_brique)
    obj_raquette.mise_a_jour(DisplayJeu)
    frame.after(10, miseaJour, frame)


