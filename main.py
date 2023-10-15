import os
import random
import pygame
import random
import colorama
import time
from AgPl import *


SIZE_TILES = 32

    
class Player(object):
  key_color =  (0, 0, 0)
  open_door = False
  collected_keys = []  # Liste pour stocker les clés collectées
  triangle_vertices = [(12, 0), (0, 24), (24, 24)]
  facing_dir = ""
  orientation = {"ouest" : 0, "sud" : 1, "est" : 2, "nord" : 3}
  x = 0
  y = 0
  agent = set()
  plateau = set()

  def __init__(self, plateau, agent, x, y):
        # creation de l'agent et du plateau
        self.agent = agent
        self.plateau = plateau
        self.agent.position[0] = 5 
        self.agent.position[1] = 5 
        self.agent.mise_a_jour_voisin_changement_pos()
        self.plateau.grille[x][y] = 1
        
        self.x = 5 * SIZE_TILES
        self.y = 5 * SIZE_TILES
        
        self.rect = pygame.Rect(self.x, self.y, SIZE_TILES, SIZE_TILES)
        self.collected_keys = set()  # Use a set to store collected keys
        self.facing_dir = self.agent.mon_orientation
        

  def move(self, dx, dy):
        new_x = self.rect.x + dx * SIZE_TILES
        new_y = self.rect.y + dy * SIZE_TILES

        # Check for collision with walls and doors
        collision = any(
            (new_x, new_y) == (wall.rect.x, wall.rect.y) for wall in walls
        )

        # Check if the player has the key to open the door
        if any(
            (new_x, new_y) == (door.rect.x, door.rect.y) and not player.can_open_door(door.get_color())
            for door in doors
        ):
            # Player doesn't have the key, prevent movement
            collision = True

        if not collision:
            self.rect.x = new_x
            self.rect.y = new_y

  def move_towards_key_or_door(self, keys, doors):
    # Calcule la distance entre le joueur et chaque clé
    key_distances = [(key, abs(self.rect.x - key.rect.x) + abs(self.rect.y - key.rect.y)) for key in keys]

    # Trie les clés par distance croissante
    key_distances.sort(key=lambda x: x[1])

    # Calcule la distance entre le joueur et chaque porte
    door_distances = [(door, abs(self.rect.x - door.rect.x) + abs(self.rect.y - door.rect.y)) for door in doors]

    # Trie les portes par distance croissante
    door_distances.sort(key=lambda x: x[1])

    # Si le joueur n'a pas de clé, il se dirige vers la clé la plus proche
    if not self.collected_keys:
        target = key_distances[0][0] if key_distances else None
    else:
        # Si le joueur a des clés, il se dirige vers la porte la plus proche qu'il peut ouvrir
        target = None
        for door, distance in door_distances:
            if door.get_color() in self.collected_keys:
                target = door
                break

    if target:
        # Calcul du déplacement pour atteindre la cible
        dx = 0
        dy = 0

        if target.rect.x < self.rect.x:
            dx = -1
        elif target.rect.x > self.rect.x:
            dx = 1

        if target.rect.y < self.rect.y:
            dy = -1
        elif target.rect.y > self.rect.y:
            dy = 1

        self.move(dx, dy)
    else:
        # Aucune cible trouvée, le joueur peut se déplacer au hasard
        dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.move(dx, dy)

  def move_randomly(self):
    dx, dy = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
    self.x = dx
    self.y = dy
    
    print(dx, dy)
    self.facing(dx,dy)

    self.move(dx, dy)

  def collect_key(self, key_color):
      self.collected_keys.add(key_color)  # Add the key color to collected keys

  def can_open_door(self, door_color):
      return door_color in self.collected_keys  # Check if the player has the corresponding key

  def get_triangle_vertices(self):
    x, y = self.rect.center  # Get the center of the player's rectangle
    # Calculate the triangle vertices relative to the player's center
    vertices = [(x + vertex[0] - 12, y + vertex[1] - 12) for vertex in self.triangle_vertices]
    return vertices

  def nouveau_orientation(orientation):
    pass
    
  def move_ag_pl(self):
    x_old = self.agent.position[0] 
    y_old = self.agent.position[1]
    voisins = self.plateau.get_direct_neighbours(x_old,y_old)
    #ici pour le teste le voisin vien du nord
    print("orientation : ", self.facing_dir)

    voisin = 0

    if(len(voisins[self.orientation[self.facing_dir]]) < 3):
        voisin = voisins[2]
    else:
        voisin = voisins[self.orientation[self.facing_dir]]

    x_voisin_direct = voisin[0]
    y_voisin_direct = voisin[1]

    if self.plateau.move_agent(self.agent,x_voisin_direct,y_voisin_direct):
        self.agent.mise_a_jour_voisin_changement_pos()
        #afficher_plateau(plateau.grille)

        # mettre a jour la position dans pygame
        print("avancer au voisin")

        # si clé alors prendre la clée
        if self.plateau.take_key(self.agent):
            # mettre a jour sur pygame
            pass

        # si porte alors tester de l'ouvrir
            # sinon revenir en arriere et tourner à droite
        if self.plateau.open_door(self.agent) == False:
            self.plateau.move_agent(self.agent,x_old,y_old)
            #afficher_plateau(plateau.grille)
            print("je recule car je ne peut pas ouvrir la porte")
            self.agent.right()
            #print("je tourne à droite"
            #mise a jour de direction dans pygame
            self.facing(self.facing_dir)
            self.agent.mise_a_jour_voisin_changement_pos()
    else:
      self.agent.right()
      #mettre a jour la position dans pygame
      self.facing(self.facing_dir)

  def facing(self,dir):
    if dir == "sud":
        self.triangle_vertices = [(24, 12), (0, 0), (0, 24)]  # Facing right est
        print(self.triangle_vertices)
    elif dir == "nord":
        self.triangle_vertices = [(0, 12), (24, 0), (24, 24)]  # Facing left ouest
        print(self.triangle_vertices)
    elif dir == "ouest":
        self.triangle_vertices = [(12, 24), (0, 0), (24, 0)]  # Facing down sud
        print(self.triangle_vertices)
    elif dir == "est":
        self.triangle_vertices = [(12, 0), (0, 24), (24, 24)] # Facing up nord
        print(self.triangle_vertices) 
  
  def facing_left(self):
     self.triangle_vertices = [(0, 12), (24, 0), (24, 24)]  # Facing left
  
  def facing_right(self):
     self.triangle_vertices = [(24, 12), (0, 0), (0, 24)]  # Facing right

class Wall(object):
  def __init__(self, pos):
    walls.append(self)
    self.rect = pygame.Rect(pos[0], pos[1], SIZE_TILES, SIZE_TILES)

class Key(object):

  color = (0, 0, 0)

  def __init__(self, pos, color):
    keys.append(self)
    self.color = color
    self.rect = pygame.Rect(SIZE_TILES / 2 + pos[0], SIZE_TILES / 2 + pos[1],
                            SIZE_TILES / 2, SIZE_TILES / 2)

  def get_color(self):
    return self.color


class Door(object):

  color = (0, 0, 0)

  def __init__(self, pos, color):
    doors.append(self)
    self.color = color
    self.rect = pygame.Rect(pos[0], pos[1], SIZE_TILES, SIZE_TILES)

  def get_color(self):
    return self.color

  def is_accessible(self, player):
          return self.get_color() in player.collected_keys


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Sortir du labyrinthe !")
screen = pygame.display.set_mode((SIZE_TILES * 10, SIZE_TILES * 10))

clock = pygame.time.Clock()
walls = []  # List to hold the walls
keys = []
doors = []

# Holds the level layout in a list of strings.
level1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 0, 0, 0, 7, 0, 0],
          [0, 5, 5, 5, 5, 5, 5, 5, 0, 0], [0, 8, 0, 5, 0, 0, 0, 5, 0, 0],
          [0, 0, 0, 0, 0, 0, 0, 5, 0, 0], [0, 0, 0, 5, 5, 5, 0, 5, 0, 0],
          [4, 5, 5, 5, 0, 5, 5, 5, 0, 0], [0, 5, 1, 5, 3, 0, 0, 0, 0, 0],
          [0, 5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

pl = plateau(10)
X,Y= pl.construct_plateau()
ag = agent(5, 5, plateau)
#level = level1
player = Player(pl,ag, X,Y)  # Create the player

level = pl.grille

enum_entite = {
    "mur": 0,
    "agent": 1,
    "cle": {
        "rouge": 7,
        "vert": 8
    },
    "porte": {
        "rouge": 3,
        "vert": 4
    },
    "vide": 5
}

x = y = 0
for row in level:
  for col in row:
    if col == 0:  #MUR
      Wall((x, y))
    if col == 8:  #CLE VERT
      Key((x, y), (0, 255, 0))
    if col == 7:  #CLE ROUGE
      Key((x, y), (255, 0, 0))
    if col == 3:  #PORTE ROUGE
      Door((x, y), (255, 0, 0))
    if col == 4:  #PORTE VERT
      Door((x, y), (0, 255, 0))
    x += SIZE_TILES
  y += SIZE_TILES
  x = 0

running = True
while running:
  clock.tick(60)

  # Vérifie si le joueur est sur la même case qu'une clé
  for key in keys:
    if player.rect.colliderect(key.rect):
        keys.remove(key)
        player.collect_key(key.get_color())

  # Check if the player can open a door
  for door in doors:
      if player.rect.colliderect(door.rect):
          door_color = door.get_color()
          if player.can_open_door(door_color):
              doors.remove(door) 


  # L'agent se déplace de manière intelligente 
  #player.move_towards_key_or_door(keys, doors)
  
  # L'agent se déplace de manière pas intelligente 
  #player.move_randomly()

   # L'agent se déplace de manière pas intelligente 
  player.move_ag_pl()

  pygame.time.delay(50)  # Ajoute une pause de 200 millisecondes


  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False
    if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
      running = False

  # Move the player if an arrow key is pressed
  keyb = pygame.key.get_pressed()
  if keyb[pygame.K_LEFT]:
      player.facing = "LEFT"
      player.triangle_vertices = [(0, 12), (24, 0), (24, 24)]
      player.move(-1, 0)
  if keyb[pygame.K_RIGHT]:
      player.facing = "RIGHT"
      player.triangle_vertices = [(24, 12), (0, 0), (0, 24)]
      player.move(1, 0)
  if keyb[pygame.K_UP]:
      player.facing = "UP"
      player.triangle_vertices = [(12, 0), (0, 24), (24, 24)]
      player.move(0, -1)
  if keyb[pygame.K_DOWN]:
      player.facing = "DOWN"
      player.triangle_vertices = [(12, 24), (0, 0), (24, 0)]
      player.move(0, 1)



  # Just added this to make it slightly fun ;)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  #if (player.door_opened()):
  #   running = False
  
  # Draw the scene
  screen.fill((255, 255, 255))

  
  for wall in walls:
    pygame.draw.rect(screen, (0, 0, 0), wall.rect)
    #pygame.draw.rect(screen, (255, 255, 255), end_rect)
    #pygame.draw.rect(screen, (255, 200, 0), player.rect)


  pygame.draw.rect(screen, (255, 200, 0), player.rect)
  triangle_vertices = player.get_triangle_vertices()  # Get updated vertices
  pygame.draw.polygon(screen, (0, 0, 255), triangle_vertices)  # Draw the triangle
  
  for key in keys:
    if key.get_color() == (255, 0, 0):  # Clé rouge
        color = (255, 0, 0)
    else:  # Clé verte
        color = (0, 255, 0)
    pygame.draw.rect(screen, color, key.rect)

  
  for door in doors:
    if door.get_color() == (255, 0, 0):  # Porte rouge
        color = (255, 0, 0)
    else:  # Porte verte
        color = (0, 255, 0)
    pygame.draw.rect(screen, color, door.rect)

  
  # colorGreen = (0, 255, 0) # Vert 
  # colorRed = (255, 0, 0) # Rouge 
  # pygame.draw.rect(screen, colorRed, key.rect)
  # pygame.draw.rect(screen, colorGreen, key.rect)

  # pygame.draw.rect(screen, colorGreen, door.rect)
  # pygame.draw.rect(screen, colorRed, door.rect)


  # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
  pygame.display.flip()
  clock.tick(360)


pygame.quit()
