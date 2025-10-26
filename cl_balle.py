#####################################################################################################
# Objectif : Classe Balle pour gérer position, mouvement, collisions avec raquette, murs et briques
# Auteurs : Dorian Touraud et Victor Saunier
# Date de début du projet : 06/10/2025
#####################################################################################################

import math

class Balle:
    #initialisation des parametres associes a la balle
    def __init__(self, x, y, rayon=8, couleur="red", destructionBrique=None):
        self.x = x
        self.y = y
        self.rayon = rayon
        self.couleur = couleur
        #vitesses horizontales et verticales de la balle
        self.vx = 3
        self.vy = -3

        self.id = None
        self.destructionBrique = destructionBrique

    def afficher(self, canvas):
        #afficher la balle (cercle) dans le canva avec tkinter
        #on definit ici le rectangle dans lequel se trouve l oval
        self.id = canvas.create_oval(
            self.x - self.rayon,
            self.y - self.rayon,
            self.x + self.rayon,
            self.y + self.rayon,
            fill=self.couleur
        )

    def bouger(self, canvas, raquette, liste_brique):
        #increment de la position de la balle selon sa vitesse
        self.x += self.vx
        self.y += self.vy
        canvas.move(self.id, self.vx, self.vy)
        largeur = canvas.winfo_width()
        hauteur = canvas.winfo_height()

        #rebonds avec les bordures laterales et superieure du canva
        #on regarde si les extremites de la balle franchissent les limites
        #et on inverse le sens de deplacement selon la bordure touchee
        if self.x - self.rayon <= 0: #bordure gauche
            self.x = self.rayon
            self.vx = -self.vx
        elif self.x + self.rayon >= largeur: #bordure droite
            self.x = largeur - self.rayon
            self.vx = -self.vx
        elif self.y - self.rayon <= 0: #bordure superieure
            self.y = 0 + self.rayon
            self.vy = -self.vy
        
        #sortie de la zone de jeu
        if self.y - self.rayon >= hauteur:
            #on recree une raquette a la position initiale
            nouveau_raquette_x = (largeur - raquette.largeur) / 2
            dx = nouveau_raquette_x - raquette.x
            raquette.x = nouveau_raquette_x
            canvas.move(raquette.id, dx, 0)
            self.x = raquette.x + raquette.largeur / 2
            self.y = raquette.y - self.rayon - 1
            #reinitialisation de la vitesse et direction
            self.vx = 3
            self.vy = -3
            #on recree la balle
            canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)

        #Collision raquette
        if raquette.id is not None:
            rx1, ry1, rx2, ry2 = canvas.coords(raquette.id)
            #verification de la collision entre la raquette et la balle
            if (self.vy > 0 and (self.y + self.rayon) >= ry1 and (self.y - self.rayon) <= ry2
                    and (self.x >= rx1) and (self.x <= rx2)):
                #calcul de la position du centre de la raquette pour determiner le rebond
                raquette_centre = (rx1 + rx2) / 2
                distance_centre = self.x - raquette_centre
                proportion = distance_centre / (raquette.largeur / 2)
                angle_max = math.radians(60)
                angle = proportion * angle_max
                vitesse = (self.vx ** 2 + self.vy ** 2) ** 0.5
                #modification de la vitesse de la balle et changement de direction sur l axe vertical
                self.vx = vitesse * math.sin(angle)
                self.vy = -abs(vitesse * math.cos(angle))
                self.y = ry1 - self.rayon

        #Collision briques
        for ligne_idx, ligne in enumerate(liste_brique):
            #parcour des differentes briques
            for brique in ligne:
                if brique.id is not None:
                    bx1, by1, bx2, by2 = canvas.coords(brique.id)
                    #verification du contact de la balle avec la brique
                    if (self.x + self.rayon >= bx1 and self.x - self.rayon <= bx2 and
                        self.y + self.rayon >= by1 and self.y - self.rayon <= by2):

                        # Supprime la brique
                        canvas.delete(brique.id)
                        brique.id = None

                        # Rebonds selon le cote touche
                        dx_gauche = abs((self.x + self.rayon) - bx1)
                        dx_droite = abs((self.x - self.rayon) - bx2)
                        dy_haut = abs((self.y + self.rayon) - by1)
                        dy_bas = abs((self.y - self.rayon) - by2)
                        min_dist = min(dx_gauche, dx_droite, dy_haut, dy_bas)
                        if min_dist == dx_gauche or min_dist == dx_droite:
                            self.vx = -self.vx if self.vx != 0 else 3
                        else:
                            self.vy = -self.vy if self.vy != 0 else 3

                        #Ajout du score de destruction de la brique
                        if callable(self.destructionBrique):
                            try:
                                self.destructionBrique(ligne_idx)
                            except Exception as e:
                                print("Erreur callback destructionBrique :", e)
