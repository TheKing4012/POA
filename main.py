import random

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings


class agent:
    position = [0, 0] # position de l'agent x, y
    #tableau des 4 case autour de lui
    neighbour = [[0, 0], [0, 0], [0, 0], [0, 0]] # nord, est, sud, ouest -> x, y
    orientation = {"nord" : 0, "est" : 1, "sud" : 2, "ouest" : 3} # nord : tete, boolean -> orientation actuelle
    inventaire_cle = [False, False] # element 1 : cle rouge, element 2 : cle vert

    def __init__(self, x, y, plateau):
        self.position[0] = x
        self.position[1] = y
        self.neighbour[0] = [x, y - 1]# nord
        self.neighbour[1] = [x + 1, y] # est
        self.neighbour[2] = [x, y + 1] # sud
        self.neighbour[3] = [x - 1, y] # ouest

    # Permet d'avancer en  x y
    # si l'agent peut avancer -> return true sinon false
    def move_forward(self, plateau):
        # verification de la position de l'agent si ce n est pas un mur
        if plateau.grille[self.neighbour[self.orientation["nord"]][0]][self.neighbour[self.orientation["nord"]][1]] != 0:
            self.position[0] = self.neighbour[self.orientation["nord"]][0]
            self.position[1] = self.neighbour[self.orientation["nord"]][1]
            # on met a jour les voisins
            self.neighbour[0] = [self.position[0], self.position[1] - 1]  # nord
            self.neighbour[1] = [self.position[0] + 1, self.position[1]]  # est
            self.neighbour[2] = [self.position[0], self.position[1] + 1]  # sud
            self.neighbour[3] = [self.position[0] - 1, self.position[1]]  # ouest
            return True
        else:
            print(f"impossible d'avancer, il y a un mur...")
            return False

    def left(self):
        # on let a jour ses voisins (neighbour) en decalant les cases des neighbour pour qu'ils correspondent a la nouvelle orientation (ouest = nord, nord = est, est = sud, sud = ouest)
        # copie de neighbour dans un tableau temporaire
        temp = self.neighbour.copy()
        # on met a jour les voisins
        self.neighbour[0] = temp[3]  # nord
        self.neighbour[1] = temp[0]
        self.neighbour[2] = temp[1]
        self.neighbour[3] = temp[2]
        # print(f"nouvelle orientation : {self.orientation}")
        print(f"je tourne a gauche...")
        print(f"nouveau voisin : {self.neighbour}")
        
    def right(self):
        # on let a jour ses voisins (neighbour) en decalant les cases des neighbour pour qu'ils correspondent a la nouvelle orientation (ouest = sud, nord = ouest, est = nord, sud = est)
        # copie de neighbour dans un tableau temporaire
        temp = self.neighbour.copy()
        # on met a jour les voisins
        self.neighbour[0] = temp[1]  # nord
        self.neighbour[1] = temp[2]
        self.neighbour[2] = temp[3]
        self.neighbour[3] = temp[0]
        # print(f"nouvelle orientation : {self.orientation}")
        print(f"je tourne a droite...")
        print(f"nouveau voisin : {self.neighbour}")

    def add_key_bag(self, type_cle):
        if type_cle == 7:
            self.inventaire_cle[0] = True
            self.inventaire_cle[1] = False
        else:
            self.inventaire_cle[1] = True
            self.inventaire_cle[0] = False

    # Permet d'ouvrir une porte
     # si l'agent possede la bonne cle pour ouvrir la porte -> return true sinon false
     # si la porte ne correspond a rien, erreur
    def open_door(self,type_porte):
        if type_porte == 3: # porte rouge
            for i in self.inventaire_cle:
                if self.inventaire_cle[0]:# cle rouge
                    self.inventaire_cle[0] = False
                    return True
            return False
        elif type_porte == 4: #porte vert
            for i in self.inventaire_cle:
                if self.inventaire_cle[1]:#cle vert
                    self.inventaire_cle[1] = False
                    return True
            return False
        else:
            print(f"le type de porte ne correspond à aucune cle...")


# class plateau
class plateau:
    taille = 0
    enum_entite = {"mur": 0, "agent": 1, "cle": {"rouge": 7, "vert": 8}, "porte": {"rouge": 3, "vert": 4}, "vide": 5, "chemin": 11, "sortie": 12}
    grille = []

    def __init__(self, taille):
        self.taille = taille - 2
        self.init_plateau()

    def init_plateau(self):
        for i in range(self.taille):
            self.grille.append([])
            for j in range(self.taille):
                self.grille[i].append(self.enum_entite["mur"])
                      

    def print_plateau(self):
        for j in range(self.taille):
            for i in range(self.taille):
                if self.grille[j][i] == self.enum_entite["vide"]:
                    print("\033[44m  \033[0m", end='')  # Bleu pour le chemin
                elif self.grille[j][i] == self.enum_entite["mur"]:
                    print("\033[47m  \033[0m", end='')  # Blanc pour les murs
                elif self.grille[j][i] == self.enum_entite["cle"]["rouge"]:
                    print("\033[41m  \033[0m", end='')  # Rouge pour la clé rouge
                elif self.grille[j][i] == self.enum_entite["cle"]["vert"]:
                    print("\033[42m  \033[0m", end='')  # Vert pour la clé verte
                """# afffichage des portes
                elif self.grille[j][i] == self.enum_entite["porte"]["rouge"]:
                     # magenta pour la porte rouge
                    print("\033[105m  \033[0m", end='')
                elif self.grille[j][i] == self.enum_entite["porte"]["vert"]:
                     # cyan pour la porte verte
                    print("\033[102m  \033[0m", end='')"""
                # ... (ajoutez des couleurs pour les autres éléments si nécessaire)
            print()  # Nouvelle ligne après chaque rangée

    """def construct_plateau(self):
        doorSet = 0
        keySet = 0
        redDoorSet = 0
        blueDoorSet = 0
        redKeySet = 0
        blueKeySet = 0

        for y in range(self.taille):
            for x in range(self.taille):
                if y == round(self.taille / 2) and x == round(self.taille / 2):
                    self.grille[y][x] = self.enum_entite["vide"]
                elif y == 0 or y == self.taille - 1:
                    if x == 0 or x == self.taille - 1:
                        self.grille[y][x] = self.enum_entite["mur"]
                    elif doorSet != 2:
                        if random.randint(0, 10) % 2 == 1:
                            if redDoorSet == 0:
                                self.grille[y][x] = self.enum_entite["porte"]["rouge"]
                                redDoorSet = 1
                            elif blueDoorSet == 1:
                                self.grille[y][x] = self.enum_entite["porte"]["vert"]
                                blueDoorSet = 1
                            doorSet += 1
                elif x == 0 or x == self.taille - 1:
                    if doorSet != 2:
                        if random.randint(0, 10) % 2 == 1:
                            if redDoorSet == 0:
                                self.grille[y][x] = self.enum_entite["porte"]["rouge"]
                                redDoorSet = 1
                            elif blueDoorSet == 1:
                                self.grille[y][x] = self.enum_entite["porte"]["vert"]
                                blueDoorSet = 1
                            doorSet += 1
                        else:
                            self.grille[y][x] = self.enum_entite["mur"]
                elif self.grille[y - 1][x] == self.enum_entite["porte"]["vert"] or self.grille[y - 1][x] == self.enum_entite["porte"]["rouge"] or self.grille[y + 1][x] == self.enum_entite["porte"]["vert"] or self.grille[y + 1][x] == self.enum_entite["porte"]["rouge"]:
                    self.grille[y][x] = self.enum_entite["vide"]
                elif self.grille[y][x - 1] == self.enum_entite["porte"]["vert"] or self.grille[y][x - 1] == self.enum_entite["porte"]["rouge"] or self.grille[y][x + 1] == self.enum_entite["porte"]["vert"] or self.grille[y][x + 1] == self.enum_entite["porte"]["rouge"]:
                    self.grille[y][x] = x, self.enum_entite["vide"]
                elif keySet != 2:
                    if random.randint(0, 10) % 2 == 1:
                        if redKeySet == 0:
                            self.grille[y][x] = self.enum_entite["cle"]["rouge"]
                            redKeySet = 1
                        elif blueKeySet == 1:
                            self.grille[y][x] = self.enum_entite["cle"]["vert"]
                            blueKeySet = 1
                        keySet += 1
                else:
                    self.grille[y][x] = self.enum_entite["vide"]"""
    
    def get_neighbours(self, x, y):
        neighbours = []
        if x - 2 > 0:
            neighbours.append((x-2, y))
        if x + 2 < self.taille:
            neighbours.append((x+2, y))
        if y - 2 > 0:
            neighbours.append((x, y-2))
        if y + 2 < self.taille:
            neighbours.append((x, y+2))
        return neighbours
    
    def place_keys(self, num_keys):
        # Obtenir toutes les cellules vides
        empty_cells = [(x, y) for x in range(self.taille) for y in range(self.taille) if self.grille[x][y] == self.enum_entite["vide"]]

        # Mélanger la liste de cellules vides
        random.shuffle(empty_cells)

        # Placer les clés
        for i in range(min(num_keys, len(empty_cells))):
            x, y = empty_cells[i]
            # Alterne entre les clés rouges et vertes
            key_type = self.enum_entite["cle"]["rouge"] if i % 2 == 0 else self.enum_entite["cle"]["vert"]
            self.grille[x][y] = key_type
    
    def place_doors_on_edge(self, num_doors):
        # Obtenir toutes les cellules vides qui ont au moins une case vide en tant que voisin et qui sont au bord du plateau
        empty_cells = [(x, y) for x in range(self.taille) for y in range(self.taille) if self.grille[x][y] == self.enum_entite["vide"] and (x == 0 or y == 0 or x == self.taille - 1 or y == self.taille - 1) and self.get_neighbours(x, y)]
        # Mélanger la liste de cellules vides
        random.shuffle(empty_cells)
        # Placer les portes que sur les cellules vides qui ont au moins une case vide en tant que voisin et qui sont au bord du plateau
        for i in range(min(num_doors, len(empty_cells))):
            x, y = empty_cells[i]
            # Alterne entre les portes rouges et vertes
            door_type = self.enum_entite["porte"]["rouge"] if i % 2 == 0 else self.enum_entite["porte"]["vert"]
            self.grille[x][y] = door_type
        


    def construct_plateau(self):
        #self.init_plateau()

        # Choisissez un point de départ
        start_x = random.randint(0, self.taille - 1) // 2 * 2
        start_y = random.randint(0, self.taille - 1) // 2 * 2
        self.grille[start_x][start_y] = self.enum_entite["vide"]

        # Liste des cellules visitées
        visited = [(start_x, start_y)]

        while visited:
            x, y = visited[-1]
            neighbours = [n for n in self.get_neighbours(x, y) if self.grille[n[0]][n[1]] == self.enum_entite["mur"]]
            
            if neighbours:
                nx, ny = random.choice(neighbours)

                # Ouvrez un passage entre les cellules
                self.grille[nx][ny] = self.enum_entite["vide"]
                self.grille[nx + (x - nx) // 2][ny + (y - ny) // 2] = self.enum_entite["vide"]

                visited.append((nx, ny))
            else:
                visited.pop()
        self.place_keys(4)
        # ajouter une collonne au debut et a la fin du plateau(idem pour les lignes)
        # cre d un plateau temporaire
        temp = []
        for i in range(self.taille + 2):
            temp.append([])
            for j in range(self.taille + 2):
                if i == 0 or i == self.taille + 1:
                    temp[i].append(self.enum_entite["mur"])
                else:
                    if j == 0 or j == self.taille + 1:
                        temp[i].append(self.enum_entite["mur"])
                    else:
                        temp[i].append(self.grille[i - 1][j - 1])
        #self.place_doors_on_edge(2)


    def test(self, agent_):
        print("test")
        # plateau.print_plateau()
        plateau.construct_plateau()
        plateau.print_plateau()
        # affichage des plateaux
        # print(f"plateau : {plateau.grille}")
        for i in range(plateau.taille):
            print(f"ligne {i} : {plateau.grille[i]}")
    
        # creation de l'agent
        """agent = agent_
        print(f"position de l'agent : {agent.position}")
        print(f"voisin de l'agent : {agent.neighbour}")
        # deplacement de l'agent
        agent.move_forward(plateau)
        print(f"position de l'agent : {agent.position}")
        print(f"voisin de l'agent : {agent.neighbour}")
        # mise a jour du plateau en fonction de la position de l'agent
        plateau.grille[agent.position[0]][agent.position[1]] = 1
        plateau.print_plateau()"""
        




if __name__ == '__main__':
    print('PyCharm')
    # creation du plateau
    plateau = plateau(10)
    # creation de l'agent
    agent = agent(5, 5, plateau)
    plateau.test(agent)
    

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
