import random
import tkinter as tk
from tkinter import font as tkfont
from tkinter import font as tkfont
import numpy as np



##########################################################################
#
#   Partie I : variables du jeu  -  placez votre code dans cette section
#
#########################################################################


# Plan du labyrinthe

# 0 vide
# 1 mur
# 2 maison des fantomes (ils peuvent circuler mais pas pacman)

# transforme une liste de liste Python en TBL numpy équivalent à un tableau 2D en C
def CreateArray(L):
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  ## ainsi, on peut écrire TBL[x][y] (accès aux éléments)
    return T
    T = np.array(L, dtype=np.int32)
    T = T.transpose()  ## ainsi, on peut écrire TBL[x][y] (accès aux éléments)
    return T


TBL = CreateArray([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 2, 2, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 2, 2, 2, 2, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
# attention, on utilise TBL[x][y]

HAUTEUR = TBL.shape[1]
LARGEUR = TBL.shape[0]


# placements des pacgums et des fantomes

def PlacementsGUM():  # placements des pacgums
    GUM = np.zeros(TBL.shape, dtype=np.int32)  # Conversion de la liste de listes en tableau de numpy de int
    # Parcours chaque case du tab TBL
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 0):
                GUM[x][y] = 1  # Placement d'une Pac-Gomme
    return GUM


GUM = PlacementsGUM()


def updateDistance(carte):
    ok = True
    while ok:
        ok = True
        for x in range(LARGEUR):
            for y in range(HAUTEUR):
                if GUM[x][y] == 1:
                    carte[x][y] = 0
                    continue
                if GUM[x][y] == 0 and carte[x][y] == 0:
                    carte[x][y] = 100
                if x - 1 >= 0 and carte[x][y] < carte[x-1][y] and carte[x - 1][y] != 1000:
                    carte[x][y] = carte[x - 1][y] + 1
                    ok = True
                    continue
                if x + 1 < LARGEUR and carte[x][y] < carte[x+1][y] and carte[x + 1][y] != 1000:
                    carte[x][y] = carte[x + 1][y] + 1
                    ok = True
                    continue
                if y - 1 >= 0 and carte[x][y - 1] != 1000 and carte[x][y - 1] != 100:
                    carte[x][y] = carte[x][y - 1] + 1
                    ok = True
                    continue
                if y + 1 < HAUTEUR and carte[x][y + 1] != 1000 and carte[x][y + 1] != 100:
                    carte[x][y] = carte[x][y + 1] + 1
                    ok = True
                    continue
    return carte


# Fonction pour calculer la carte des distances
def carteDeplacement():
    M = LARGEUR * HAUTEUR  # Les cases du parcours, nombre de cases totales du labyrinthe : 220 < 1000
    G = 1000  # Les cases correspondantes aux murs : Valeur très grande
    P = 0  # Les cases des Pac-Gommes : 0
    carte = np.full(TBL.shape, M, dtype=np.int32)  # Initialisation avec les valeurs de M
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if TBL[x][y] == 1:  # Murs
                carte[x][y] = G
            elif GUM[x][y] == 1:  # Gums
                carte[x][y] = 0
    return carte


PacManPos = [5, 5]
carteDeplacement()

Ghosts = []
#Ajout d'une value direction
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "pink", "up"])
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "orange", "up"])
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "cyan", "up"])
Ghosts.append([LARGEUR // 2, HAUTEUR // 2, "red", "up"])

##############################################################################
#
#  Debug : ne pas toucher (affichage des valeurs autours dans les cases

LTBL = 100
TBL1 = [["" for i in range(LTBL)] for j in range(LTBL)]
TBL2 = [["" for i in range(LTBL)] for j in range(LTBL)]


# info peut etre une valeur / un string vide / un string...
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0: return
    if y < 0: return
    if x >= LTBL: return
    if y >= LTBL: return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0: return
    if y < 0: return
    if x >= LTBL: return
    if y >= LTBL: return
    TBL2[x][y] = info
def SetInfo1(x, y, info):
    info = str(info)
    if x < 0: return
    if y < 0: return
    if x >= LTBL: return
    if y >= LTBL: return
    TBL1[x][y] = info


def SetInfo2(x, y, info):
    info = str(info)
    if x < 0: return
    if y < 0: return
    if x >= LTBL: return
    if y >= LTBL: return
    TBL2[x][y] = info


##############################################################################
#
#   Partie II :  AFFICHAGE -- NE PAS MODIFIER  jusqu'à la prochaine section
#
##############################################################################

ZOOM = 40  # taille d'une case en pixels
EPAISS = 8  # epaisseur des murs bleus en pixels

screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM
screeenWidth = (LARGEUR + 1) * ZOOM
screenHeight = (HAUTEUR + 2) * ZOOM

Window = tk.Tk()
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenetre
Window.geometry(str(screeenWidth) + "x" + str(screenHeight))  # taille de la fenetre
Window.title("ESIEE - PACMAN")

# gestion de la pause

PAUSE_FLAG = False

PAUSE_FLAG = False


def keydown(e):
    global PAUSE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG


    global PAUSE_FLAG
    if e.char == ' ':
        PAUSE_FLAG = not PAUSE_FLAG


Window.bind("<KeyPress>", keydown)

# création de la frame principale stockant plusieurs pages

F = tk.Frame(Window)
F.pack(side="top", fill="both", expand=True)
F.grid_rowconfigure(0, weight=1)
F.grid_columnconfigure(0, weight=1)

# gestion des différentes pages

ListePages = {}
PageActive = 0



def CreerUnePage(id):
    Frame = tk.Frame(F)
    ListePages[id] = Frame
    Frame.grid(row=0, column=0, sticky="nsew")
    return Frame



def AfficherPage(id):
    global PageActive
    PageActive = id
    ListePages[id].tkraise()




def WindowAnim():
    PlayOneTurn()
    Window.after(333, WindowAnim)

    Window.after(333, WindowAnim)


Window.after(100, WindowAnim)
Window.after(100, WindowAnim)

# Ressources

PoliceTexte = tkfont.Font(family='Arial', size=22, weight="bold", slant="italic")

# création de la zone de dessin

Frame1 = CreerUnePage(0)

canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas = tk.Canvas(Frame1, width=screeenWidth, height=screenHeight)
canvas.place(x=0, y=0)
canvas.configure(background='black')


#  FNT AFFICHAGE

def To(coord):
    return coord * ZOOM + ZOOM


    return coord * ZOOM + ZOOM


# dessine l'ensemble des éléments du jeu par dessus le décor

anim_bouche = 0
animPacman = [5, 10, 15, 10, 5]
animPacman = [5, 10, 15, 10, 5]


def Affiche(PacmanColor, message):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 1 and TBL[x + 1][y] == 1):
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")
def Affiche(PacmanColor, message):
    global anim_bouche

    def CreateCircle(x, y, r, coul):
        canvas.create_oval(x - r, y - r, x + r, y + r, fill=coul, width=0)

    canvas.delete("all")

    # murs

    for x in range(LARGEUR - 1):
        for y in range(HAUTEUR):
            if (TBL[x][y] == 1 and TBL[x + 1][y] == 1):
                xx = To(x)
                xxx = To(x + 1)
                yy = To(y)
                canvas.create_line(xx, yy, xxx, yy, width=EPAISS, fill="blue")

    for x in range(LARGEUR):
        for y in range(HAUTEUR - 1):
            if (TBL[x][y] == 1 and TBL[x][y + 1] == 1):
                xx = To(x)
                yy = To(y)
                yyy = To(y + 1)
                canvas.create_line(xx, yy, xx, yyy, width=EPAISS, fill="blue")

    # pacgum
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if (GUM[x][y] == 1):
                xx = To(x)
                yy = To(y)
                e = 5
                canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill="orange")

    # extra info
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x)
            yy = To(y) - 11
            txt = TBL1[x][y]
            canvas.create_text(xx, yy, text=txt, fill="white", font=("Purisa", 8))

    # extra info 2
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            xx = To(x) + 10
            yy = To(y)
            txt = TBL2[x][y]
            canvas.create_text(xx, yy, text=txt, fill="yellow", font=("Purisa", 8))

    # dessine pacman
    xx = To(PacManPos[0])
    yy = To(PacManPos[1])
    e = 20
    anim_bouche = (anim_bouche + 1) % len(animPacman)
    ouv_bouche = animPacman[anim_bouche]
    tour = 360 - 2 * ouv_bouche
    canvas.create_oval(xx - e, yy - e, xx + e, yy + e, fill=PacmanColor)
    canvas.create_polygon(xx, yy, xx + e, yy + ouv_bouche, xx + e, yy - ouv_bouche, fill="black")  # bouche

    # dessine les fantomes
    dec = -3
    for P in Ghosts:
        xx = To(P[0])
        yy = To(P[1])
        e = 16

        coul = P[2]
        # corps du fantome
        CreateCircle(dec + xx, dec + yy - e + 6, e, coul)
        canvas.create_rectangle(dec + xx - e, dec + yy - e, dec + xx + e + 1, dec + yy + e, fill=coul, width=0)

        # oeil gauche
        CreateCircle(dec + xx - 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx - 7, dec + yy - 8, 3, "black")

        # oeil droit
        CreateCircle(dec + xx + 7, dec + yy - 8, 5, "white")
        CreateCircle(dec + xx + 7, dec + yy - 8, 3, "black")

        dec += 3

    # texte
    canvas.create_text(screeenWidth // 2, screenHeight - 50, text="PAUSE : PRESS SPACE", fill="yellow",
                       font=PoliceTexte)
    canvas.create_text(screeenWidth // 2, screenHeight - 20, text=message, fill="yellow", font=PoliceTexte)


AfficherPage(0)




#########################################################################
#
#  Partie III :   Gestion de partie   -   placez votre code dans cette section
#
#########################################################################

def PacManPossibleMove():
    global score
    L = []
    x, y = PacManPos
    if (TBL[x][y - 1] == 0 and GUM[x][y - 1] == 1):
        L.append((0, -1))
        GUM[x][y - 1] = 0
        score += 100
        return L
    if (TBL[x][y + 1] == 0 and GUM[x][y + 1] == 1):
        L.append((0, 1))
        GUM[x][y + 1] = 0
        score += 100
        return L
    if (TBL[x + 1][y] == 0 and GUM[x + 1][y] == 1):
        L.append((1, 0))
        GUM[x + 1][y] = 0
        score += 100
        return L
    if (TBL[x - 1][y] == 0 and GUM[x - 1][y] == 1):
        L.append((-1, 0))
        GUM[x - 1][y] = 0
        score += 100
        return L
    if (TBL[x][y - 1] == 0):
        L.append((0, -1))
    if (TBL[x][y + 1] == 0):
        L.append((0, 1))
    if (TBL[x + 1][y] == 0):
        L.append((1, 0))
    if (TBL[x - 1][y] == 0 and GUM[x - 1][y] == 1):
        L.append((-1, 0))

    return L


def GhostsPossibleMove(x, y):
    L = []
    if (TBL[x][y - 1] == 2): L.append((0, -1))
    if (TBL[x][y + 1] == 2): L.append((0, 1))
    if (TBL[x + 1][y] == 2): L.append((1, 0))
    if (TBL[x - 1][y] == 2): L.append((-1, 0))
    return L


def IAPacman():
    global PacManPos, Ghosts, carteDistance
    #deplacement Pacman
    L = PacManPossibleMove()
    choix = random.randrange(len(L))
    PacManPos[0] += L[choix][0]
    PacManPos[1] += L[choix][1]
    carteDistance = updateDistance(carteDistance)
    # juste pour montrer comment on se sert de la fonction SetInfo1
    for x in range(LARGEUR):
        for y in range(HAUTEUR):
            if carteDistance[x][y] < 1000:
                SetInfo1(x, y, carteDistance[x][y])
            else : SetInfo1(x, y, "")
            """ 
         if GUM[x][y] == 1:
            difX = x - PacManPos[0]
            difX = difX if difX > 0 else -difX
            difY = y - PacManPos[1]
            difY = difY if difY > 0 else -difY
            if difX + difY > 0: info =  x - PacManPos[0] + y - PacManPos[1]
            else : info = -(difX + difY)
            SetInfo1(x,y,info)
         """


def IAGhosts():
    for ghost in Ghosts:
        x, y, color, direction = ghost

        possible_moves = GhostsPossibleMove(x, y)

        if direction == "up" and "down" in possible_moves:
            possible_moves.remove("down")
        elif direction == "down" and "up" in possible_moves:
            possible_moves.remove("up")
        elif direction == "left" and "right" in possible_moves:
            possible_moves.remove("right")
        elif direction == "right" and "left" in possible_moves:
            possible_moves.remove("left")

        new_direction = random.choice(possible_moves)
        if new_direction == "up":
            ghost[1] -= 1
        elif new_direction == "down":
            ghost[1] += 1
        elif new_direction == "left":
            ghost[0] -= 1
        elif new_direction == "right":
            ghost[0] += 1

        ghost[3] = new_direction
def checkCollision():
    for F in Ghosts:
        if PacManPos[0] == F[0] and PacManPos[1] == F[1]:
            return True
    return False


# Boucle principale de votre jeu appelée toutes les 500ms

iteration = 0




def PlayOneTurn():
    global iteration, PAUSE_FLAG

    if not PAUSE_FLAG:
        iteration += 1
        if iteration % 2 == 0:
            IAPacman()
        else:
            IAGhosts()

        if checkCollision():
            PAUSE_FLAG = True
            Affiche(PacmanColor="yellow", message="Collision detected! Game Over.")
        else:
            Affiche(PacmanColor="yellow", message="")


###########################################:
# demarrage de la fenetre - ne pas toucher

Window.mainloop()

