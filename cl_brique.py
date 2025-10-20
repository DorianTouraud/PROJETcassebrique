#####################################################################################################
# Objectif : Classe Brique pour gérer position, dimensions, couleur et affichage
# Auteurs : Dorian Touraud et Victor Saunier
# Date : 20/10/2025
# ToDo : Ajouter des types de briques
#####################################################################################################


class Brique:
    def __init__(self, indice, x, y, largeur=120, hauteur=50, couleur="red"):
        self.indice = indice
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        self.id = None
    def afficher(self, canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur, outline="black")
