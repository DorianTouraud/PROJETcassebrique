Casse-Briques - README

Présentation du jeu :

Ce jeu est une adaptation du jeu Casse-Briques, développé en Python avec la bibliothèque Tkinter. 
Le joueur controle une raquette pour faire rebondir une balle et casser des briques disposées en haut de l'écran. 
L'objectif est de détruire toutes les briques sans perdre toutes ses vies.

Règles du jeu :

1. Déplacement de la raquette
   - La raquette se déplace horizontalement avec les touches flèche gauche et flèche droite.
   - La raquette ne peut pas sortir des limites de l'écran.

2. Balle
   - La balle rebondit sur les murs, le plafond, la raquette et les briques.
   - Si la balle touche le bord inférieur de l'écran, le joueur perd une vie et la balle est replacée au-dessus de la raquette.

3. Briques
   - Les briques sont disposées en plusieurs lignes.
   - Chaque brique cassée rapporte 100 points, avec un bonus multiplicateur si plusieurs briques consécutives sont cassées sur la meme ligne (système de combo).

4. Score et vies
   - Le score total et le nombre de vies restantes sont affichés en haut de l'écran.
   - Le joueur commence avec 3 vies.
   - Lorsque toutes les vies sont perdues, le jeu affiche GAME OVER et se bloque.

5. Fin du jeu
   - Le jeu se termine lorsque toutes les briques sont détruites, affichant le message VICTOIRE ! et bloquant la balle et la raquette.

Spécificités du jeu :

- Taille du terrain : 1200 x 780 pixels.
- Raquette : largeur de 100 pixels, hauteur de 10 pixels, controlée par les flèches.
- Balle : rayon de 8 pixels, vitesse initiale de 3 pixels par mise à jour.
- Briques : largeur de 120 pixels, hauteur de 50 pixels, disposées en 5 lignes et 8 colonnes, avec des couleurs alternées.
- Système de score avec combo :
   - Chaque brique rapporte 100 points.
   - Si plusieurs briques consécutives sont cassées sur la meme ligne, un multiplicateur de score est appliqué (1 + 0,5 par brique consécutive).
- Blocage des actions après la fin du jeu :
   - La balle s'arrete et la raquette ne peut plus etre déplacée.

Comment lancer le jeu :

1. Assurez-vous d'avoir Python d'installé sur votre machine.
2. Lancer le fichier principal : main.py
3. Le jeu se lance dans une fenetre Tkinter.
4. Cliquez sur Démarrer pour initialiser la partie.

Controles :

- Flèche gauche : déplacer la raquette vers la gauche
- Flèche droite : déplacer la raquette vers la droite

Adresse du répertoire GIT : 

https://github.com/DorianTouraud/PROJETcassebrique