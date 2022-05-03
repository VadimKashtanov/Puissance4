import tkinter as tk
import random

#<vadim> cette partie de tkinter permet d'afficher des info facilement dans une fenetre
from tkinter.messagebox import showinfo
#<vadim> ou d'ouvrire un fichier avec le gestionnaire de fichier local
from tkinter.filedialog import askopenfile

nbre_colonne = 7
nbre_ligne = 6

couleur_joueur1 = "yellow"
couleur_joueur2 = "red"
couleur_vide = "white"

tour_joueur = 0
début_partie = False


grille = []

def création_grille():
    global grille
    for i in range(nbre_colonne):
        grille.append([])
        for j in range(nbre_ligne):
            grille[i].append(0)
    return grille
    
def affiche_grille():

    for i in range(7):
        for j in range(6):

            if grille[i][j] == 0:
                coul = "white"
            if grille[i][j] == 1:
                coul = "yellow"
            if grille[i][j] == 2:
                coul = "red"

            larg = 100
            haut = 100

            x1 = i * larg
            y1 = j * haut
            x2 = (i+1) * larg
            y2 = (j+1) * haut

            tableau.create_oval((x1, y1), (x2,y2), fill = coul)



def placer_jeton(event):
    global tour_joueur
    if début_partie == True:
        for i in range(7):
            if 100 * i < event.x < 100 * (i+1):
                
                j = 0
                while j < 6 and grille[i][j] == 0:
                            if j > 0:
                                grille[i][j-1] = 0
                            if tour_joueur == 0:
                                grille[i][j] = 1
                            if tour_joueur == 1:
                                grille[i][j] = 2
                            j += 1
                
                tour_joueur = 1 - tour_joueur
                texte_joueur()
    
    grille_pleine()
    #alignement()
    affiche_grille()

def grille_pleine():
    cpt = 0
    for i in range(0,7):
        for j in range(0,6):
            if grille[i][j] == 1 or grille[i][j] == 2:
                cpt += 1
    if cpt == (7*6):
        texte_gagné_ou_nul.config(text="NUL")
        début_partie = False

def grille_vide():
    for i in range(0,7):
        for j in range(0,6):
            grille[i][j] = 0



def tirage():
    grille_vide()
    affiche_grille()
    global début_partie
    global tour_joueur
    tour_joueur = random.randint(0,1)
    début_partie = True
    texte_joueur()
   


def texte_joueur():
    if tour_joueur == 0:
        tour.config(text= "tour joueur jaune", bg ="yellow")
    if tour_joueur == 1:
        tour.config(text = "tour joueur rouge", bg = "red")

    

def alignement():
    if ... :
        
        texte_gagné_ou_nul.config(text="GAGNE")
        début_partie = False

    pass




def charger():
    global grille, nbre_colonne, nbre_ligne
    with open(askopenfile(title="Select a file", filetypes=[("all files","*.*")]), "r") as FILE:
        contenue = [int(i) for i in FILE.read().split(',')]
        X = contenue[0]
        Y = contenue[1]
        grille_fichier = contenue[2:]
        grille = [[grille_fichier[y*X + x] for x in range(X)] for y in range(Y)]
        nbre_colonne = X
        nbre_ligne = Y

def sauvegarder():
    pass

def annuler():
    pass


racine = tk.Tk()
tableau = tk.Canvas(racine, bg = "blue", width = 700, height = 600)
tableau.grid(column = 1, row = 0,rowspan=10)

bouton_début = tk.Button(racine, text= "nouvelle partie", command= tirage)
bouton_début.grid(row = 0)

tour = tk.Label(racine, text = "tour joueur")
tour.grid(row = 1)

texte_gagné_ou_nul = tk.Label(racine,text = "" )
texte_gagné_ou_nul.grid(row = 4)

charger = tk.Button(racine, text = "charger", command = charger)
sauvegarder = tk.Button(racine, text = "sauvegarder", command = sauvegarder)
annuler = tk.Button(racine, text = "annuler", command = annuler)

charger.grid(column = 2,row = 0)
sauvegarder.grid(column = 2,row = 1)
annuler.grid(column = 2,row = 2)

tableau.bind("<Button-1>", placer_jeton)

création_grille()
affiche_grille()




racine.mainloop()
