import pygame
import sys
import os
from os import path
import random
from time import sleep

#Dimensions of screen
height = 600
width = 720

#Colours defined
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (0,0,255)
BLUE = (255,0,0)
GREEN = (0,255,0)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Protect base")
game_folder = os.path.dirname(__file__)
img_folder = os.path.join(game_folder,"img")
snd_dir = path.join(path.dirname(__file__),"snd")
font_name = pygame.font.match_font('Berlin Sans FB')
bg_image = pygame.image.load(path.join(img_folder, "background.jpg")).convert()
bg_image = pygame.transform.scale(bg_image, (width,height))
base_image = pygame.image.load(path.join(img_folder, "base.png")).convert()
base_image = pygame.transform.scale(base_image, (width, 80))
# base_image.set_colorkey(WHITE)
base_rect = base_image.get_rect()
base_rect.centery = height - 40
FPS = 60
clock = pygame.time.Clock()

explosion = []
for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_folder, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (60, 60))
    explosion.append(img)

def highscore(score):
	dir = path.dirname(__file__)
	with open(path.join(dir, "highscore.txt"), 'r') as f:
		try:
			highscore = int(f.read())
		except:
			highscore = 0
	if score>highscore:
		highscore = score
		with open(path.join(dir, "highscore.txt"), 'w') as f:
			f.write(str(highscore))

def gamesplayed():
	dir = path.dirname(__file__)
	with open(path.join(dir, "game.txt"), 'r') as f:
		try:
			game = int(f.read())
		except:
			game = 0
	game_new = game+1
	with open(path.join(dir, "game.txt"), 'w') as f:
		f.write(str(game_new))

def draw_text(surf, msg, size, centerx, centery, color):
	font = pygame.font.Font(font_name,size)
	msg_img = font.render(msg, True, color)
	msg_rect = msg_img.get_rect()
	msg_rect.centerx = centerx
	msg_rect.centery = centery
	surf.blit(msg_img, msg_rect)


class Explosion(pygame.sprite.Sprite):
	def __init__(self, centerx, centery):
		pygame.sprite.Sprite.__init__(self)
		self.image = explosion[0]
		self.rect = self.image.get_rect()
		self.rect.centerx = centerx
		self.rect.centery = centery
		self.frame = 0
		self.last_update = pygame.time.get_ticks()
		self.frame_rate = FPS

	def update(self):
		now = pygame.time.get_ticks()
		if now - self.last_update > self.frame_rate:
			self.last_update = now
			self.frame +=1
			if self.frame == len(explosion):
				self.kill()
			else:
				centerx = self.rect.centerx
				centery = self.rect.centery
				self.image = explosion[self.frame]
				self.rect = self.image.get_rect()
				self.rect.centerx, self.rect.centery = centerx, centery

class Player(pygame.sprite.Sprite):
	def __init__(self,choice):
		pygame.sprite.Sprite.__init__(self)
		if choice == 1:
			self.image = pygame.image.load(os.path.join(img_folder, "player1.png")).convert()
		elif choice == 2:
			self.image = pygame.image.load(os.path.join(img_folder, "player2.png")).convert()
		elif choice == 3:
			self.image = pygame.image.load(os.path.join(img_folder, "player3.png")).convert()
		self.image = pygame.transform.scale(self.image, (60,100))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		screen.blit(self.image, self.rect)
		self.rect.centerx, self.rect.centery = width/2, height - 130
		self.speedx, self.speedy = 0, 0

	def update(self):
		self.speedy = 0
		self.speedx = 0
		keystate = pygame.key.get_pressed()
		if keystate[pygame.K_LEFT]:
			self.speedx = -1
		if keystate[pygame.K_RIGHT]:
			self.speedx = 1
		if keystate[pygame.K_UP]:
			self.speedy = -1
		if keystate[pygame.K_DOWN]:
			self.speedy = 1
		if self.rect.centerx > 30 and self.speedx<0:
			self.rect.centerx+=self.speedx
		if self.rect.centery > 50 and self.speedy<0:
			self.rect.centery+=self.speedy
		if self.rect.centerx < width-30 and self.speedx>0:
			self.rect.centerx+=self.speedx
		if self.rect.centerx < height-130 and self.speedy>0:
			self.rect.centery+=self.speedy


	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.top)
		bullets.add(bullet)
		all_sprites.add(bullet)

class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.color = BLACK 
		self.image = pygame.image.load(os.path.join(img_folder, "bullet3.png")).convert()
		self.image.set_colorkey(WHITE)
		self.image = pygame.transform.scale(self.image, (7, 10))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		screen.fill(BLACK, self.rect)
		self.rect.bottom = y
		self.speedy = -2

	def update(self):
		self.rect.centery += self.speedy
		if self.rect.bottom < 0:
			self.kill()

class e_Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.color = BLACK 
		self.image = pygame.image.load(os.path.join(img_folder, "bullet3.png")).convert()
		self.image.set_colorkey(WHITE)
		self.image = pygame.transform.rotate(self.image, 180)
		self.image = pygame.transform.scale(self.image, (7, 10))
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		screen.fill(BLACK, self.rect)
		self.rect.bottom = y
		self.speedy = 2

	def update(self):
		self.rect.centery += self.speedy
		if self.rect.bottom > height:
			self.kill()

class Button():
	def __init__(self, msg, x, y):
		self.height = 30
		self.width = 180
		self.font = pygame.font.Font(font_name, 24)
		self.text_color = BLACK
		self.bg_color = WHITE
		self.rect = pygame.Rect(0 , 0, self.width, self.height)
		self.msg_img = self.font.render(msg, True, self.text_color, self.bg_color)
		self.msg_rect = self.msg_img.get_rect()
		self.rect.centerx, self.rect.centery = x, y
		self.msg_rect.centerx, self.msg_rect.centery = x, y
		screen.fill(self.bg_color, self.rect)
		screen.blit(self.msg_img, self.msg_rect)

class Soldier(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.image = pygame.image.load(os.path.join(img_folder, "soldier.png"))
		self.image = pygame.transform.scale(self.image, (20,20))
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.centery = random.randrange(0, width-self.rect.width), random.randrange(-150,-50)
		self.speedy = 1
		self.last_update = pygame.time.get_ticks() 

	def update(self):
		self.rect.y+=self.speedy
		self.now = pygame.time.get_ticks()
		if (self.now - self.last_update)%500 == 0:
			self.shoot()
		if self.rect.bottom > height-80:
			self.rect.x, self.rect.centery = random.randrange(0, width-self.rect.width), random.randrange(-150,-50)

	def shoot(self):
		bullet = e_Bullet(self.rect.centerx, self.rect.centery)
		ebullets.add(bullet)
		all_sprites.add(bullet)

class Tank(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.choice = random.randrange(0,500)%4 + 1
		if self.choice == 1 :
			self.image = pygame.image.load(os.path.join(img_folder, "enemy1.png"))
		elif self.choice == 2 :
			self.image = pygame.image.load(os.path.join(img_folder, "enemy2.png"))
		elif self.choice == 3 :
			self.image = pygame.image.load(os.path.join(img_folder, "enemy3.png"))
		elif self.choice == 4 :
			self.image = pygame.image.load(os.path.join(img_folder, "enemy4.png"))
		self.image = pygame.transform.scale(self.image, (60,100))
		self.image.set_colorkey(WHITE)
		self.rect = self.image.get_rect()
		self.rect.x, self.rect.centery = random.randrange(0, width-self.rect.width), random.randrange(-150,-50)
		self.speedy = 1
		self.last_update = pygame.time.get_ticks() 

	def update(self):
		self.rect.centery = self.rect.centery+self.speedy
		self.now = pygame.time.get_ticks()
		if (self.now - self.last_update)%500 == 0:
			self.shoot()
		if self.rect.bottom > height-80:
			self.rect.x, self.rect.centery = random.randrange(0, width-self.rect.width), random.randrange(-150,-50)

	def shoot(self):
		bullet = e_Bullet(self.rect.centerx, self.rect.centery)
		ebullets.add(bullet)
		all_sprites.add(bullet)


def story_mode():
	screen.fill(BLACK)
	draw_text(screen, "YOUR BASE HAS BEEN ATTACKED BY ENEMIES!!!!!!!", 36, width/2, height/4, WHITE)
	draw_text(screen, "<< YOU ARE ASSIGNED TO PROTECT THE BASE UNTIL AIRFORCE ARRIVES >>", 24, width/2, height/2, WHITE)
	draw_text(screen, "ENTER ANY KEY TO CONTINUE", 24, width/2, 3*height/4, WHITE)
	pygame.display.flip()
	waiting = True
	while waiting :
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				waiting = False
			elif event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()


def instructions():
	screen.fill(BLACK)
	draw_text(screen, "INSTRUCTIONS", 100, width/2, 70, WHITE)
	draw_text(screen, "YOUR TASK IS TO KILL AS MANY ENEMIES AS POSSIBLE", 24, width/2, 230, WHITE)
	draw_text(screen, "ARROWS ARE USED TO PILOT TANK", 24, width/2, 270, WHITE)
	draw_text(screen, "PRESS SPACE TO FIRE BULLET", 24, width/2, 290, WHITE)
	draw_text(screen, "YOU TANK IS DESTROYED IF ENEMY TANK OR SOLDIER HITS YOU", 24, width/2, 350, WHITE)
	draw_text(screen, "YOUR TANK IS ALSO DESTROYED IF IT IS HIT BY ENEMIES BULLETS", 24, width/2, 410, WHITE)
	button1 = Button("<<< MAIN MENU", 110, height-30)
	button2 = Button("START GAME >>>", width-110, height-30)
	pygame.display.flip()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if button1.rect.collidepoint(mouse_x, mouse_y):
					main_menu()
					waiting = False
				elif button2.rect.collidepoint(mouse_x, mouse_y):
					waiting = False


def main_menu():
	screen.fill(BLACK)
	draw_text(screen, "Protect Base", 128, width/2, height/4, WHITE)
	button1 = Button("START GAME", width/2, height/2)
	button2 = Button("INSTRUCTIONS", width/2, height/2+40)
	button3 = Button("STATS", width/2, height/2+80)
	pygame.display.flip()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if button1.rect.collidepoint(mouse_x, mouse_y):
					waiting = False
				elif button2.rect.collidepoint(mouse_x, mouse_y):
					instructions()
					waiting = False
				elif button3.rect.collidepoint(mouse_x, mouse_y):
					stats()
					waiting = False

def select_ship():
	screen.fill(BLACK)
	draw_text(screen, "Select your vehichle", 64, width/2, 64, WHITE)
	img1 = pygame.image.load(os.path.join(img_folder, "player1.png")).convert()
	img2 = pygame.image.load(os.path.join(img_folder, "player2.png")).convert()
	img3 = pygame.image.load(os.path.join(img_folder, "player3.png")).convert()
	img1 = pygame.transform.scale(img1, (int(width/7),240))
	img2 = pygame.transform.scale(img2, (int(width/7),240))
	img3 = pygame.transform.scale(img3, (int(width/7),240))
	rect1 = img1.get_rect()
	rect2 = img2.get_rect()
	rect3 = img3.get_rect()
	rect1.centerx, rect1.centery = int(3*width/14), height/2
	rect2.centerx, rect2.centery = int(7*width/14), height/2
	rect3.centerx, rect3.centery = int(11*width/14), height/2
	screen.blit(img1,rect1)
	screen.blit(img2,rect2)
	screen.blit(img3,rect3)
	pygame.display.flip()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if rect1.collidepoint(mouse_x, mouse_y):
					choice = 1
					return choice
					waiting = False
				elif rect2.collidepoint(mouse_x, mouse_y):
					choice = 2
					return choice
					waiting = False
				elif rect3.collidepoint(mouse_x, mouse_y):
					choice = 3
					return choice
					waiting = False

def game_over(choice):
	screen.fill(BLACK)
	img1 = pygame.image.load(os.path.join(img_folder, "Nice-Game-Over.jpg")).convert()
	rect1 = img1.get_rect()
	rect1.centerx = width/2
	screen.blit(img1, rect1)
	draw_text(screen, "Your tank is detroyed!!!", 30, width/2, height/2, WHITE)
	button1 = Button("PLAY AGAIN", width/4, height*3/4)
	button2 = Button("CHANGE TANK", 3*width/4, 3*height/4)
	pygame.display.flip()
	highscore(score)
	gamesplayed()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if button1.rect.collidepoint(mouse_x, mouse_y):
					waiting = False
					return choice
				elif button2.rect.collidepoint(mouse_x, mouse_y):
					waiting = False
					choice = select_ship()
					return choice

def stats():
	dir = path.dirname(__file__)
	with open(path.join(dir, "highscore.txt"), 'r') as f:
		try:
			highscore = int(f.read())
		except:
			highscore = 0
	with open(path.join(dir, "game.txt"), 'r') as f:
		try:
			game = int(f.read())
		except:
			game = 0
	screen.fill(BLACK)
	draw_text(screen, "STATS", 128, width/2, height/4, WHITE)
	draw_text(screen, "HIGHSCORE : "+ str(highscore), 24, width/2, height/2-20, WHITE)
	draw_text(screen, "TOTAL GAMES PLAYED : "+str(game),24, width/2, height/2+20, WHITE)
	button1 = Button("<< MAIN MENU", width/4, height*3/4)
	button2 = Button("START GAME >>", 3*width/4, 3*height/4)
	pygame.display.flip()
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			elif event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = pygame.mouse.get_pos()
				if button1.rect.collidepoint(mouse_x, mouse_y):
					main_menu()
					waiting = False
				elif button2.rect.collidepoint(mouse_x, mouse_y):
					waiting = False


# pygame.mixer.music.load(path.join(snd_dir,'back.wav'))
# pygame.mixer.music.set_volume(0.4)
# pygame.mixer.music.play(-1)
shoot_sound = pygame.mixer.Sound(path.join(snd_dir,"gun.wav"))
main_menu()
story_mode()
choice = select_ship()
running = True
game_active = False
score = 0
tanksdestroyed1 = 0
soldierskilled1 = 0
while running:
	screen.fill(WHITE)
	screen.blit(bg_image, (0,0))
	screen.blit(base_image, base_rect)
	if not game_active:
		score = 0
		tanksdestroyed1 = 0
		soldierskilled1 = 0
		game_active = True
		all_sprites = pygame.sprite.Group()
		bullets = pygame.sprite.Group()
		ebullets = pygame.sprite.Group()
		tanks = pygame.sprite.Group()
		soldiers = pygame.sprite.Group()
		player = Player(choice)
		soldier1 = Soldier()
		soldier2 = Soldier()
		soldier3 = Soldier()
		soldier4 = Soldier()
		tank1 = Tank()
		tank2 = Tank()
		tanks.add(tank1)
		tanks.add(tank2)
		soldiers.add(soldier1)
		soldiers.add(soldier2)
		soldiers.add(soldier3)
		all_sprites.add(tank1)
		all_sprites.add(tank2)
		all_sprites.add(soldier1)
		all_sprites.add(soldier2)
		all_sprites.add(soldier3)
		all_sprites.add(player)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE:
				#shoot_sound.play()
				player.shoot()

	clock.tick()
	all_sprites.update()
	sleep(0.001)
	draw_text(screen, str(score), 24, width/2, 20, BLACK)
	hits = pygame.sprite.groupcollide(bullets, tanks, True, True)# or pygame.sprite.spritecollide(player, ebullets, True)
	for hit in hits:
		tanksdestroyed1+=1
		score+=20
		expl = Explosion(hit.rect.centerx, hit.rect.centery)
		all_sprites.add(expl)
		tank = Tank()
		all_sprites.add(tank)
		tanks.add(tank)
	hits = pygame.sprite.spritecollide(player, ebullets, True)
	for hit in hits:
		game_active = False
		expl = Explosion(hit.rect.centerx,hit.rect.centery)
		all_sprites.add(expl)
		sleep(0.5)
		game_over(choice)
	hits = pygame.sprite.groupcollide(bullets, soldiers, True, True)
	for hit in hits:
		soldierskilled1+=1
		score+=10
		expl = Explosion(hit.rect.centerx, hit.rect.centery)
		all_sprites.add(expl)
		soldier = Soldier()
		all_sprites.add(soldier)
		soldiers.add(soldier)
	hits = pygame.sprite.spritecollide(player, tanks, True) or pygame.sprite.spritecollide(player, soldiers, True)
	for hit in hits:
		expl = Explosion(hit.rect.centerx,hit.rect.centery)
		all_sprites.add(expl)
		game_active = False
		sleep(0.5)
		game_over(choice)

	all_sprites.draw(screen)
	pygame.display.flip()

pygame.quit()
