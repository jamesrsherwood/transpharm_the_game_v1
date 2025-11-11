from settings import *
from timer import Timer

class MapTitleSprite(pygame.sprite.Sprite):
	def __init__(self, title, groups, font, player):
		super().__init__(groups)
		self.z = WORLD_LAYERS['text']
		self.player = player
		self.lifetime = 4000  # 4 seconds in milliseconds
		self.timer = Timer(self.lifetime, autostart=True, func=self.kill)

		# text
		text_surf = font.render(title, False, COLORS['black'])
		padding = 10
		width = text_surf.get_width() + padding * 2
		height = text_surf.get_height() + padding * 2

		# background
		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		surf.fill((0,0,0,0))
		pygame.draw.rect(surf, COLORS['pure white'], surf.get_frect(topleft=(0,0)), 0, 5)
		surf.blit(text_surf, text_surf.get_frect(center=(width / 2, height / 2)))

		self.image = surf
		# Position relative to player so it stays at top center of viewable area
		self.y_sort = self.player.y_sort
		self.update_position()

	def update_position(self):
		# Keep the title at the top center of the viewable screen
		# Calculate position relative to player (camera center)
		self.rect = self.image.get_frect(midtop=(
			self.player.rect.centerx,
			self.player.rect.centery - WINDOW_HEIGHT / 2 + 20
		))

	def update(self, dt):
		self.timer.update()
		self.update_position()

class DialogTree:
	def __init__(self, character, player, all_sprites, font, end_dialog):
		self.player = player
		self.character = character
		self.font = font 
		self.all_sprites = all_sprites
		self.end_dialog = end_dialog
		
		self.dialog = list(character.get_dialog())
		self.dialog_num = len(self.dialog)
		self.dialog_index = 0

		self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)
		self.dialog_timer = Timer(250, autostart = True)

	def input(self):
		keys = pygame.key.get_just_pressed()
		if keys[pygame.K_SPACE] and not self.dialog_timer.active:
			self.current_dialog.kill()
			self.dialog_index += 1
			if self.dialog_index < self.dialog_num:
				self.current_dialog = DialogSprite(self.dialog[self.dialog_index], self.character, self.all_sprites, self.font)
				self.dialog_timer.activate()
			else:
				self.end_dialog(self.character)

	def update(self):
		self.dialog_timer.update()
		self.input()

class DialogSprite(pygame.sprite.Sprite):
	def __init__(self, message, character, groups, font):
		super().__init__(groups)
		self.z = WORLD_LAYERS['text']
		self.character = character

		# Calculate max width for text (screen width - padding on both sides)
		max_text_width = WINDOW_WIDTH - (SCREEN_PADDING * 2)

		# Wrap text to fit within screen bounds
		lines = wrap_text(message, font, max_text_width)

		# Render each line
		line_surfs = [font.render(line, False, COLORS['black']) for line in lines]
		line_height = line_surfs[0].get_height() if line_surfs else 0

		# Calculate total dimensions
		padding = 5
		width = max(30, max(surf.get_width() for surf in line_surfs) + padding * 2) if line_surfs else 30
		height = (line_height * len(lines)) + (padding * 2) + (2 * (len(lines) - 1))  # 2px spacing between lines

		# background
		surf = pygame.Surface((width, height), pygame.SRCALPHA)
		surf.fill((0,0,0,0))
		pygame.draw.rect(surf, COLORS['pure white'], surf.get_frect(topleft = (0,0)),0, 5)

		# Blit each line
		y_offset = padding
		for line_surf in line_surfs:
			surf.blit(line_surf, line_surf.get_frect(centerx = width / 2, top = y_offset))
			y_offset += line_height + 2  # 2px spacing between lines

		self.image = surf

		# Position dialog box above character
		ideal_rect = self.image.get_frect(midbottom = character.rect.midtop + vector(0,-10))

		# Get player (camera center) position to calculate screen bounds
		player = character.player
		screen_left = player.rect.centerx - WINDOW_WIDTH / 2 + SCREEN_PADDING
		screen_right = player.rect.centerx + WINDOW_WIDTH / 2 - SCREEN_PADDING
		screen_top = player.rect.centery - WINDOW_HEIGHT / 2 + SCREEN_PADDING
		screen_bottom = player.rect.centery + WINDOW_HEIGHT / 2 - SCREEN_PADDING

		# Clamp dialog box within screen bounds
		self.rect = ideal_rect
		if self.rect.left < screen_left:
			self.rect.left = screen_left
		if self.rect.right > screen_right:
			self.rect.right = screen_right
		if self.rect.top < screen_top:
			self.rect.top = screen_top
		if self.rect.bottom > screen_bottom:
			self.rect.bottom = screen_bottom