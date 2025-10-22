"""
fonctions d'interface tkinter
TO_DO:
            FAIT supprimmer raquette fantome
    corriger rebond
            FAIT score
            FAIT texte de victoire
"""
from tkinter import Frame, Canvas, Label, Button
from cl_brique import Brique
from cl_raquette import Raquette
from cl_balle import Balle


'''
FONCTIONS contenues dans le ruban
Score   Vies    [Démarrer]  [Quitter]
'''
class Fonctions:
    def __init__(self, frame, vies_init, LARGEUR_FENETRE = 1200, HAUTEUR_FENETRE = 780):
        self.frame = frame
        self.LARGEUR_FENETRE = LARGEUR_FENETRE
        self.HAUTEUR_FENETRE = HAUTEUR_FENETRE
        #ruban valeurs initiales
        self.score_init = 0
        self.vies_init = vies_init
        #ruban valeurs
        self.score = self.score_init
        self.vies = self.vies_init
        #displays
        self.DisplayRuban = Frame(self.frame, width = self.LARGEUR_FENETRE, pady=10, bg='red')
        self.DisplayRuban.pack(side='top')
        self.DisplayScore = self.score_init
        self.DisplayVies = self.vies_init
        self.PileCombo = []  # pile pour les lignes de brique touchées
        self.DisplayJeu = Canvas(self.frame,width = self.LARGEUR_FENETRE, height = self.HAUTEUR_FENETRE, bg='gray26')
        self.DisplayJeu.pack(side='bottom')

        #briques
        self.couleurs = ["red", "orange", "yellow", "green", "blue"]
        self.largeur_mur = 8 * 120 + 7 * 10
        self.marge_x = (self.LARGEUR_FENETRE - self.largeur_mur) / 2
        self.ligne_idx = 0
        #raquette
        self.raquette_x = (self.LARGEUR_FENETRE - 80) / 2
        self.obj_raquette = Raquette(self.raquette_x)
        #balle

       
    def ScoreVies(self):
        self.score = self.score_init
        self.vies = self.vies_init
        self.DisplayScore = Label(self.DisplayRuban, text=f"SCORE : {self.score}")
        self.DisplayScore.pack(side='left', padx=7, pady=5)
        self.DisplayVies = Label(self.DisplayRuban, text=f"VIES : {self.vies}")
        self.DisplayVies.pack(side='left', padx=7, pady=5)
        
    def boutonDemarrer(self):
        self.DisplayDemarrer = Button(self.DisplayRuban,text='Démarrer', command = self.initialiserPartie) #ne pas mettre () après appel de initialiserPartie
        self.DisplayDemarrer.pack(side = 'right',padx=7,pady=5)

    def boutonQuitter(self):
        #la fonction reprend la fonction destroy de tkinter
        self.DisplayQuitter = Button(self.DisplayRuban,text='Quitter',command = self.frame.destroy)
        self.DisplayQuitter.pack(side = 'right',padx=7,pady=5)

    def packRuban(self):
        ## ajouter dans __init__
        self.ScoreVies()
        self.boutonQuitter()
        self.boutonDemarrer()

    def perte_vie(self):
        self.vies -= 1
        self.DisplayVies.config(text=f"VIES : {self.vies}")

        if self.vies <= 0:
            self.GameOver = self.DisplayJeu.create_text(self.LARGEUR_FENETRE / 2, self.HAUTEUR_FENETRE / 2,text="GAME OVER", fill="white", font=("Arial", 40, "bold"))        
            self.DisplayDemarrer.config(text='Redémarrer', state='active' ,command=self.Rejouer)
            return False  # stop le jeu
        return True

    
    #FONCTIONS de creation et gestion du CANVAS
    def CreateDisplayJeu(self):
        self.DisplayJeu = Canvas(self.frame,width = self.LARGEUR_FENETRE, height = self.HAUTEUR_FENETRE, bg='gray26')
        self.DisplayJeu.pack(side='bottom')
    
    #FONCTIONS d'initalisation
    def bindings(self):
        #Binds de la raquette
        self.DisplayJeu.focus_set()
        self.DisplayJeu.bind("<KeyPress-Left>", self.obj_raquette.appui_gauche)
        self.DisplayJeu.bind("<KeyRelease-Left>", self.obj_raquette.relache_gauche)
        self.DisplayJeu.bind("<KeyPress-Right>", self.obj_raquette.appui_droite)
        self.DisplayJeu.bind("<KeyRelease-Right>", self.obj_raquette.relache_droite)

    def initialiserBriques(self):
        self.liste_brique = []
        for i in range(5):
            ligne_brique = []
            for j in range(8):
                x = self.marge_x + j * 130
                y = 50 + i * 58
                couleur = self.couleurs[i % len(self.couleurs)]
                obj_brique = Brique((i,j), x, y, couleur=couleur)
                obj_brique.afficher(self.DisplayJeu)
                ligne_brique.append(obj_brique)
            self.liste_brique.append(ligne_brique)

    def initialiserRaquette(self):
        self.raquette_x = (self.LARGEUR_FENETRE - 80) / 2
        self.obj_raquette = Raquette(self.raquette_x)
        self.obj_raquette.afficher(self.DisplayJeu)

    def initialiserBalle(self):
        self.balle_x = self.obj_raquette.x + self.obj_raquette.largeur / 2
        self.balle_y = self.obj_raquette.y - 8 - 1
        self.obj_balle = Balle(self.balle_x, self.balle_y, on_brique_destroy=self.on_brique_destroy)
        self.obj_balle.afficher(self.DisplayJeu)

        

    def initialiserPartie(self):
        #initialisation des graphiques et objets
        self.score = self.score_init
        self.vies = self.vies_init
        self.DisplayVies.config(text=f"VIES : {self.vies}")
        self.initialiserBriques()
        self.initialiserRaquette()
        self.initialiserBalle()
        self.bindings()
        self.DisplayDemarrer.config(text='jeu en cours', state='disabled')
        self.miseaJour()

    def Rejouer(self):
        #nettoyer le canva des ibjets précédents
        self.DisplayJeu.delete('all')
        self.initialiserPartie()
        self.DisplayJeu.delete(self.GameOver)


    #fonction de gestion du score et du combo
    def on_brique_destroy(self, ligne_idx):
        if self.PileCombo and self.PileCombo[-1] == ligne_idx:
            self.PileCombo.append(ligne_idx)
        else:
            self.PileCombo = [ligne_idx]

        multiplicateur = 1 + (len(self.PileCombo) - 1) * 0.5
        points = int(100 * multiplicateur)
        self.score += points

        if isinstance(self.DisplayScore, Label):
            self.DisplayScore.config(text=f"SCORE : {self.score}")

        



    def ajouter_score_ligne(self):
        # Si la pile est vide ou si on casse une brique sur la même ligne que le sommet
        if self.PileCombo and self.PileCombo[-1] == self.ligne_idx:
            self.PileCombo.append(self.ligne_idx)
        else:
            self.PileCombo = [self.ligne_idx]

        # Calcul du multiplicateur : 1 + 0.5 par brique consécutive sur la même ligne
        multiplicateur = 1 + (len(self.PileCombo) - 1) * 0.5
        points = int(100 * multiplicateur)

        self.score += points
        self.DisplayScore.config(text=f"SCORE : {self.score}")
    
    def VerifierBriquesRestantes(self):
        print(self.ligne_idx)
        if all(brique.id is None for ligne in self.liste_brique for brique in ligne):
            self.GameOver = self.DisplayJeu.create_text(self.LARGEUR_FENETRE / 2, self.HAUTEUR_FENETRE / 2,text="GAGNE", fill="white", font=("Arial", 40, "bold"))
            self.DisplayDemarrer.config(text='Redémarrer', state='active' ,command=self.Rejouer)
            return False  # stop le jeu
        else :
            return True

    #Mettre à jour la fenetre et les entrees
    def miseaJour(self):
        self.obj_balle.bouger(self.DisplayJeu, self.obj_raquette, self.liste_brique)
        self.obj_raquette.deplacementRaquette(self.DisplayJeu)
        # Si la balle est tombée sous le bas du canvas
        if self.obj_balle.y - self.obj_balle.rayon >= self.HAUTEUR_FENETRE:
            if not self.perte_vie():
                return  # stop la boucle si GAME OVER
            self.frame.after(1000, self.miseaJour)
        elif not self.VerifierBriquesRestantes():
            return
        else:
            self.frame.after(10, self.miseaJour)
    

    