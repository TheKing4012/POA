import random


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
                    pass
                    # self.grille[y][x] = self.enum_entite["vide"]
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
                elif self.grille[y - 1][x] == self.enum_entite["porte"]["vert"] or self.grille[y - 1][x] == \
                        self.enum_entite["porte"]["rouge"] or self.grille[y + 1][x] == self.enum_entite["porte"][
                    "vert"] or self.grille[y + 1][x] == self.enum_entite["porte"]["rouge"]:
                    self.grille[y][x] = self.enum_entite["vide"]
                elif self.grille[y][x - 1] == self.enum_entite["porte"]["vert"] or self.grille[y][x - 1] == \
                        self.enum_entite["porte"]["rouge"] or self.grille[y][x + 1] == self.enum_entite["porte"][
                    "vert"] or self.grille[y][x + 1] == self.enum_entite["porte"]["rouge"]:
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
                    i = random.randint(1, 100)
                    if i >= 45:
                        self.grille[y][x] = self.enum_entite["mur"]
                    else:
                        self.grille[y][x] = self.enum_entite["vide"]


# Press the green button in the gutter to run the script.


# Press the green button in the gutter to run the script.


if __name__ == '__main__':
    p = plateau(10)
    p.construct_plateau()
    p.print_plateau()
