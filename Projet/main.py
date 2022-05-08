import tkinter as tk

from gui import build_gui

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

if __name__ == "__main__":
    X,Y = 7,6
	SIZE = 50
    IAMODE = 0  #0 = 2nd joueur, 1 = aleatoire, 2 = une certaine inteligence

	GRID, GRID_FRAM, GRID_CANVAS = None, None, None
	
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

	root.mainloop()
