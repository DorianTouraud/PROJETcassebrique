#####################################################################################################
# Objectif : Classe Brique pour gérer position, dimensions, couleur et affichage
# Auteurs : Dorian Touraud et Victor Saunier
# Date de début du projet : 06/10/2025
#####################################################################################################

class Brique:
    #initialisation des parametres associes a la brique
    def __init__(self, indice, x, y, largeur=120, hauteur=50, couleur="red"):
        self.indice = indice
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur
        #id de la brique qui servira a reperer lorsqu il y a collision avec la brique
        self.id = None
    #affichage de la brique dans le canva tkinter
    def afficher(self, canvas):
        self.id = canvas.create_rectangle(self.x, self.y, self.x + self.largeur, self.y + self.hauteur, fill = self.couleur, outline="black")
