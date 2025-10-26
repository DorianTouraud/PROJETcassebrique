#####################################################################################################
# Objectif : Classe Raquette pour gérer position, déplacement et collisions
# Auteurs : Dorian Touraud et Victor Saunier
# Date de début du projet : 06/10/2025
# ToDo : Ajouter éventuellement animation ou effet de rebond
#####################################################################################################

class Raquette:
    #initialisation des parametres associes a la raquette
    def __init__(self, x, y = 650, largeur = 100, hauteur = 10, couleur = "black", contour = "white"):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.contour = contour
        self.vitesse = 10
        #parametres qui servent pour verifier l appui sur l une des touches de deplacement
        self.vers_gauche = False
        self.vers_droite = False
        self.id = None
    
    def afficher(self,canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur, outline = self.contour)

    def deplacer_gauche(self, canvas):
        #verification pour empecher la raquette de sortir a gauche lors du deplacement
        if self.x - self.vitesse >= 0:
            #increment de la position de la raquette vers la gauche
            self.x -= self.vitesse
            canvas.move(self.id, -self.vitesse, 0)

    def deplacer_droite(self, canvas):
        #verification pour empecher la raquette de sortir a droite lors du deplacement
        if self.x + self.largeur + self.vitesse <= canvas.winfo_width():
            #increment de la position de la raquette vers la droite
            self.x += self.vitesse
            canvas.move(self.id, self.vitesse, 0)

    def appui_gauche(self, event=None):
        self.vers_gauche = True

    def relache_gauche(self, event=None):
        self.vers_gauche = False

    def appui_droite(self, event=None):
        self.vers_droite = True

    def relache_droite(self, event=None):
        self.vers_droite = False

    #deplacement de la raquette lorsque la touche est maintenue
    #le deplacement s arrete seulement lorsque la touche est relachee
    def deplacementRaquette(self, canvas):
        if self.vers_gauche:
            self.deplacer_gauche(canvas)
        if self.vers_droite:
            self.deplacer_droite(canvas)
