import pygame, sys
from settings import *
from level import Level

class Game:
	def __init__(self):
		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
		pygame.display.set_caption('Zelda')
		self.clock = pygame.time.Clock()
		self.level = Level()
		main_sound = pygame.mixer.Sound('audio/main.ogg')
		main_sound.set_volume(0.5)
		main_sound.play(loops=-1)
	
	def run(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_m:
						self.level.toggle_menu()
						
			self.screen.fill(WATER_COLOR)
			self.level.run()
			pygame.display.update()
			self.clock.tick(FPS)

	def death(self):
		font = pygame.font.Font(None, 36)
		text = font.render("You died!", True, TEXT_COLOR)
		text_rect = text.get_rect(center=(WIDTH // 2, HEIGTH // 2))
		self.screen.fill(UI_BG_COLOR)
		self.screen.blit(text,text_rect)
		pygame.display.update()


if __name__ == '__main__':
	game = Game()

	game.run()