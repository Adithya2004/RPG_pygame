import pygame
from support import *
from settings import *
from entity import Entity

class Player(Entity):

	def __init__(self,pos,groups,obstacle_sprites,create_attack,destroy_weapon,create_magic):
		super().__init__(groups)

		self.image = pygame.image.load(r"graphics\test\player.png").convert_alpha()
		self.rect = self.image.get_rect(topleft = pos)

		self.import_player_assets()
		self.status = 'down'
		
		self.hitbox = self.rect.inflate(0,-25)
		self.speed = 5

		self.attack_cooldown = 400
		self.attacking = False
		self.attack_time = 40

		self.obstacle_sprites = obstacle_sprites
		self.create_attack = create_attack
		self.destroy_attack = destroy_weapon
		self.weapon_index = 0
		self.weapon = list(weapon_data.keys())[self.weapon_index]
		self.can_switch_weapon = True
		self.weapon_switch_time = None
		self.switch_duration_cooldown = 300

		self.create_magic = create_magic
		self.magic_index = 0
		self.magic = list(magic_data.keys())[self.magic_index]
		self.can_switch_magic = True
		self.magic_switch_time = None

		self.stats = {'health':100,'energy':60,'attack':10,'magic':4,'speed':6}
		self.health = self.stats['health']
		self.energy = self.stats['energy']
		self.speed = self.stats['speed']
		self.exp = 123

	def input(self):
		if not self.attacking:
			keys = pygame.key.get_pressed()
			if keys[pygame.K_UP]:
				self.direction.y = -1
				self.status = 'up'
			elif keys[pygame.K_DOWN]:
				self.direction.y = 1
				self.status = 'down'
			else:
				self.direction.y = 0
			if keys[pygame.K_RIGHT] :
				self.direction.x = 1
				self.status = 'right'
			elif keys[pygame.K_LEFT] :
				self.direction.x = -1
				self.status = 'left'
			else:
				self.direction.x = 0
			#ATTACK
			if keys[pygame.K_SPACE]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				self.create_attack()
			#Magic
			if keys[pygame.K_LCTRL]:
				self.attacking = True
				self.attack_time = pygame.time.get_ticks()
				style = list(magic_data.keys())[self.magic_index]
				strength = magic_data[style]['strength'] + self.stats['magic']
				cost = magic_data[style]['cost']
				self.create_magic(style,strength,cost)
			#Weapon Cange input
			if keys[pygame.K_q] and self.can_switch_weapon:
				self.can_switch_weapon = False
				self.weapon_switch_time = pygame.time.get_ticks()
				self.weapon_index +=1
				if self.weapon_index>4:
					self.weapon_index = 0
				self.weapon = list(weapon_data.keys())[self.weapon_index]
			
			if keys[pygame.K_e] and self.can_switch_magic:
				self.can_switch_magic = False
				self.magic_switch_time = pygame.time.get_ticks()
				if self.magic_index < len(list(magic_data.keys())) - 1:
					self.magic_index += 1
				else:
					self.magic_index = 0
				self.magic = list(magic_data.keys())[self.magic_index]
			
	def import_player_assets(self):
		character_path = 'graphics/player/'
		self.animations = {'up':[],'down':[],'left':[],'right':[],
					 'up_idle':[],'down_idle':[],'left_idle':[],'right_idle':[],
					 'up_attack':[],'down_attack':[],'left_attack':[],'right_attack':[]}
		for animation in self.animations.keys():
			full_path = character_path+animation
			self.animations[animation] = import_folder(full_path)
		#print(self.animations)

	def cooldown(self):
		current_time = pygame.time.get_ticks()
		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_attack()
		if not self.can_switch_weapon:
			if current_time - self.weapon_switch_time >= self.switch_duration_cooldown:
				self.can_switch_weapon = True
		if not self.can_switch_magic:
			if current_time - self.magic_switch_time >= self.switch_duration_cooldown:
				self.can_switch_magic = True
		
	def animate(self):
		animation = self.animations[self.status]
		
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.rect = self.image.get_rect(center = self.hitbox.center)
	
	def get_status(self):

		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status:
				self.status = self.status+'_idle'
		if self.attacking:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					self.status = self.status.replace('_idle','_attack')
				else:
					self.status = self.status+'_attack'
		elif 'attack' in self.status:
			self.status = self.status.replace('_attack','_idle')
	
	def update(self):
		self.input()
		self.cooldown()
		self.get_status()
		self.animate()
		self.move(self.speed)