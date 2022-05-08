''' Puissance 4 avec une possibilite d'IA.

Tout est centralise dans ce fichier.

Syntaxe : Indentation par tabulations, pas par espaces


Principe Generale :
	Il y a un grille (avec `.grid(row=y,col=x)` et non `.pack()`) de Canvas ou on dessine les jetons.
	On `.bind("<Button-1>", cliquer_sur_la_colone(x))` sur chaque canvas.
	De cette maniere, chaque clique sur Canvas appelle la fonction `cliquer_sur_la_colone(x)`
	et donc lache un jeton dans la colone `x`. Ensuit si le joueur 2nd est une IA, la fonction
	call IA() pour qu'elle place un jeton a la place du joueur 2nd.
	La banniere est mise a jour pour le joueur qui joue.
'''

tour = 0	#A qui est le tour ?

ia_en_train_de_jouer = False

disponible_colors = ['white', 'red', 'blue', 'yellow', 'black']

# === Importer toutes les libs ===

import tkinter as tk
from tkinter.messagebox import showinfo, askyesnocancel
from tkinter import filedialog
from random import randint

def update_graphics():
	delet_banniere()
	delet_grid()

	build_banniere()
	update_banniere()
	build_grid()

def Toplevel_list(names, title="Top"):
	_top = tk.Toplevel()
	_top.title = title
	
	_list = tk.Listbox(_top)
	for i in range(len(names)):
		_list.insert(i+1, names[i])
	_list.pack()

	def put_results():
		global _x 				#_x etant utilise comme variable temporaire
		_x = names[_list.curselection()[0]]
		_top.quit()

	tk.Button(_top, text="Ok", command=put_results).pack()

	_top.mainloop()

# === Fonctions du Menu ===

def ask_XYSIZE():
	global X,Y,SIZE
	variables = ('x', 1, 20, X), ('y', 1, 20, Y), ('size', 10, 100, SIZE)

	_top = tk.Toplevel()

	frames = [tk.Frame(_top) for _ in range(len(variables))]
	for i,(name,from_,to,VAL) in enumerate(variables):
		frames[i].pack()
		tk.Label(frames[i], text=name).grid(row=0,column=0)

	spins = [tk.Spinbox(frames[i], from_=from_, to=to) for i,(name,from_,to,VAL) in enumerate(variables)]
	for i,(name,from_,to,VAL) in enumerate(variables):
		spins[i].grid(row=0, column=1)
		spins[i].delete(0,2)
		spins[i].insert(0, VAL)

	def put_results():
		values = [int(spins[i].get()) for i in range(len(variables))]
		
		global _x,_y,_size

		r = askyesnocancel("Ok ?", "Confirmer la saisie ?")
		if r == None:
			_x,_y,_size = None,None,None
			_top.quit()
			#_top.destroy()
		elif r == True:
			_x,_y,_size = values
			X,Y,SIZE = values#_x,_y,_size
			_top.quit()
			#_top.destroy()
		else:
			pass

	tk.Button(
		_top,
		text="Ok",
		command=put_results
	).pack()

	_top.mainloop()

# = File =
def menu_file_nouveau():
	global X,Y,SIZE,grid,_x,_y,_size
	
	ask_XYSIZE()

	if (_x,_y,_size) == (None,None,None):
		return

	delet_banniere()
	delet_grid()

	X,Y,SIZE = _x,_y,_size
	grid = [[0 for x in range(X)] for y in range(Y)]
	
	build_banniere()
	update_banniere()
	build_grid()

def menu_file_charger():
	global grid,X,Y

	delet_banniere()
	delet_grid()

	with open(filedialog.askopenfilename(initialdir="."), "r") as fic:
		text = fic.read()
		X = len(text.split('\n')[0].strip(',').split(','))

		numbs = text.replace(' ','').replace('\n',',').split(',')
		Y = int(len(numbs)/X)
		
		grid = [[int(numbs[y*X + x]) for x in range(X)] for y in range(Y)]

	build_banniere()
	update_banniere()
	build_grid()

def menu_file_sauvgarder():
	global grid, X,Y
	with open(filedialog.asksaveasfilename(), "w") as fic:
		fic.write(
			'\n'.join(
				','.join(str(grid[y][x]) for x in range(X)) for y in range(Y)
			)
		)

# = Edit =

def menu_edit_1st_color():
	global color_list

	Toplevel_list(disponible_colors, title="1s player")	#store in _x
	color_list[1] = _x

	update_graphics()

def menu_edit_2nd_color():
	global color_list

	Toplevel_list(disponible_colors, title="2nd player")	#store in _x
	color_list[2] = _x

	update_graphics()

def menu_edit_null_color():
	global color_list

	Toplevel_list(disponible_colors, title="Null player")	#store in _x
	color_list[0] = _x

	update_graphics()

def menu_edit_IA():
	global IA_MODE

	ias = ['Jouer Reel', 'Mode Aleatoire', 'IA Inteligente']

	Toplevel_list(ias, title="IA")	#store in _x
	IA_MODE = ias.index(_x)

# = Aide =

def menu_aide_aide():
	_top = tk.Toplevel()
	text = tk.Text(_top)
	_help = '''	Cliquer sur une colone pour glisser un jeton.
Utilisez l'IA dans 2 modes differents : Aleatoire et Inteligente
	'''
	text.insert(tk.INSERT, _help)
	text.pack()
	tk.Button(_top, text="Ok", command=_top.quit)
	_top.mainloop()

# === Fonctions de construction du GUI ===

def build_banniere():
	global root, banniere_frame, color_list, banniere, X, SIZE

	banniere = []
	for x in range(X):
		banniere += [tk.Canvas(banniere_frame, height=SIZE, width=SIZE, bg=color_list[0])]
		banniere[x].bind("<Button-1>", lambda event,x=x: joueur_clique_colone(x))
		banniere[x].grid(row=0, column=x)

def build_menu():
	global root

	menu = tk.Menu(root)

	#	File
	menu_file = tk.Menu(menu, tearoff=0)
	menu_file.add_command(label="Nouveau", command=menu_file_nouveau)
	menu_file.add_command(label="Charger", command=menu_file_charger)
	menu_file.add_command(label="Sauvgarder", command=menu_file_sauvgarder)
	menu.add_cascade(label="File", menu=menu_file)
	
	#	Edit
	menu_edit = tk.Menu(menu, tearoff=0)
	menu_edit.add_command(label="1st Player color", command=menu_edit_1st_color)
	menu_edit.add_command(label="2nd Player color", command=menu_edit_2nd_color)
	menu_edit.add_command(label="Null color", command=menu_edit_null_color)
	menu_edit.add_command(label="2nd Player mode", command=menu_edit_IA)
	menu.add_cascade(label="Edit", menu=menu_edit)

	#	Aide
	menu_aide = tk.Menu(menu, tearoff=0)
	menu_aide.add_command(label="Aide", command=menu_aide_aide)
	menu.add_cascade(label="Aide", menu=menu_aide)

	root.config(menu=menu)
	
def build_grid():
	global root, X,Y,SIZE, grid,canvas, grid_frame

	canvas = []
	for y in range(Y):
		canvas += [[]]
		for x in range(X):
			canvas[-1] += [tk.Canvas(grid_frame, height=SIZE, width=SIZE, bg=color_list[0])]
			canvas[-1][-1].grid(row=y, column=x)
			canvas[-1][-1].bind("<Button-1>", lambda event,x=x: joueur_clique_colone(x))
			
			if grid[y][x] != 0:
				dessiner_jeton(x,y,color_list[grid[y][x]])

# === Fonction de Tour ===

def joueur_clique_colone(x):
	""" effectue un tour du joueur:
	
	- place un jeton dans la colonne souhaitée
	- passe au tour du joueur suivant
	
	variable x:
	
	correspond à l'endroit cliqué sur la fenêtre,
	clic à la colonne souhaitée
	"""

	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_MODE, ia_en_train_de_jouer, color_list

	if ia_en_train_de_jouer:
		return

	y = clic(tour+1, x)	# tour+1 est la couleur (0+1=1=1st, 1+1=2=nd), sauf que on stoque juste 0,1,2 dans grid (pas les couleurs)

	# colonne pleine
	if y == -1:
		showinfo("Impossible", "On ne peut pas staquer plus de Y pièces pas colonnes")

	else:
		# le cercle apparait sur l'image
		dessiner_jeton(x,y, color_list[tour+1])
		# vérifie s'il y a alignement
		check_win()
	
	# tour du joueur suivant
	tour = (tour + 1) % 2

	# modifie la couleur de la bannière pour le prochain joueur
	update_banniere()

	# si le joueur suivant est une IA
	if tour == 1 and IA_MODE > 0:
		#IA()
		ia_en_train_de_jouer = True
		root.after(1000, IA)	#sleep(2)

def clic(grid_joueur, x):
	""" - faire descendre les jetons
		- change les valeurs des cases
	
	variables:
	tour_joueur: valeur numérique de la case dans la matrice
	x: coordonnée horizontale d'une case
	
	return:
	- coordonnée verticale d'une case
	- ou colonne pleine
	"""
	
	global X,Y,grid

	for y in range(Y):
		if grid[Y-y-1][x] == 0:
			grid[Y-y-1][x] = grid_joueur	#1 ou 2
			return Y-y-1
	return -1

# === IA ===

def IA():
	'''
	Apres qu'un vrai joueur ai joué, IA() est lancé pour gliser un jeton
	'''
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_MODE, ia_en_train_de_jouer

	x = 0 		# la colone ou l'IA veut glisser un jeton

	if IA_MODE == 1:
		disponible_Xs = [x for x in range(X) if any(grid[Y-y-1][x] == 0 for y in range(Y))]
		x = disponible_Xs[randint(0, len(disponible_Xs)-1)]

	elif IA_MODE == 2:
		disponible_Xs = [x for x in range(X) if any(grid[Y-y-1][x] == 0 for y in range(Y))]
		x = disponible_Xs[randint(0, len(disponible_Xs)-1)]

	y = clic(2, x)	# tour+1 est la couleur (0+1=1=1st, 1+1=2=nd), sauf que on stoque juste 0,1,2 dans grid (pas les couleurs)

	dessiner_jeton(x,y, color_list[tour+1])
	check_win()
	
	# tour du joueur suivant
	tour = 0

	# modifie la couleur de la bannière pour le prochain joueur
	update_banniere()

	ia_en_train_de_jouer = False

# === Fonctions Graphiques du jeux ===

def update_banniere():
	global banniere, tour, color_list, X,SIZE, color_list
	for x in range(X):
		points = [0,0, SIZE,0, int(SIZE/2),SIZE]
		banniere[x].create_polygon(points, fill=color_list[tour+1])

def dessiner_jeton(x,y,color):
	""" trace un cercle correspondant aux paramètres:
	
	variables:
	x y: coordonnées horizontales et verticales
	color: correspond à la valeur numérique du joueur
	
	return:
	un cercle dans le graphique"""

	global canvas, SIZE
	
	canvas[y][x].create_oval(0,0,SIZE-1,SIZE-1, fill=color)

def delet_grid():
	global X,Y, canvas, grid_frame

	for y in range(Y):
		for x in range(X):
			del canvas[0][0]
		del canvas[0]

	for widget in grid_frame.winfo_children():
		widget.destroy()

	canvas = []

def delet_banniere():
	global X, banniere, banniere_frame
	
	for widget in banniere_frame.winfo_children():
		widget.destroy()
	
	for x in range(X):
		del banniere[0]	#va supprimer tout
	banniere = []

# === Fonctions Logiques ===

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
	global X,Y,ZOOM, root, grid, tour, banniere, canvas, IA_MODE, scores

	#	Boucle toutes les cases
	for y in range(Y):
		for x in range(X):
			#	Si la case actuelle a un jeton de la couleur du joueur analysé
			if grid[y][x] == tour+1:
				#	On cherche si ce jeton fait partie d'un alignement
				if check_position(y, x):
					
					#	Fin de partie
					showinfo("BRAVO !", f"Le {('rouge' if tour == 0 else 'jaune')} a gagné !")
					
					scores[tour] += 1
					manches.config(text=f"Score : {scores[0]} - {scores[1]}")

					if scores[0] == scores[1]:
						jeux.config(text="Egalitee")
					elif scores[0] > scores[1]:
						jeux.config(text="Le 1er joueur a remporte plus de parties !")
					else:
						jeux.config(text="Le 2nd joueur a remporte plus de parties !")
						
					#	On reinitialise Toute la grille
					delet_banniere()
					delet_grid()

					grid = [[0 for x in range(X)] for y in range(Y)]

					build_banniere()
					build_grid()

# === Mainloop ===

scores = [0,0]

X,Y, SIZE = 7,6, 50										#	Parametres de la grille
_x,_y,_size = 0,0,0 									#	Transition variables
tour = 0												#	0 = 1er joueur, 1 = 2nd joueur
banniere, canvas = [], []								#	Liste des widgets	
root, grid_frame, banniere_frame = None,None,None		#	Les conteneur tkinter
IA_MODE = 0 											#	0 = reel 2nd joueur, 1 = aleatoire, 2 = une IA
color_list = ['white', 'red', 'yellow']					#	Couleur des casses ou jetons

if __name__ == "__main__":
	root = tk.Tk()

	grid_frame = tk.Frame(root)
	banniere_frame = tk.Frame(root)

	grid = [[0 for x in range(X)] for y in range(Y)]

	build_menu()
	build_banniere()
	update_banniere()
	build_grid()

	banniere_frame.pack()
	grid_frame.pack()

	manches = tk.Label(root, text="Score : 0-0")
	manches.pack()#grid(row=2,column=0)

	jeux = tk.Label(root, text="Egalitee")
	jeux.pack()#grid(row=3,column=0)

	root.mainloop()
