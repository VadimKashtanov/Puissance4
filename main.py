'''
Le principe : 

Habituellement il y a 2 joueurs (rouge jaune) sauf qu'en fait ca change rien de faire 7 joueurs par exemple.
En plus ca sera beaucoup plus clean, et ca sera plus structuree avec des `for`

X,Y - est la taille de la grille.
L - est la taille de la ligne qu'il faut cree pour gagner

PLAYERS - le nombre de joueurs differents
COLORS - les couleurs pour chaque joueure
IA - True/False si c'est une IA ou un joueur (le i-eme joueur)

Tkinter va cree un fenetre avec dedans une banniere (au dessus) qui indique a qui le tour est.
Une grille ou la fonction `update()` va dessiner si il faut des cercles de differents couleurs.
`update()` sera call par une fonction `clik()` qui va etre `.bind()` sur les evenements de tkinter.

'''

# Importer tout les librairies

# Les varibels gloals
global root, X,Y, L, PLAYERS,COLORS, ROUND, GRID, IAMODE
#round - a qui le tour (0 ... n  ou n est la quantite de joueurs)
#GRID = [ [couleur pour x in X] pour y in Y ]
#IAMODE = 0,1,2    (0 = random, 1 = 'logique simple', 2 - avancee)

# [def] qui genere les variables qui seront `global`
def glob():
  # Cree un fenetre qui demande si la personne veut charger une partie depuis un fichier ou non
  # Autrement ca demande les X,Y,L,PLAYERS et COLORS avec une autre fenetre
  # Par default (X,Y) = (6,5)    L=4    
  return tk.Tk(), X,Y,L, PLAYERS,COLORS, 0, GRID, IAMODE

# [def] qui .pack() tous les elements
def pack():
  global root, X,Y, L, PLAYERS,COLORS, ROUND, GRID
  pass

# [def] qui va update les graphics de la fenetre
def update():
  global root, X,Y, L, PLAYERS,COLORS, ROUND, GRID
  pass

#[def] fonction qui check en (x,y) si il y a une ligne (dans les 8 direction) de `L` jettons
def check_if_ligne(color, y,x):
  pass

# [def] fonction simple qui check `GRID`
def find_win(color):
  global GRID
  ret = False
  
  for y in range(Y):
    for x in range(X):
      check_if_ligne(color, y,x)
  
  return ret

# [def] qui finit tout et qui affiche le resultat et la grille avec une droite qui montre ou la joueur a gagnee
def win(who): #click() fait un `for player in range(PLAYERS) : win(i)`     who=i
  global root, X,Y, L, PLAYERS,COLORS, ROUND, GRID
  pass

# [def] fonction qui joue a la place d'un joueur
def IA(who):
  #si il y a une IA apres cette IA alors : IA(i+1), autrement elle ne fait rien, car de toute facon `click`
  
  if IAMODE == 0:
    pass
  elif IAMODE == 1:
    pass
  else: #2
    pass
  
  pass

# [def] qui check a qui est le tour et qui update la grille et call win() call update()
def click(args):
  # Si apres le joueur actuelle il y a une IA, alors IA(i+1)
  pass

####################################################################
################                  Main            ##################
####################################################################

root, X,Y, L, PLAYERS,COLORS, ROUND, GRID, IAMODE = glob()

assert IAMODE in (0,1,2)

root.mainloop()
