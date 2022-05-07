# import des librairies

import tkinter as tk
from tkinter.messagebox import showinfo
from time import sleep
from random import randint

#############################

# fonctions de gestion du GUI

def tour_de_jeu(x):
	""" effectue un tour du joueur:
	
	- place un jeton dans la colonne souhaitée
	- passe au tour du joueur suivant
	
	variable x:
	
	correspond à l'endroit cliqué sur la fenêtre,
	clic à la colonne souhaitée
	"""

	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE
					
	y = clic(tour+1, x)	# tour+1 est la couleur, il y a pas de modulo
	
	# colonne pleine
	if y == -1:
		showinfo("Impossible", "On ne peut pas staquer plus de Y pièces pas colonnes")

	else:
		# le cercle apparait sur l'image
		tracer_cercle(y, x, ("red" if tour == 0 else "yellow"))
		# vérifie s'il y a alignement
		root.after(50, check_win)

	# modifie la couleur de la bannière pour le prochain joueur
	for x in range(X):
		banniere[x].config(bg=("red" if tour == 1 else "yellow"))
	
	# tour du joueur suivant
	tour = (1 if tour == 0 else 0)

	# si le joueur suivant est une IA
	if (tour == 0 and IA_PLAYER0 == True) or (tour == 1 and IA_PLAYER1 == True):
		root.after(1000, IA)	#sleep(2)

        
def clic(tour_joueur, x):
	""" - faire descendre les jetons
		- change les valeurs des cases
	
	variables:
	tour_joueur: valeur numérique de la case dans la matrice
	x: coordonnée horizontale d'une case
	
	return:
	- coordonnée verticale d'une case
	- ou colonne pleine
	"""
	
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE

	for y in range(Y):
		if grid[Y-y-1][x] == 0:
			grid[Y-y-1][x] = tour_joueur
			return Y-y-1
	return -1


def ligne(_sum, y, x, __y, __x):
	'''
	C'est une fonction recurente qui fait partie de l'analyse du gagnant.
	A partire d'une position (y,x) va avancer par recurence dans la grille en s'auto appellant tant qu'il n'y a pas de jeton adverse ou de vide.
	Par exemple on commence a (0,0) et comme `pas` (1,1), le fonction va call (0,0), (1,1), (2,2) ... (n,m) tant qu'il y a un jeton du joueur analysé en ce moment.
	__y,__x etant ls pas fait a chaque fois pour avancer dans la grille. Ca peut etre (-1,1) (1,1) (0,-1) ...
	'''
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE

	if X == x  or x < 0 or Y == y  or y < 0:	#Dans le cas ou la fonction analyse une case sortie en dehor du tableau
		return _sum
	elif grid[y][x] == tour+1:	#dans le cas ou la case actuellement regardé comporte un jeton de la couleur du joueur analysé (`tour+1`)
		return ligne(_sum+1, y+__y, x+__x, __y, __x)
	else:	#Sinon on revoit la somme de jetons compté dans une direction
		return _sum


def check_position(y, x):
	'''
	A partire d'un point (y,x) on check dans toutes les directions si il y a des lignes de jetons du joueur analysé
	'''
	a_droite = ligne(0, y, x+1, 0, 1)
	a_gauche = ligne(0, y, x-1, 0, -1)
	en_haut = ligne(0, y-1, x, -1, 0)
	en_bas = ligne(0, y+1, x, 1, 0)
	diag_nord_ouest = ligne(0, y-1, x-1, -1, -1)
	diag_nord_est = ligne(0, y-1, x+1, -1, 1)
	diag_sud_ouest = ligne(0, y+1, x-1, 1, -1)
	diag_sud_est = ligne(0, y+1, x+1, 1, 1)
	# + 1 +   car on avait vu avant qu'en (x,y) il y a un jetons du joueur analysé
	a = (a_droite + 1 + a_gauche >= 4)	#horizontale
	b = (en_haut + 1 + en_bas >= 4)		#verticale
	c = (diag_nord_ouest + 1 + diag_sud_est >= 4)	#diagonale nord_ouest -> sud_est
	d = (diag_nord_est + 1 + diag_sud_ouest >= 4)	#diagonale nord_est -> sud_ouest
	
	return a or b or c or d	#si il y a au moin 4 jetons aliges d'une meme couleur


def check_win():
	'''
	On cherche si il y a 4 jetons alignés.
	Pour ca on cherche a partire de toutes les position (0 ... X; 0 ... Y) les alignements
	'''
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE

	global score1, score2

	#	Boucle toutes les cases
	for y in range(Y):
		for x in range(X):
			#	Si la case actuelle a un jeton de la couleur du joueur analysé
			if grid[y][x] == tour+1:
				#	On cherche si ce jeton fait partie d'un alignement
				if check_position(y, x):
					
					#	Fin de partie
					showinfo("BRAVO !", f"Le {('rouge' if tour == 0 else 'jaune')} a gagné !")
					
					if tour == 0:
						manches.config(text= str(score1 +1) + str(score2))
					elif tour == 1:
						manches.config(text= str(score1) + str(score2 +1))
						
					#	On reinitialise Toute la grille
					reinit_grid()
def reinit_grid():
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE
	
	for x in range(X):
		for y in range(Y):
			grid[y][x] = 0
			canvas[y][x].delete('all')

def tracer_cercle(y, x, couleur):
	""" trace un cercle correspondant aux paramètres:
	
	variables:
	x y: coordonnées horizontales et verticales
	couleur: correspond à la valeur numérique du joueur
	
	return:
	un cercle dans le graphique"""

	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE
	
	canvas[y][x].create_oval(0,0,ZOOM-1,ZOOM-1, fill= couleur)

#############################

# partie IA

def IA():
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE

	x = 0 		#?

	if IA_MODE == 0:
		disponible_Xs = [x for x in range(X) if any(grid[Y-y-1][x] == 0 for y in range(Y))]
		x = disponible_Xs[randint(0, len(disponible_Xs)-1)]

	elif IA_MODE == 1:	#pour l'instant c'est la meme chose que IA_MODE == 0. Il faut juste que je cherche un endroit ou il y a une suite et puis c'est tout
		disponible_Xs = [x for x in range(X) if any(grid[Y-y-1][x] == 0 for y in range(Y))]
		x = disponible_Xs[randint(0, len(disponible_Xs)-1)]

		#Je changerais apres

	tour_de_jeu(x)


#############################################################

# génération des données


global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_PLAYER0, IA_PLAYER1, IA_MODE

# colonnes
X = 7
# lignes
Y = 6
# dimensions case
ZOOM = 50

# paramètres IA
IA_PLAYER0 = False
IA_PLAYER1 = True
IA_MODE = 0

# fenètre principale
root = tk.Tk()

# liste imbriquée matrice
grid = [[0 for _ in range(X)] for _ in range(Y)]

# joueur 0 = rouge
# joueur 1 = jaune
tour = 0

# pour connaitre le tour du joueur
banniere = []
for x in range(X):
	banniere += [tk.Canvas(root, bg='red', width=ZOOM, height=ZOOM)]
	banniere[-1].grid(row= 0, column= x)


# construction graphique en grille
canvas = []
for y in range(Y):
	canvas += [[]]
	for x in range(X):
		canvas[-1] += [tk.Canvas(root, height=ZOOM, width=ZOOM, bg="white")]
		canvas[-1][-1].grid(row=y+1, column=x)

		# clic dans une colonne x: appel fonction tour_de_jeu(x)
		canvas[-1][-1].bind("<Button-1>", lambda event, x= x: tour_de_jeu(x))

if IA_PLAYER0 == True:
	IA()

###################################

def sauvegarde():

    fic = open("sauvegarde.txt", "w")
    for y in range(Y):
      for x in range(X):
          fic.write(str(grid[y][x]) +"\n")
    fic.close()

s = tk.Button(root, text= "sauvegarde", command= sauvegarde)
s.grid(row= 0, column= X+1)

def charge():

	fic = open("sauvegarde.txt", "r")
	for ligne in fic:
		print(ligne)
	fic.close()

c = tk.Button(root, text= "charge", command= charge)
c.grid(row= 0, column= X+2)

###################################

global score1, score2, n

score1 = 0
score2 = 0

n = 1

manches = tk.Label(root, text = str(score1) + str(score2))
manches.grid(row= 0, column= X+4)

def sets():
	if score1 == n:
		jeux.config(text= "joueur rouge gagnant")
	elif score2 == n:
		jeux.config(text= "joueur jaune gagnant")
        
jeux = tk.Label(root, text= "égalité")
jeux.grid(row= 0, column= X+3)

###################################

# nouvelle partie
# paramètres: X, Y, nbre_jetons_à_aligner (?), n, IA_MODE

###################################

#   Mainloop
root.mainloop()

