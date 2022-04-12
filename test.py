import tkinter as tk
from tkinter.messagebox import showinfo

X,Y = 7,6
ZOOM = 50

class Main:
	def __init__(self):
		self.root = tk.Tk()

		self.grid = [[0 for _ in range(X)] for _ in range(Y)]
		self.tour = 0 #0=red, 1=yellow

		#   Banniere rouge ou jaune
		self.banniere = []
		for x in range(X):
			self.banniere += [tk.Canvas(self.root, bg='red', width=ZOOM, height=ZOOM)]
			self.banniere[-1].grid(row=0, column=x)

		#   Buttons
		#for x in range(X):
		#	tk.Button(self.root, text='V', command=lambda x=x:self.update(x)).grid(row=1, column=x)
		
		#   Build grid
		self.canvas = []
		for y in range(Y):
			self.canvas += [[]]
			for x in range(X):
				self.canvas[-1] += [tk.Canvas(self.root, height=ZOOM, width=ZOOM, bg='white')]
				self.canvas[-1][-1].grid(row=y+1, column=x)
				self.canvas[-1][-1].bind("<Button-1>", lambda event, x=x:self.update(x))#eval(f"lambda *args: self.update(self, {x})"))

		#   Mainloop
		self.root.mainloop()

	def update(self, x):
		y = self.push(self.tour+1, x)
		if y == -1:
			showinfo('Impossible', 'On ne peut pas staquer plus de 5 piece pas colones')
		else:
			self.put_circle(y, x, ('red' if self.tour==0 else 'yellow'))
			self.check_win()

		#Modifier la banniere pour le prochain
		for x in range(X):
			self.banniere[x].config(bg=('red' if self.tour == 1 else 'yellow'))

		self.tour = (1 if self.tour == 0 else 0)

		########### IA ###########
        
	def push(self, red_or_blue, x):
		for y in range(Y):
			if self.grid[Y-y-1][x] == 0:
				self.grid[Y-y-1][x] = red_or_blue
				return Y-y-1
		return -1

	def ligne(self, _sum, y, x, __y, __x):
		if X == x  or x < 0 or Y == y  or y < 0:
			return _sum
		elif self.grid[y][x] == self.tour+1:
			return self.ligne(_sum+1, y+__y, x+__x, __y, __x)
		else:
			return _sum

	def check_position(self, y, x):
		a_droite = self.ligne(0, y, x+1, 0, 1)
		a_gauche = self.ligne(0, y, x-1, 0, -1)
		en_haut = self.ligne(0, y-1, x, -1, 0)
		en_bas = self.ligne(0, y+1, x, 1, 0)
		diag_nord_ouest = self.ligne(0, y-1, x-1, -1, -1)
		diag_nord_est = self.ligne(0, y-1, x+1, -1, 1)
		diag_sud_ouest = self.ligne(0, y+1, x-1, 1, -1)
		diag_sud_est = self.ligne(0, y+1, x+1, 1, 1)

		a = (a_droite + 1 + a_gauche == 4)
		b = (en_haut + 1 + en_bas == 4)
		c = (diag_nord_ouest + 1 + diag_sud_est == 4)
		d = (diag_nord_est + 1 + diag_sud_ouest == 4)

		return a or b or c or d

	def check_win(self):
		for y in range(Y):
			for x in range(X):
				if self.grid[y][x] == self.tour+1:
					if self.check_position(y, x):
						showinfo('BRAVO !', f"Le {('rouge' if self.tour==0 else 'jaune')} a gagné !")
						exit()

	def put_circle(self, y, x, color):
		self.canvas[y][x].create_oval(0,0,49,49, fill=color)
		#for _ in range(Y):
		#	print(self.grid[_])

if __name__ == "__main__":
	root = tk.Tk()
	root
	sX = tk.Spinbox(root, from_=0, to=20)
	sY = tk.Spinbox(root, from_=0, to=20)
	sZOOM = tk.Spinbox(root, from_=0, to=50)
	sX.grid(row=0, column=0)
	sY.grid(row=0, column=1)
	sZOOM.grid(row=0, column=2)
	root.mainloop()

	X,Y,ZOOM = int(sX.get()), int(sY.get()), int(sZOOM.get())

	Main()
