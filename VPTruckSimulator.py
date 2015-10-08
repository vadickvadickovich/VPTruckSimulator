import pygame
from pygame.locals import *
from vector2 import Vector2
from random import randint, choice

pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
screen = pygame.display.set_mode((800, 600), 0, 32)
pygame.display.set_caption('VPTruckSimulator')

font = pygame.font.SysFont('arial', 16)

target_image = pygame.image.load('target_2012.png').convert_alpha()
death_image = pygame.image.load('death.png').convert_alpha()

def collision(player, target):
	if player.pos[0] <= target.pos[0]:
		if player.pos[0] + player.size[0] >= target.pos[0]:
			if player.pos[1] <= target.pos[1]:
				if player.pos[1] + player.size[1] >= target.pos[1]:
					return True

class background(object):
	def __init__(self, image):
		self.image = image

	def render(self):
		screen.blit(self.image, (0, 0))

class lines(object):
	def __init__(self, image):
		self.image = image
		self.step = 0

	def process(self, truck_speed):
		self.step += truck_speed
		if self.step >= 600:
			self.step = 1

	def render(self):
		screen.blit(self.image, (0, self.step))
		screen.blit(self.image, (0, self.step - 600))

class Truck(object):
	def __init__(self, name, image):
		self.name = name
		self.image = image
		self.pos = Vector2(375, 400)
		self.speed = 10
		self.angle = 0
		self.move_speed = 350.
		self.size = (150, 240)

	def render(self):
		render_x = self.pos[0] - self.size[0]/2
		render_y = self.pos[1] - self.size[1]/2
		screen.blit(pygame.transform.rotate(self.image, self.angle), (render_x, render_y))

	def moving(self, pressed_keys, time_passed_seconds):
		key_direction = Vector2(0, 0)
		if pygame.key.get_pressed():
			if pressed_keys[K_a]:
				key_direction.x = -1
				#self.angle = 45
			if pressed_keys[K_d]:
				key_direction.x = +1
				#self.angle = -45
			if pressed_keys[K_w]:
				key_direction.y = -1
			if pressed_keys[K_s]:
				key_direction.y = +1

		key_direction.normalize()
		self.pos += key_direction * self.move_speed * time_passed_seconds

class target(object):
	def __init__(self):
		self.image = target_image
		self.size = (150, 197)
		self.pos = Vector2(0, 0)

		x = randint(200, 600)
		self.pos[0] = x

	def render(self):
		render_x = self.pos[0] - self.size[0]/2
		render_y = self.pos[1] - self.size[1]/2
		screen.blit(self.image, (render_x, render_y))

	def process(self, truck_speed):
		self.pos[1] += truck_speed

	def create(self):
		x = randint(150, 650)
		self.pos[0] = x

class Game(object):
	def __init__(self):
		self.screen = pygame.display.get_surface()
		self.clock = pygame.time.Clock()

		self.background = background('bg.png')
		self.background.image = pygame.image.load(self.background.image).convert()

		self.lines = lines('lines.png')
		self.lines.image = pygame.image.load(self.lines.image).convert_alpha()

		self.targets = []

		self.score = 0

	def NewGame(self):
		self.Truck = Truck('VPTruck', 'truck_sprite.png')
		self.Truck.image = pygame.image.load(self.Truck.image).convert_alpha()

		self.run()

	def render(self):
		self.background.render()
		self.lines.render()

		for value in self.targets:
			value.render()

		self.Truck.render()

		screen.blit(self.score_text, (10, 10))

	def process(self):
		self.lines.process(self.Truck.speed)

		#for x in xrange(0, 500):
		if randint(1, 2) == 1:
			self.targets.append(target())

		for value in self.targets:
			value.process(self.Truck.speed)
			if collision(self.Truck, value):
				if value.image == target_image:
					value.image = death_image
					self.score += 1
					if self.score%25 == 0:
						self.Truck.speed += 25

		self.score_text = font.render("Score: " + str(self.score), 1, (0, 0, 0))


	def run(self):
		while True:
			for event in pygame.event.get():
				if (event.type == QUIT) or ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)):
					exit()


			pressed_keys = pygame.key.get_pressed()
			time_passed = self.clock.tick(30)
			time_passed_seconds = time_passed / 1000.0

			self.Truck.moving(pressed_keys, time_passed_seconds)

			self.process()
			self.render()
			pygame.display.update()
			


#Game
VPTruckSimulator = Game()
VPTruckSimulator.NewGame()