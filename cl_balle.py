#####################################################################################################
# Objectif : Classe Balle pour gérer position, mouvement, collisions avec raquette, murs et briques
# Auteurs : Dorian Touraud et Victor Saunier
# Date : 20/10/2025
# ToDo : Ajouter éventuellement une vitesse variable
#####################################################################################################


class Balle:
    def __init__(self, x, y, rayon = 8, couleur = "red"):
        self.x = x
        self.y = y 
        self.rayon = rayon
        self.couleur = couleur
        self.vx = 3
        self.vy = -3
        self.vie_perdue = False
        self.id = None

    def afficher(self, canvas):
        self.id = canvas.create_oval(self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon, fill = self.couleur)

    def bouger(self, canvas, raquette, liste_brique):
        self.x += self.vx
        self.y += self.vy
        self.active = True
        canvas.move(self.id, self.vx, self.vy)
        largeur = canvas.winfo_width()
        hauteur = canvas.winfo_height()
        
        # Arret du mouvement de la balle si on gagne/perd
        if not self.active:
                return

        # Collision avec les murs gauche/droite/plafond
        if self.x - self.rayon <= 0:
            self.x = self.rayon
            self.vx = -self.vx
        elif self.x + self.rayon >= largeur:
            self.x = largeur - self.rayon
            self.vx = -self.vx
        elif self.y - self.rayon <= 0:
            self.y = 0 + self.rayon
            self.vy = -self.vy
        
        # Collision avec la bordure inférieure
        if self.y - self.rayon >= hauteur:
            if not self.vie_perdue:
                # Déclenche perte de vie une seule fois
                import fonctions
                if canvas.master:
                    fonctions.perte_vie(canvas.master)
                self.vie_perdue = True
            # recentre la raquette et replace la balle juste au-dessus
            nouveau_raquette_x = (largeur - raquette.largeur) / 2
            dx = nouveau_raquette_x - raquette.x
            raquette.x = nouveau_raquette_x
            canvas.move(raquette.id, dx, 0)
            self.x = raquette.x + raquette.largeur / 2
            self.y = raquette.y - self.rayon - 1
            self.vx = 3
            self.vy = -3
            canvas.coords(self.id, self.x - self.rayon, self.y - self.rayon, self.x + self.rayon, self.y + self.rayon)
        elif self.vie_perdue and self.y - self.rayon < hauteur - 10:
            self.vie_perdue = False

        # Collision avec la raquette
        if raquette.id is not None:
            rx1, ry1, rx2, ry2 = canvas.coords(raquette.id)
            # si la balle touche la raquette
            if (self.vy > 0 and (self.y + self.rayon) >= ry1 and (self.y - self.rayon) <= ry2 and (self.x >= rx1) and (self.x <= rx2)):
                raquette_centre = (rx1 + rx2) / 2
                distance_centre = self.x - raquette_centre
                
                # Normalisation de la raquette (-1 = tout à gauche, 1 = tout à droite)
                proportion = distance_centre / (raquette.largeur / 2)
                
                # Définition d'un angle maximum de rebond
                import math
                angle_max = math.radians(60)
                angle = proportion * angle_max
                
                vitesse = (self.vx**2 + self.vy**2)**0.5  # On garde la même vitesse en norme
                self.vx = vitesse * math.sin(angle)
                self.vy = -abs(vitesse * math.cos(angle))  # La balle rebondit toujours vers le haut
                self.y = ry1 - self.rayon


        # Collision avec les briques
        for ligne_idx, ligne in enumerate(liste_brique):
            for brique in ligne:
                if brique.id is not None:
                    bx1, by1, bx2, by2 = canvas.coords(brique.id)
                    if (self.x + self.rayon >= bx1 and self.x - self.rayon <= bx2 and self.y + self.rayon >= by1 and self.y - self.rayon <= by2):
                        canvas.delete(brique.id)  # Supprime la brique
                        brique.id = None

                        # Gestion du rebond selon le côté touché
                        dx_gauche = abs((self.x + self.rayon) - bx1)
                        dx_droite = abs((self.x - self.rayon) - bx2)
                        dy_haut = abs((self.y + self.rayon) - by1)
                        dy_bas = abs((self.y - self.rayon) - by2)
                        min_dist = min(dx_gauche, dx_droite, dy_haut, dy_bas)
                        if min_dist == dx_gauche or min_dist == dx_droite:
                            self.vx = -self.vx if self.vx != 0 else 3
                        else:
                            self.vy = -self.vy if self.vy != 0 else 3

                        # Ajouter le score avec combo par ligne
                        import fonctions
                        if canvas.master:
                            fonctions.ajouter_score_ligne(canvas.master, ligne_idx)
        
        # Vérifie si toutes les briques ont été détruites
        if all(brique.id is None for ligne in liste_brique for brique in ligne):
            canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, text="GAGNE", fill="white", font=("Arial", 40, "bold"))
            obj_balle.active = False # type: ignore
            obj_raquette.vers_gauche = False # type: ignore
            obj_raquette.vers_droite = False # type: ignore
            return  # arrête de bouger la balle
