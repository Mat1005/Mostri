import os
from random import choice

DIRECTIONS = "up", "down", "left", "right"
list = os.listdir("C:/Users/user/Desktop/mostri/livelli")
number_files = len(list)

class Entity: 
  def _init_(self, x, y, field, graphic):
    self.x = x
    self.y = y
    self.field = field
    self.field.entities.append(self)
    self.graphic = graphic

  def move(self, direction):
    futureX = self.x
    futureY = self.y

    if direction == "up" and self.y > 0:
      futureY -= 1
    elif direction == "down" and self.y < self.field.h - 1:
      futureY += 1
    elif direction == "left" and self.x > 0:
      futureX -= 1
    elif direction == "right" and self.x < self.field.w - 1:
      futureX += 1

    if self.x == futureX and self.y == futureY:
      return

    e = self.field.get_entity_at_coords(futureX, futureY)

    if e == None:
      self.x = futureX
      self.y = futureY
    else:
      self.collide(e)

  def update(self):
    pass

class Gold(Entity):
  def _init_(self, x, y, field):
    super()._init_(x, y, field, "$")
    self.value = 100

class Wall(Entity):
  def _init_(self, x, y, field):
    super()._init_(x, y, field, "#")

class Living_Entity(Entity):
  def _init_(self, x, y, name, hp, damage, field, graphic):
    super()._init_(x, y, field, graphic)
    self.name = name
    self.hp = hp
    self.max_hp = hp
    self.damage = damage
    self.field.livingentities.append(self)
    
  def attack(self, enemy):
    print(self.name, "attacca", enemy.name)
    enemy.hp -= self.damage
    if enemy.hp <= 0:
      print(enemy.name, "è morto")
      self.field.livingentities.remove(enemy)
      self.field.entities.remove(enemy)

class Monster(Living_Entity):
  def _init_(self, x, y, name, field):
    super()._init_(x, y, name, 10, 5, field, "m")
    
  def collide(self, entity):
    if isinstance(entity, Player):
      self.attack(entity)
  
  def move(self):
    super().move(choice(DIRECTIONS))

  def update(self):
    super().update()
    self.move()

class Player(Living_Entity):
  def _init_(self, x, y, name, field):
    super()._init_(x, y, name, 80, 20, field, "p")
  
  def collide(self, entity):
    if isinstance(entity, Monster):
      self.attack(entity)
    elif isinstance(entity, Gold):
      self.field.score += entity.value
      self.field.entities.remove(entity)

class Field:
  def _init_(self, levelNumber):
    self.entities = []
    self.score = 0
    self.levelNumber = levelNumber
    self.livingentities = []

    f = open("./level" + str(n) + ".txt", "r")
    rows = f.read().split("\n")
    f.close()

    self.h = len(rows)
    self.w = len(rows[0])

    for y in range(self.h):
      row = rows[y]
      for x in range(self.w):
        char = row[x]
        if char == "p":
          self.player = Player(x, y, "Player", self)
        elif char == "#":
          Wall(x, y, self)
        elif char == "$":
          Gold(x, y, self)
        elif char == "m":
          Monster(x, y, "Monster", self)

  def get_entity_at_coords(self, x, y):
    for e in self.entities:
      if e.x == x and e.y == y:
        return e

    return None
    
  def draw(self):
    print("score:", self.score)
    for y in range(self.h):
      for x in range(self.w):
        for e in self.entities:
          if x == e.x and y == e.y:
            print("[" + e.graphic + "]", end = "")
            break    
        else:
          print("[ ]", end = "")
      print()
  
  def update(self):
    for e in self.entities:
      e.update()
      
def check_victory(field):
  global vittoria
  global sconfitta
  vittoria = False
  sconfitta = False
  istherePlayer = False
  for e in field.livingentities:
    if isinstance(e, Player):
      istherePlayer = True
      if len(field.livingentities) == 1:
        vittoria = True
  if istherePlayer == False:
    sconfitta = True
    
        
field = Field(1)

def clear_screen():
  if os.name == "nt":
    os.system("cls")
  else:
    os.system("clear")

    
clear_screen()
while True:  
  
  check_victory(field)
  if vittoria == True:
    if field.levelNumber < number_files:
      field.levelNumber += 1
      n += 1
      print("livello", n)
      field._init_(n)
    else:
      print("hai vinto")
      break
  elif sconfitta == True:
    print("hai perso")
    break
  
  field.update()
  field.draw()
  
  command = input("input: ").lower()
  clear_screen()
  
  if command == "q": break
  elif command == "w": field.player.move("up")
  elif command == "a": field.player.move("left")
  elif command == "s": field.player.move("down")
  elif command == "d": field.player.move("right")
  
