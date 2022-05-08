''' Puissance 4 avec une possibilite d'IA.

Tout est centralise dans ce fichier.

Syntaxe : Indentation par tabulations, pas par espaces

'''

tour = 0	#A qui est le tour ?

# === Importer toutes les libs ===

# === Fonctions du Menu ===

def ask_XY():
	pass

def build_new_board():
	for x in range(X):

# = File =
def menu_file_nouveau():
	pass

def menu_file_charger():
	pass

def menu_file_sauvgarder():
	pass

# = Edit =

def menu_edit_IA():
	pass

# = Aide =

def menu_aide_aide():
	pass

# === Fonctions de construction du GUI ===

def build_banniere():
	pass

def build_menu():
	menu = tk.Menu(root)

	#	File
	menu_file = tk.Menu(menu, tearoff=0)
	menu_file.add_command(label="Nouveau", command=menu_file_new)
	menu_file.add_command(label="Charger", command=menu_file_load)
	menu_file.add_command(label="Sauvgarder", command=menu_file_save)
	menu.add_cascade(label="File", menu=menu_file)
	
	#	Edit
	menu_edit = tk.Menu(menu, tearoff=0)
	menu_edit.add_command(label="2nd Player mode")
	menu.add_cascade(label="Edit", menu=menu_edit)

	#	Aide
	menu_aide = tk.Menu(menu, tearoff=0)
	menu_aide.add_command(label="Aide", command=toplevel_aide)
	menu.add_cascade(label="Aide", menu=menu_aide)
	
	
def build_grid(_X,_Y,_grid):
	pass

# === Fonction de Tour ===

# === IA ===

# === Fonctions Graphiques du jeux ===

def update_banniere():
	pass

def build_grid():
	global X,Y,canvas
	canvas = []
	for y in range(Y):
		canvas[-1] += [[]]
		for x in range(X):
			canvas[-1] += [tk.Canvas(root, height=ZOOM, width=ZOOM, bg="white")]

def delet_grid():
	global X,Y, canvas
	
	for y in range(Y):
		for x in range(X):
			canvas[y][x].delete('all')
			del canvas[y][x]
		del canvas[y]
	del canvas
			
def bind_events():
	global X,Y,canvas
	
	for y in range(Y):
		for x in range(X):
			canvas[y][x].bind("<Button-1>", lambda event, x= x: tour_de_jeu(x))

# === Fonctions Logiques ===

# === Mainloop ===

X,Y, SIZE = 7,6, 50											#	Parametres de la grille
tour = 0													#	0 = 1er joueur, 1 = 2nd joueur
banniere, canvas = None, None, None							#	Liste des widgets	
root, grid_frame, banniere_frame = None,None,None,None		#	Les conteneur tkinter
IAMODE = 0 													#	0 = reel 2nd joueur, 1 = aleatoire, 2 = une IA
color_null, color_1er, color_2nd = 'white', 'red', 'yellow'	#	Couleur des casses ou jetons
if __name__ == "__main__":
	root = tk.Tk()
	
	root.mainloop()
