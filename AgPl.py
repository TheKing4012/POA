import random
import colorama

class agent:
    position = [0, 0] # position de l'agent x, y
    #tableau des 4 case autour de lui
    neighbour = [[0, 0], [0, 0], [0, 0], [0, 0]] # nord, est, sud, ouest -> x, y
    orientation = {"nord" : 0, "est" : 1, "sud" : 2, "ouest" : 3} # nord : tete, boolean -> orientation actuelle
    inventaire_cle = [False, False] # element 1 : cle rouge, element 2 : cle vert
    mon_orientation = "nord"

    def __init__(self, x, y, plateau):
        self.position[0] = x
        self.position[1] = y
        self.neighbour[0] = [x, y - 1]# nord
        self.neighbour[1] = [x + 1, y] # est
        self.neighbour[2] = [x, y + 1] # sud
        self.neighbour[3] = [x - 1, y] # ouest
    
    def mise_a_jour_voisin_changement_pos(self):
        self.neighbour[0] = [self.position[0], self.position[1] - 1]
        self.neighbour[1] = [self.position[0] + 1, self.position[1]]
        self.neighbour[2] = [self.position[0], self.position[1] + 1]
        self.neighbour[3] = [self.position[0] - 1, self.position[1]]

    # Permet d'avancer en  x y
    # si l'agent peut avancer -> return true sinon false
    def move_forward(self, grille):
        # verification de la position de l'agent si ce n est pas un mur
        if grille[self.neighbour[self.orientation[self.mon_orientation]][0]][self.neighbour[self.orientation[self.mon_orientation]][1]] != 0:
            self.position[0] = self.neighbour[self.orientation[self.mon_orientation]][0]
            self.position[1] = self.neighbour[self.orientation[self.mon_orientation]][1]
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
        if self.mon_orientation == "nord":
            self.mon_orientation = "est"
        if self.mon_orientation == "est":
            self.mon_orientation = "sud"
        if self.mon_orientation == "sud":
            self.mon_orientation = "ouest"
        if self.mon_orientation == "ouest":
            self.mon_orientation = "nord"

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
        if self.mon_orientation == "nord":
            self.mon_orientation = "ouest"
        if self.mon_orientation == "ouest":
            self.mon_orientation = "sud"
        if self.mon_orientation == "sud":
            self.mon_orientation = "est"
        if self.mon_orientation == "est":
            self.mon_orientation = "nord"
        print(f"je tourne a droite...")
        print(f"nouveau voisin : {self.neighbour}")

    def add_key_bag(self, type_cle):
        type_cle  = 0
        if type_cle == 7:
            self.inventaire_cle[0] = True
            if self.inventaire_cle[1]:
                type_cle = 8
            self.inventaire_cle[1] = False
        else:
            self.inventaire_cle[1] = True
            if self.inventaire_cle[0]:
                type_cle = 7
            self.inventaire_cle[0] = False
        return type_cle

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

class plateau:
    taille = 0
    enum_entite = {"mur": 0, "agent": 1, "cle": {"rouge": 7, "vert": 8}, "porte": {"rouge": 3, "vert": 4}, "vide": 5}
    grille = []
    non_connected_doors = []
    array_cle = [] # liste des cle contenue dans le labyrinthe (une case vide peut avoir une cle)
    array_porte = [] # liste des portes contenue dans le labyrinthe (une case porte peut avoir un agent dessus)

    def __init__(self, taille):
        self.taille = taille
        self.init_plateau()

    def init_plateau(self):
        for i in range(self.taille):
            self.grille.append([])
            for j in range(self.taille):
                self.grille[i].append(self.enum_entite["mur"])
                      
    def print_plateau(self):
        for i in range(self.taille):
            for j in range(self.taille):
                if self.grille[i][j] == self.enum_entite["agent"]:
                    print(colorama.Fore.BLUE + "██", end="")
                else:
                    if self.grille[i][j] == self.enum_entite["porte"]["rouge"]:
                        # couleur rose
                        print(colorama.Fore.MAGENTA + "██", end="")
                    elif self.grille[i][j] == self.enum_entite["porte"]["vert"]:
                        # couleur  jauune
                         print(colorama.Fore.YELLOW + "██", end="")
                    elif self.grille[i][j] == self.enum_entite["mur"]:
                        print(colorama.Fore.WHITE + "██", end="")
                    elif self.grille[i][j] == self.enum_entite["cle"]["rouge"]:
                        print(colorama.Fore.RED + "██", end="")
                    elif self.grille[i][j] == self.enum_entite["cle"]["vert"]:
                        print(colorama.Fore.GREEN + "██", end="")
                    elif self.grille[i][j] == self.enum_entite["vide"]:
                        print(colorama.Fore.BLACK + "██", end="")
                    # ... (ajoutez des couleurs pour les autres éléments si nécessaire)
            print()  # Nouvelle ligne après chaque rangée
    
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
            # sauvegarde de la position de la clé
            self.array_cle.append((x, y, key_type))
    
    def place_doors_on_edge(self, num_doors):
        # Créer une liste des positions possibles sur les bords
        top_edge = [(0, y) for y in range(1, self.taille-1)]
        bottom_edge = [(self.taille-1, y) for y in range(1, self.taille-1)]
        left_edge = [(x, 0) for x in range(1, self.taille-1)]
        right_edge = [(x, self.taille-1) for x in range(1, self.taille-1)]
        edge_positions = top_edge + bottom_edge + left_edge + right_edge

        # Mélanger la liste
        random.shuffle(edge_positions)

        # Placer les portes
        for i in range(min(num_doors, len(edge_positions))):
            x, y = edge_positions[i]
            # Alterne entre les portes rouges et vertes
            door_type = self.enum_entite["porte"]["rouge"] if i % 2 == 0 else self.enum_entite["porte"]["vert"]
            self.grille[x][y] = door_type
            # sauvegarde de la position de la porte
            self.non_connected_doors.append((x, y))
            # sauvegarde de la position de la porte
            self.array_porte.append((x, y, door_type))

    # savoir quelles portes sont connectées au labyrinthe
    def connect_doors_to_maze(self):
        # parcourir grille et trouver porte
        for x in range(self.taille):
            for y in range(self.taille):
                if self.grille[x][y] in [self.enum_entite["porte"]["rouge"], self.enum_entite["porte"]["vert"]]:
                    # Trouver tous les voisins qui sont des murs
                    neighbours = [n for n in self.get_direct_neighbours(x, y) if self.grille[n[0]][n[1]] == self.enum_entite["vide"]]
                    
                    # Si un voisin est une case vide, alors nous avons connecté la porte au labyrinthe
                    for nx, ny in neighbours:
                        if self.grille[nx][ny] == self.enum_entite["vide"]:
                          #self.grille[x][y] = self.enum_entite["vide"]
                          self.non_connected_doors.remove((x, y))
                          break

    # fonction qui etend le labyrinthe a partir des portes         
    def expand_from_door(self, door_x, door_y):
        # recup case vide 
        empty_cells = [(x, y) for x in range(self.taille) for y in range(self.taille) if self.grille[x][y] == self.enum_entite["vide"]]
        # Liste pour suivre les cellules à explorer
        to_expand = [(door_x, door_y)]
        visited = set()

        while to_expand:
            x, y = to_expand.pop()
            visited.add((x, y))

            # Obtenez les voisins directs qui sont des murs
            wall_neighbours = [(nx, ny) for nx, ny in self.get_direct_neighbours(x, y) if self.grille[nx][ny] == self.enum_entite["mur"]]

            # S'il n'y a pas de voisins muraux, continuez avec la prochaine cellule
            if not wall_neighbours:
                continue

            # Choisissez un voisin mur au hasard
            nx, ny = random.choice(wall_neighbours)

            # Marquez cette cellule comme vide
            self.grille[nx][ny] = self.enum_entite["vide"]

            # Vérifiez si cette cellule est adjacente à une cellule vide du premier algorithme
            if (nx, ny) in empty_cells:
                # Si c'est le cas, nous avons connecté cette porte au labyrinthe
                self.non_connected_doors.remove((door_x, door_y))
                return

            # Ajoutez cette cellule à la liste à explorer
            to_expand.append((nx, ny))

    # fonction qui retourne les voisins d'une case (hors case bord) pour la construction du labyrinthe
    def get_neighbours(self, x, y):
        neighbours = []
        
        # Liste des positions possibles pour les voisins
        possible_neighbours = [(x-2, y), (x+2, y), (x, y-2), (x, y+2)]
        
        # Vérifiez chaque position pour voir si elle est à l'intérieur des limites et non sur le bord
        for nx, ny in possible_neighbours:
            if 1 < nx < self.taille - 1 and 1 < ny < self.taille - 1:
                neighbours.append((nx, ny))
                
        return neighbours

    # fonction qui retourne les voisins directs d'une case (hors case bord) pour relier les portes au labyrinthe
    def get_direct_neighbours(self, x, y):
        """Récupère les voisins immédiats (Nord, Sud, Est, Ouest)"""
        """Récupère les voisins immédiats (Nord, Sud, Est, Ouest) qui ne sont pas sur le bord du plateau"""
        neighbours = [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]
        # Filtrer les voisins pour exclure les cellules du bord
        return [[nx, ny] for nx, ny in neighbours if 0 < nx < self.taille - 1 and 0 < ny < self.taille - 1]

    def construct_plateau(self):
        # Choisissez un point de départ
        start_x = random.randint(1, self.taille - 2)
        start_y = random.randint(1, self.taille - 2)
        self.grille[start_x][start_y] = self.enum_entite["vide"]

        # Liste des cellules à visiter
        to_visit = [(start_x, start_y)]

        while to_visit:
            x, y = random.choice(to_visit)
            neighbours = self.get_neighbours(x, y)


            for nx, ny in neighbours:
                if self.grille[nx][ny] == self.enum_entite["mur"]:
                    # Briser le mur entre x, y et nx, ny
                    self.grille[(x + nx) // 2][(y + ny) // 2] = self.enum_entite["vide"]
                    self.grille[nx][ny] = self.enum_entite["vide"]

                    # Ajouter le voisin à la liste des cellules à visiter
                    to_visit.append((nx, ny))

            to_visit.remove((x, y))

        # Placer les portes sur les bords
        self.place_doors_on_edge(2)
        # Placer les clés
        self.place_keys(2)
        #self.print_plateau()
        # Connecter les portes au labyrinthe
        #self.connect_doors_to_maze()
        print(f"portes non connectées : {self.non_connected_doors}")
        #self.print_plateau()
        # Etendre le labyrinthe à partir des portes
        for door_x, door_y in self.non_connected_doors:
            self.expand_from_door(door_x, door_y)
        # affichage neighbour d une case du labyrinthe
        print(f"voisin de la case 0, 0 : {self.get_direct_neighbours(0, 0)}")
        
        # return case de départ
        return (start_x, start_y)

    # methode pour faire avancer l'agent (mettre a jour plateau et agent)
    def move_agent(self, agent, x , y):
        # verification de la position de l'agent si ce n est pas un mur
        if self.grille[x][y] != 0:
            x_old, y_old = agent.position[0], agent.position[1]
            # on met a jour les voisins
            verif = agent.move_forward(self.grille)
            if verif == False:
                agent.position[0] = x_old
                agent.position[1] = y_old
                return False
            # mise a jour plateau
            self.grille[agent.position[0]][agent.position[1]] = 1
            # remttre a vide la case precedente
            # si la case possede une cle ou une porte, on ne la remet pas a vide
            if self.array_cle.count((x_old, y_old)) == 0 and self.array_porte.count((x_old, y_old)) == 0:
                self.grille[x_old][y_old] = 5
            else:
                if self.array_cle.count((x_old, y_old)) != 0:
                    type_cle = 0
                    # recuperation type_cle
                    for cle in self.array_cle:
                        if cle[0] == x and cle[1] == y:
                            # Les coordonnées correspondent à celles de la clé
                            type_cle = cle[2]
                            break
                    # mise a jour plateau
                    self.grille[x_old][y_old] = type_cle
                elif self.array_porte.count((x_old, y_old)) != 0:
                    type_porte = 0
                    # recuperation type_cle
                    for cle in self.array_porte:
                        if cle[0] == x and cle[1] == y:
                            # Les coordonnées correspondent à celles de la clé
                            type_porte = cle[2]
                            break
                    # mise a jour plateau
                    self.grille[x_old][y_old] = type_porte

            if verif:
                return True
            return False
        return False

    # prendre une cle
    def take_key(self, agent):
        # verification de la position de l'agent si c est bien une cle
        if self.array_cle.count((agent.position[0], agent.position[1], self.enum_entite["cle"]["rouge"])) != 0:
            cle_recup = agent.add_key_bag(7)
            if cle_recup != 0:
                self.array_cle.remove((agent.position[0], agent.position[1], 7))
                self.array_cle.append((agent.position[0], agent.position[1], cle_recup))
            else: 
                self.array_cle.remove((agent.position[0], agent.position[1], 7))
            return True
        elif self.array_cle.count((agent.position[0], agent.position[1], self.enum_entite["cle"]["vert"])) != 0:
            cle_recup = agent.add_key_bag(8)
            if cle_recup != 0:
                self.array_cle.remove((agent.position[0], agent.position[1], 8))
                self.array_cle.append((agent.position[0], agent.position[1], cle_recup))
            else:
                self.array_cle.remove((agent.position[0], agent.position[1], 8))
            return True
        else:
            return False
    
    # fonction qui verifie que l agent est dans une porte et qu il a la bonne cle pour l ouvrir
    def open_door(self, agent):
        # verification de la position de l'agent est sur une porte
        if self.array_porte.count((agent.position[0], agent.position[1], self.enum_entite["porte"]["rouge"])) != 0:
            if agent.open_door(3):
                return True
        elif self.array_porte.count((agent.position[0], agent.position[1], self.enum_entite["porte"]["vert"])) != 0:
            if agent.open_door(4):
                return True
        else:
            print("impossible d'ouvrir la porte...")
            return False
        
    def test(self,agent):
        print("test")
        #plateau.print_plateau()
        #--------------------------------------TOUR-----------------------------

        #------------------INITIALISATION 2----------------------
        # IMPORTANT : avant de faire d'utiliser self.move_agent, il faut verifier que l'agent est bien sur une case valide qui est sur le plateau
            # C est pour ca que juste avant la boucle while, j'ai mis la position de l'agent a la position de depart donnee par le graphe qui est valide (le depart doit etre forcement sur une case vide)
        # position de depart de l'agent a recuperer dans la fonction construct_plateau
        x, y  = plateau.construct_plateau()
        print("position de depart de l'agent : ", x, y)
        # mise a jour de la position de l'agent
        agent.position[0] = x
        agent.position[1] = y
        agent.mise_a_jour_voisin_changement_pos()
        # mise a jour du plateau en fonction de la position de l'agent
        plateau.grille[agent.position[0]][agent.position[1]] = 1
        # ----------------------------------------------------
        
        # ----DEBUG-------------------------
        # affichage info case
        print(f"position de l'agent : {agent.position}")
        # voisin agen
        print(f"voisin de l'agent : {agent.neighbour}")
        for i in range(plateau.taille):
                print(f"ligne {i} : {plateau.grille[i]}")
        #self.move_agent(agent, x, y)
        # ----------------------------------

        # boucle de jeu avec action random pour le test
        # ------------------Boucle jeu random----------------------
        while(True):
            # action random
            action = random.randint(0, 3)
            if action == 0:
                # avancer
                x = agent.neighbour[agent.orientation["nord"]][0]
                y = agent.neighbour[agent.orientation["nord"]][1]
                verif = self.move_agent(agent, x, y)
                if verif == False:
                    print("impossible d'avancer, il y a un mur...")
                else:
                    print("j'avance...")
            elif action == 1:
                # tourner a gauche
                agent.left()
            elif action == 2:
                # tourner a droite
                agent.right()
            elif action == 3:
                self.take_key(agent)
            # verification si c est pas la fin du jeu
            if self.open_door(agent):
                print("porte ouverte")
                print("Fin du jeu")
                break

            # affichage du plateau version couleur
            print("Original")
            plateau.print_plateau()

            # affichage des plateaux
            # print(f"plateau : {plateau.grille}")
            for i in range(plateau.taille):
                print(f"ligne {i} : {plateau.grille[i]}")
        # ---------------------------------------------------------
        
        # ------------------Boucle jeu manuel pour voir comment marche chaque commande----------------------
        """while(True): # exemple de tour 

            #--------------POUR LES TESTS----------------
            # UTILISER LES ACTIONS DE L AGENT
            # mise a jour de la position de l'agent
            #agent.position[0] = x
            #agent.position[1] = y
            # ---------------------------------------------------------------

            # information sur l'agent
            # SE SERVIR DE agent.neighbour pour savoir quelle est l orientation de l agent
                # 0 : nord, 1 : est, 2 : sud, 3 : ouest
                # la case au nord indique la case devant lui donc la case ou il peut avancer
                # les autres cases indiquent les cases a sa gauche, a sa droite et derriere lui (pas utilise pour la partie graphique, c est juste pour le calcul)
            print(f"position de l'agent : {agent.position}")
            print(f"voisin de l'agent : {agent.neighbour}")

            # --------------POUR LES TESTS----------------
            # UTILISER LES ACTIONS DE L AGENT
            # mise a jour du plateau en fonction de la position de l'agent
            #plateau.grille[agent.position[0]][agent.position[1]] = 1
            # ---------------------------------------------------------------

            # verification si c est pas la fin du jeu
            if self.open_door(agent):
                print("porte ouverte")
                print("Fin du jeu")
                break

            # affichage du plateau version couleur
            print("Original")
            plateau.print_plateau()

            # faire une action
            # avant de faire d'utiliser self.move_agent, il faut verifier que l'agent est bien sur une case valide qui est sur le plateau
             # C est pour ca que juste avant la boucle while, j'ai mis la position de l'agent a la position de depart donnee par le graphe qui est valide (le depart doit etre forcement sur une case vide)
            # 1 : avancer
             # choisir un x et y qui est possible ( la case devant lui (nord -> devant lui))
            x = agent.neighbour[agent.orientation["nord"]][0]
            y = agent.neighbour[agent.orientation["nord"]][1]
            verif = self.move_agent(agent, x, y)
            if verif == False:
                print("impossible d'avancer, il y a un mur...")
            else:
                print("j'avance...")
            # prendre une cle
            verif_2 = self.take_key(agent)
            if verif_2:
                print("j'ai pris une cle...")
            else :
                print("il n'y a pas de cle...")


            # affichage du plateau version couleur
            print("Apres action")
            plateau.print_plateau()

            # affichage des plateaux
            # print(f"plateau : {plateau.grille}")
            for i in range(plateau.taille):
                print(f"ligne {i} : {plateau.grille[i]}")
            break"""
        #-----------------------------------------------------------------------
    
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