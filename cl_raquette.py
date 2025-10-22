class Raquette:
    def __init__(self, x, y = 500, largeur = 100, hauteur = 10, couleur = "black", contour = "white"):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.contour = contour
        self.vitesse = 10
        self.vers_gauche = False
        self.vers_droite = False
        self.id = None
    
    def afficher(self,canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur, outline = self.contour)

    def deplacer_gauche(self, canvas):
        if self.x - self.vitesse >= 0:
            self.x -= self.vitesse
            canvas.move(self.id, -self.vitesse, 0)

    def deplacer_droite(self, canvas):
        if self.x + self.largeur + self.vitesse <= canvas.winfo_width():
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

    def deplacementRaquette(self, canvas):
        if self.vers_gauche:
            self.deplacer_gauche(canvas)
        if self.vers_droite:
            self.deplacer_droite(canvas)
