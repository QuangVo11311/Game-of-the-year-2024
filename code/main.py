import pygame, sys
from settings import *
from level import Level
from itertools import cycle
BLINK_EVENT = pygame.USEREVENT + 0

class Game:
	def __init__(self):

		# general setup
		pygame.init()
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		pygame.display.set_caption('PixelWar Project')
		self.clock = pygame.time.Clock()

		self.level = Level()

		# sound 
		main_sound = pygame.mixer.Sound('../audio/main.mp3')
		main_sound.set_volume(0.5)
		self.accept = pygame.mixer.Sound('../audio/Accept.wav')
		self.accept.set_volume(0.2)
		self.state = 'intro'
		self.started = False
		main_sound.play(loops = -1)
		self.font = pygame.font.Font(UI_FONT, 50)
		self.screen_rect = self.screen.get_rect()
		self.game_over = False

        # title
		title_surf = self.font.render('press enter to start', True, (255,255,255))
		self.title_rect = title_surf.get_rect(center = (self.screen_rect.center[0], self.screen_rect.center[1] + 120))
		off_text_surf = pygame.Surface(self.title_rect.size, pygame.SRCALPHA, 32)
		off_text_surf = off_text_surf.convert_alpha()
		self.blink_surfaces = cycle([title_surf, off_text_surf])
		self.blink_surf = next(self.blink_surfaces)
	
	def intro(self):
		if not self.started:
			self.level.visible_sprites.custom_draw(self.level.player)
                
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						self.accept.play()
						self.started = True
						self.state = 'main_game'
				if event.type == BLINK_EVENT:
					self.blink_surf = next(self.blink_surfaces)
			self.screen.blit(self.blink_surf, self.title_rect)
			pygame.display.update()

	def state_manager(self):
		if self.state == 'intro':
			self.intro()
		if self.state == 'main_game':
			self.main_game()
		if self.state == 'restart':
			self.game_over = True
			self.level = Level()
			self.state = 'main_game'

	def main_game(self):
		self.screen.fill(WATER_COLOR)
		self.level.run()
		pygame.display.update()
		if self.game_over:
			self.game_over = False
			self.accept.play()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_m:
					self.level.toggle_menu()
		if self.level.player.health < 0 and self.level.player.restart_pressed:
			self.state = 'restart'

	def run(self):
		while True:
			self.state_manager()
			self.clock.tick(FPS)

if __name__ == '__main__':
	game = Game()
	game.run()