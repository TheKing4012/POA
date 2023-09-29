import random

# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings


class agent:
    position = [0, 0]
    orientation = {"nord" : [0, True], "est" : [1, False], "sud" : [2, False], "ouest" : [3, False]} # nord : tete, boolean -> orientation actuelle
    inventaire_cle = [False, False] # element 1 : cle rouge, element 2 : cle vert

    def __init__(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def reload_orientation(self):
        for key, element in self.orientation.items():
            if element[1]:
                element[1] = False

    def move_forward(self, x, y):
        self.position[0] = x
        self.position[1] = y

    def backround(self):
        self.reload_orientation()
        self.orientation["sud"][1] = True

    def left(self):
        self.reload_orientation()
        self.orientation["ouest"][1] = True

    def right(self):
        self.reload_orientation()
        self.orientation["est"][1] = True

    def add_key_bag(self, type_cle):
        if type_cle == 7:
            self.inventaire_cle[0] = True
            self.inventaire_cle[1] = False
        else:
            self.inventaire_cle[1] = True
            self.inventaire_cle[0] = False




# class plateau
class plateau:
    taille = 0
    enum_entite = {"mur": 0, "agent": 1, "cle": {"rouge": 7, "vert": 8}, "porte": {"rouge": 3, "vert": 4}, "vide": 5}
    grille = []

    def __init__(self, taille):
        self.taille = taille
        self.init_plateau()

    def init_plateau(self):
        for i in range(self.taille):
            self.grille.append([])
            for j in range(self.taille):
                self.grille[i].append(self.enum_entite["mur"])

    def print_plateau(self):
        for j in range(self.taille):
            print(self.grille[j])

    def construct_plateau(self):
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
                    self.grille[y][x] = self.enum_entite["vide"]


if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
