import time
import pygame
import random
import math

pygame.init()
pygame.mixer.init()
# ustawienie wielkości okna

screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# ustawienie tytułu okna

pygame.display.set_caption(' Space Invaders ')

# załaduj obrazek statku
statek = pygame.image.load('data/ship_sprite.png')
pocisk = pygame.image.load('data/bullet.png')
kosmita_sprite = pygame.image.load('data/alien_sprite.png')
theme = pygame.mixer.music.load("sounds/theme.mp3")
pocisk_sound = pygame.mixer.Sound('sounds/shoot.wav')
death_sound = pygame.mixer.Sound('sounds/explosion.wav')
win_sound = pygame.mixer.Sound('sounds/win_sound.mp3')
coin_sound = pygame.mixer.Sound('sounds/get_coin.mp3')
pygame.mixer.music.set_volume(0.05)
pygame.mixer.Sound.set_volume(pocisk_sound, 0.1)
pygame.mixer.Sound.set_volume(death_sound, 0.1)
pygame.mixer.Sound.set_volume(win_sound, 0.1)
pygame.mixer.Sound.set_volume(coin_sound, 0.1)
score = 0
font = pygame.font.Font("fonts/slkscr.ttf", 30)
other_font = pygame.font.Font("fonts/slkscrb.ttf")


class kosmita_blueprint:

  def __init__(self):
      self.x = random.randint(0, 550)
      self.y = random.randint(-50, -20)
      self.move_x = -1
      self.move_y = 5
      self.counter1 = 0
      self.counter2 = 0

  def move(self):
    self.x += self.move_x

    if self.counter1 >= 20:
      self.counter1 = 0
      self.x = 499
      self.move_x *= -1
    elif self.counter2 >= 20:
      self.counter2 = 0
      self.x = 1
      self.move_x *= -1

    if self.x < 500 and self.x > 0:
      self.x += self.move_x
    elif self.x > 500:
      self.x = 500
      self.y += self.move_y
      self.counter1 += 1
    elif self.x < 0:
      self.x = 0
      self.y += self.move_y
      self.counter2 += 1

  def draw(self):
    screen.blit(kosmita_sprite, (self.x, self.y))


def iscollision(kosmita_x, kosmita_y, x_2, y_2):
  droga = math.sqrt(math.pow((kosmita_x + 16) - x_2, 2) + math.pow((kosmita_y + 8) - y_2, 2))
  if droga <= 16:
    return True
  else:
    return False


def gameover():
  text1 = font.render("GAME OVER", True, (255, 255, 255))
  text = font.render("SCORE: " + str(score), True, (255, 255, 255), (0, 0, 0))
  screen.blit(text, (100, 170))
  screen.blit(text1, (100, 130))
  


kosmici = []
for i in range(30):
  kosmita = kosmita_blueprint()
  kosmici.append(kosmita)

pygame.mixer.music.play(-1)
x_origin = 300
y_origin = 350
x_origin + 8
counter = 0
x_bullet = 3000
y_bullet = 3000

# pętla gry
switch = False
running = True
while running:
  x_move = 0
  # zdarzenia zewnętrzne np. kliknięcie na klawiaturze
  for event in pygame.event.get():
    # zdarzenie zamknięcia programu
    if event.type == pygame.QUIT:
      running = False
  
  key = pygame.key.get_pressed()
  
  #while True:
    #screen.fill('black')
    #text2 = other_font.render("PRESS SPACE TO PLAY", True, (255, 255, 255))
    #screen.blit(text2, (100, 130))
    #if key[pygame.K_SPACE]:
      #break
      #print("1")
    #pygame.display.flip()
    #clock.tick(60)

    # dodaj obsługę zdarzenia na kliknięcie klawisza
    # obsługa strzałek jako poruszanie się statku
  key = pygame.key.get_pressed()
  if key[pygame.K_LEFT]:
    if x_origin > 0:
      x_move = -5
  elif key[pygame.K_RIGHT]:
    if x_origin < 555:
      x_move = 5
  elif key[pygame.K_SPACE]:
    if switch == False:
      pygame.mixer.Sound.play(pocisk_sound)
      x_bullet = x_origin + 18
      y_bullet = y_origin
      screen.blit(pocisk, (x_bullet, y_bullet))
      switch = True

  
  time.sleep(0.05)

  x_origin += x_move

  # narysuj statek w odpowiedniej pozycji
  screen.fill('black')
  screen.blit(statek, (x_origin, y_origin))

  text3 = other_font.render("SCORE: " + str(score), True, (255, 255, 255), (0, 0, 0))
  screen.blit(text3, (0, 390))
  
  if switch:
    screen.blit(pocisk, (x_bullet, y_bullet - 20))
    y_bullet -= 20

  for kosmita in kosmici:
    kosmita.move()

  for kosmita in kosmici:
    kolizja_kosmita_pocisk = iscollision(kosmita.x, kosmita.y, x_bullet, y_bullet)
    if kolizja_kosmita_pocisk:
      pygame.mixer.Sound.play(coin_sound)
      score += 1
      switch = False
      kosmita.x = random.randint(0, 550)
      kosmita.y = random.randint(-50, -20)
      kosmita.move_x = -1
  
  for kosmita in kosmici:
    kosmita.draw()

  if y_bullet <= 10 or switch == False:
    switch = False
    x_bullet = 3000
    y_bullet = 3000

  for kosmita in kosmici:
    kolizja_kosmita_statek = iscollision(kosmita.x, kosmita.y, x_origin, y_origin)
    if kolizja_kosmita_statek:
      pygame.mixer.music.stop()
      pygame.mixer.Sound.play(death_sound)
      screen.fill('black')
      gameover()
      running = False

  if score >= 30:
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(win_sound)
    screen.fill('black')
    gameover()
    running = False

  # aktualizuje cały ekran
  pygame.display.flip()

  # ogranicza FPS do 60
  clock.tick(60)

time.sleep(5)
# zamknięcie programu
pygame.quit()
