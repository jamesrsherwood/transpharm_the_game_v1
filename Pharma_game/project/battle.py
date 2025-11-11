from settings import * 
from sprites import MonsterSprite, MonsterNameSprite, MonsterLevelSprite, MonsterStatsSprite, MonsterOutlineSprite
from groups import BattleSprites
from support import draw_bar
from timer import Timer
from monster import Monster

class Battle:
	# main
	def __init__(self, player_monsters, opponent_monsters, monster_frames, bg_surf, fonts, end_battle, character):
		# general
		self.display_surface = pygame.display.get_surface()
		self.bg_surf = bg_surf
		self.monster_frames = monster_frames
		self.fonts = fonts
		self.character = character
		
		# Get character-specific data
		from game_data import NPC_DATA
		self.character_id = None
		for npc_id, npc_data in NPC_DATA.items():
			if npc_data is character.character_data:
				self.character_id = npc_id
				break

		# Check if this is factory2 (temperature and duration selection)
		if self.character_id == 'factory2':
			self.is_factory2 = True
			self.temperatures = [25, 50, 75, 100]
			self.durations = [1, 2, 3, 4, 5, 6, 7, 8]
			self.selected_temperature_index = 0
			self.selected_duration_index = 0
			self.selection_mode = 'temperature'  # 'temperature', 'duration', or 'exit'
			self.player_monsters = player_monsters
		else:
			self.is_factory2 = False
			# Original battle code for other characters
			self.monster_lists = {}
			self.column_names = []
			
			if self.character_id == 'scientist':
				self.monster_lists = {
					'FG_left': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('FG_left', {}).items()},
					'molecule_template_left': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('molecule_template_left', {}).items()},
					'molecule_template_right': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('molecule_template_right', {}).items()},
					'FG_right': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('FG_right', {}).items()}
				}
				self.column_names = ['FG_left', 'molecule_template_left', 'molecule_template_right', 'FG_right']
			elif self.character_id == 'factory0':
				self.monster_lists = {
					'safety': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('safety', {}).items()},
					'emissions': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('emissions', {}).items()},
					'energy': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('energy', {}).items()}
				}
				self.column_names = ['safety', 'emissions', 'energy']
			elif self.character_id == 'medic':
				self.monster_lists = {
					'cups': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('cups', {}).items()},
					'deprescribe': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('deprescribe', {}).items()}
				}
				self.column_names = ['cups', 'deprescribe']
			elif self.character_id == 'ngo':
				self.monster_lists = {
					'procurement': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('procurement', {}).items()},
					'pollution_standards': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('pollution_standards', {}).items()},
					'biodegradation_standards': {k: Monster(name, lvl) for k, (name, lvl) in character.character_data.get('biodegradation_standards', {}).items()}
				}
				self.column_names = ['procurement', 'pollution_standards', 'biodegradation_standards']
			else:
				self.monster_lists = {'monsters': opponent_monsters}
				self.column_names = ['monsters']
			
			self.player_monsters = player_monsters
			self.title = self.get_title()
			self.default_indices = self.get_default_indices()
			self.selected_indices = {col: self.default_indices.get(col, 0) for col in self.column_names}
			self.current_column = 0
			# Start with the currently selected item highlighted, not just the default
			self.current_index = self.selected_indices.get(self.column_names[0], 0)
			self.selection_mode = 'monster'
			
			# menu dimensions
			self.menu_rect = pygame.FRect(0, 0, WINDOW_WIDTH * 0.85, WINDOW_HEIGHT * 0.85).move_to(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
			self.title_height = 60
			self.animation_display_height = 150
			self.exit_button_height = 80
			self.monster_list_top = self.menu_rect.top + self.title_height + self.animation_display_height
			self.monster_list_height = self.menu_rect.height - self.title_height - self.animation_display_height - self.exit_button_height
			self.visible_items = 3
			self.item_height = self.monster_list_height / self.visible_items
			self.num_columns = len(self.column_names)
			self.column_width = self.menu_rect.width / self.num_columns if self.num_columns > 0 else self.menu_rect.width
			self.animation_frame_index = 0

		self.battle_over = False
		self.end_battle = end_battle

		# tint surf
		self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_surf.set_alpha(200)

		self.setup()

	def get_title(self):
		"""Get character-specific title"""
		titles = {
			'factory0': 'Pharmaceutical Manufacturing',
			'medic': 'Medical Treatment',
			'scientist': 'Drug Chemistry',
			'ngo': 'Environmental Policy'
		}
		return titles.get(self.character_id, 'Battle')

	def get_default_indices(self):
		"""Get default selection index for each column based on current player_monsters"""
		default_indices = {}

		if self.character_id == 'scientist':
			slots = {'FG_left': 0, 'molecule_template_left': 1, 'molecule_template_right': 2, 'FG_right': 3}
			for col_name in self.column_names:
				slot = slots[col_name]
				current_monster = self.player_monsters.get(slot)
				if current_monster:
					# Find this monster in the available list
					monster_list = list(self.monster_lists[col_name].values())
					for idx, monster in enumerate(monster_list):
						if monster.name == current_monster.name:
							default_indices[col_name] = idx
							break
					else:
						default_indices[col_name] = 0
				else:
					default_indices[col_name] = 0
		elif self.character_id == 'factory0':
			slots = {'safety': 4, 'emissions': 5, 'energy': 6}
			for col_name in self.column_names:
				slot = slots[col_name]
				current_monster = self.player_monsters.get(slot)
				if current_monster:
					monster_list = list(self.monster_lists[col_name].values())
					for idx, monster in enumerate(monster_list):
						if monster.name == current_monster.name:
							default_indices[col_name] = idx
							break
					else:
						default_indices[col_name] = 0
				else:
					default_indices[col_name] = 0
		elif self.character_id == 'medic':
			slots = {'cups': 7, 'deprescribe': 8}
			for col_name in self.column_names:
				slot = slots[col_name]
				current_monster = self.player_monsters.get(slot)
				if current_monster:
					monster_list = list(self.monster_lists[col_name].values())
					for idx, monster in enumerate(monster_list):
						if monster.name == current_monster.name:
							default_indices[col_name] = idx
							break
					else:
						default_indices[col_name] = 0
				else:
					default_indices[col_name] = 0
		elif self.character_id == 'ngo':
			slots = {'procurement': 9, 'pollution_standards': 10, 'biodegradation_standards': 11}
			for col_name in self.column_names:
				slot = slots[col_name]
				current_monster = self.player_monsters.get(slot)
				if current_monster:
					monster_list = list(self.monster_lists[col_name].values())
					for idx, monster in enumerate(monster_list):
						if monster.name == current_monster.name:
							default_indices[col_name] = idx
							break
					else:
						default_indices[col_name] = 0
				else:
					default_indices[col_name] = 0
		else:
			default_indices = {'monsters': 0}

		return default_indices

	def get_slot_index(self):
		"""Get which player_monsters slot this character updates"""
		if self.character_id == 'scientist':
			slots = {'FG_left': 0, 'molecule_template_left': 1, 'molecule_template_right': 2, 'FG_right': 3}
			return slots.get(self.column_names[self.current_column], 2)
		elif self.character_id == 'factory0':
			slots = {'safety': 4, 'emissions': 5, 'energy': 6}
			return slots.get(self.column_names[self.current_column], 0)
		elif self.character_id == 'medic':
			slots = {'cups': 7, 'deprescribe': 8}
			return slots.get(self.column_names[self.current_column], 1)
		elif self.character_id == 'ngo':
			slots = {'procurement': 9, 'pollution_standards': 10, 'biodegradation_standards': 11}
			return slots.get(self.column_names[self.current_column], 3)
		else:
			return 0

	def setup(self):
		pass

	def input_factory2(self):
		"""Handle input for factory2 temperature and duration selection"""
		keys = pygame.key.get_just_pressed()
		
		if self.selection_mode == 'temperature':
			if keys[pygame.K_LEFT]:
				self.selected_temperature_index = (self.selected_temperature_index - 1) % len(self.temperatures)
			if keys[pygame.K_RIGHT]:
				self.selected_temperature_index = (self.selected_temperature_index + 1) % len(self.temperatures)
			if keys[pygame.K_DOWN]:
				self.selection_mode = 'duration'
			if keys[pygame.K_SPACE]:
				# Store temperature selection (you can add to player_monsters or a separate dict)
				print(f"Selected temperature: {self.temperatures[self.selected_temperature_index]}°C")
				self.selection_mode = 'duration'
		
		elif self.selection_mode == 'duration':
			if keys[pygame.K_LEFT]:
				self.selected_duration_index = (self.selected_duration_index - 1) % len(self.durations)
			if keys[pygame.K_RIGHT]:
				self.selected_duration_index = (self.selected_duration_index + 1) % len(self.durations)
			if keys[pygame.K_UP]:
				self.selection_mode = 'temperature'
			if keys[pygame.K_DOWN]:
				self.selection_mode = 'exit'
			if keys[pygame.K_SPACE]:
				# Store duration selection
				print(f"Selected duration: {self.durations[self.selected_duration_index]} hours")
				self.selection_mode = 'exit'
		
		elif self.selection_mode == 'exit':
			if keys[pygame.K_UP]:
				self.selection_mode = 'duration'
			if keys[pygame.K_SPACE]:
				# Save selections and exit
				temp = self.temperatures[self.selected_temperature_index]
				duration = self.durations[self.selected_duration_index]
				print(f"Final selections - Temperature: {temp}°C, Duration: {duration}h")
				
				# Store in player_monsters dict as special entries
				# You can use slots 12 and 13 for temperature and duration
				from monster import Monster
				# Create dummy monsters to store these values in their level attribute
				self.player_monsters[12] = Monster('Standard PPE', temp)  # Using level to store temperature
				self.player_monsters[13] = Monster('Standard PPE', duration)  # Using level to store duration
				
				self.end_battle(self.character)

	def input_standard(self):
		"""Handle input for standard monster selection battles"""
		keys = pygame.key.get_just_pressed()
		
		if self.selection_mode == 'monster':
			current_col_name = self.column_names[self.current_column]
			max_index = len(self.monster_lists[current_col_name]) - 1
			
			if max_index < 0:
				if keys[pygame.K_LEFT] and self.current_column > 0:
					self.current_column -= 1
					self.current_index = self.selected_indices[self.column_names[self.current_column]]
				elif keys[pygame.K_RIGHT] and self.current_column < self.num_columns - 1:
					self.current_column += 1
					self.current_index = self.selected_indices[self.column_names[self.current_column]]
				elif keys[pygame.K_DOWN]:
					self.selection_mode = 'exit'
				return
			
			if keys[pygame.K_UP]:
				self.current_index = (self.current_index - 1) % (max_index + 1)
			
			if keys[pygame.K_DOWN]:
				if self.current_index == max_index:
					self.selection_mode = 'exit'
				else:
					self.current_index = (self.current_index + 1) % (max_index + 1)
			
			if keys[pygame.K_LEFT]:
				if self.current_column > 0:
					self.selected_indices[current_col_name] = self.current_index
					self.current_column -= 1
					self.current_index = self.selected_indices[self.column_names[self.current_column]]
			
			if keys[pygame.K_RIGHT]:
				if self.current_column < self.num_columns - 1:
					self.selected_indices[current_col_name] = self.current_index
					self.current_column += 1
					self.current_index = self.selected_indices[self.column_names[self.current_column]]
			
			if keys[pygame.K_SPACE]:
				self.selected_indices[current_col_name] = self.current_index
				monster_list = list(self.monster_lists[current_col_name].values())
				selected_monster = monster_list[self.current_index]
				slot = self.get_slot_index()
				self.player_monsters[slot] = selected_monster
		
		elif self.selection_mode == 'exit':
			if keys[pygame.K_UP]:
				self.selection_mode = 'monster'
				current_col_name = self.column_names[self.current_column]
				max_index = len(self.monster_lists[current_col_name]) - 1
				if max_index >= 0:
					self.current_index = max_index
				else:
					self.current_index = 0
			
			if keys[pygame.K_SPACE]:
				self.end_battle(self.character)

	def draw_factory2_screen(self):
		"""Draw the factory2 temperature and duration selection screen"""
		# Main menu background
		menu_rect = pygame.FRect(0, 0, WINDOW_WIDTH * 0.7, WINDOW_HEIGHT * 0.7).move_to(center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
		pygame.draw.rect(self.display_surface, COLORS['dark'], menu_rect, 0, 12)
		
		# Title
		title_text = "Reaction Conditions"
		title_surf = self.fonts['bold'].render(title_text, False, COLORS['white'])
		title_rect = title_surf.get_frect(center=(menu_rect.centerx, menu_rect.top + 40))
		self.display_surface.blit(title_surf, title_rect)
		
		# Temperature section
		temp_label = "Temperature (°C):"
		temp_label_surf = self.fonts['regular'].render(temp_label, False, COLORS['white'])
		temp_label_rect = temp_label_surf.get_frect(topleft=(menu_rect.left + 50, menu_rect.top + 100))
		self.display_surface.blit(temp_label_surf, temp_label_rect)
		
		# Draw temperature options in a row
		temp_y = temp_label_rect.bottom + 20
		temp_spacing = (menu_rect.width - 100) / len(self.temperatures)
		
		for i, temp in enumerate(self.temperatures):
			x = menu_rect.left + 50 + i * temp_spacing
			temp_rect = pygame.FRect(x, temp_y, 80, 50)
			
			# Highlight selected temperature
			if i == self.selected_temperature_index and self.selection_mode == 'temperature':
				pygame.draw.rect(self.display_surface, COLORS['gold'], temp_rect, 0, 8)
			else:
				pygame.draw.rect(self.display_surface, COLORS['light-gray'], temp_rect, 0, 8)
			
			# Draw temperature value
			temp_text = f"{temp}°C"
			temp_surf = self.fonts['regular'].render(temp_text, False, COLORS['black'])
			temp_text_rect = temp_surf.get_frect(center=temp_rect.center)
			self.display_surface.blit(temp_surf, temp_text_rect)
		
		# Duration section
		dur_label = "Duration (hours):"
		dur_label_surf = self.fonts['regular'].render(dur_label, False, COLORS['white'])
		dur_label_rect = dur_label_surf.get_frect(topleft=(menu_rect.left + 50, temp_y + 80))
		self.display_surface.blit(dur_label_surf, dur_label_rect)
		
		# Draw duration options in two rows
		dur_y = dur_label_rect.bottom + 20
		dur_spacing = (menu_rect.width - 100) / 4
		
		for i, duration in enumerate(self.durations):
			row = i // 4
			col = i % 4
			x = menu_rect.left + 50 + col * dur_spacing
			y = dur_y + row * 60
			dur_rect = pygame.FRect(x, y, 80, 50)
			
			# Highlight selected duration
			if i == self.selected_duration_index and self.selection_mode == 'duration':
				pygame.draw.rect(self.display_surface, COLORS['gold'], dur_rect, 0, 8)
			else:
				pygame.draw.rect(self.display_surface, COLORS['light-gray'], dur_rect, 0, 8)
			
			# Draw duration value
			dur_text = f"{duration}h"
			dur_surf = self.fonts['regular'].render(dur_text, False, COLORS['black'])
			dur_text_rect = dur_surf.get_frect(center=dur_rect.center)
			self.display_surface.blit(dur_surf, dur_text_rect)
		
		# Exit button
		button_width = 200
		button_height = 50
		button_x = menu_rect.centerx - button_width / 2
		button_y = menu_rect.bottom - 80
		
		button_rect = pygame.FRect(button_x, button_y, button_width, button_height)
		button_color = COLORS['gold'] if self.selection_mode == 'exit' else COLORS['white']
		pygame.draw.rect(self.display_surface, button_color, button_rect, 0, 10)
		
		text = "CONFIRM (SPACE)"
		text_surf = self.fonts['regular'].render(text, False, COLORS['black'])
		text_rect = text_surf.get_frect(center=button_rect.center)
		self.display_surface.blit(text_surf, text_rect)
		
		# Instructions
		if self.selection_mode == 'temperature':
			inst_text = "LEFT/RIGHT: Select Temperature | DOWN: Next | SPACE: Confirm"
		elif self.selection_mode == 'duration':
			inst_text = "LEFT/RIGHT: Select Duration | UP: Back | DOWN: Confirm | SPACE: Confirm"
		else:
			inst_text = "UP: Back | SPACE: Finish"
		
		inst_surf = self.fonts['small'].render(inst_text, False, COLORS['light'])
		inst_rect = inst_surf.get_frect(center=(menu_rect.centerx, menu_rect.bottom - 20))
		self.display_surface.blit(inst_surf, inst_rect)

	def draw_standard_screen(self, dt):
		"""Draw standard monster selection screen"""
		self.draw_menu_background()
		self.draw_title()
		self.draw_selected_animations()
		self.draw_exit_button()
		#self.draw_instructions()

	def draw_title(self):
		"""Draw the character-specific title at the top"""
		title_surf = self.fonts['bold'].render(self.title, False, COLORS['white'])
		title_rect = title_surf.get_frect(center=(self.menu_rect.centerx, self.menu_rect.top + self.title_height / 2))
		self.display_surface.blit(title_surf, title_rect)

	def draw_selected_animations(self):
		"""Draw monster animations above each column showing selected monsters"""
		animation_y = self.menu_rect.top + self.title_height + self.animation_display_height / 2
		
		if self.character_id == 'scientist':
			scaled_frames = []
			for col_index, col_name in enumerate(self.column_names):
				selected_idx = self.selected_indices[col_name]
				monster_list = list(self.monster_lists[col_name].values())
				if selected_idx < len(monster_list):
					selected_monster = monster_list[selected_idx]
					frames = self.monster_frames['monsters'][selected_monster.name]['idle']
					current_frame = frames[int(self.animation_frame_index) % len(frames)]
					
					max_animation_size = self.animation_display_height * 0.9
					animation_scale = min(max_animation_size / current_frame.get_width(), max_animation_size / current_frame.get_height())
					if animation_scale < 1:
						new_size = (int(current_frame.get_width() * animation_scale), int(current_frame.get_height() * animation_scale))
						current_frame = pygame.transform.scale(current_frame, new_size)
					
					scaled_frames.append(current_frame)
				else:
					scaled_frames.append(None)
			
			total_width = sum(frame.get_width() for frame in scaled_frames if frame is not None)
			start_x = self.menu_rect.centerx - total_width / 2
			
			current_x = start_x
			for frame in scaled_frames:
				if frame is not None:
					animation_rect = frame.get_frect(midleft=(current_x, animation_y))
					self.display_surface.blit(frame, animation_rect)
					current_x += frame.get_width()
		else:
			for col_index, col_name in enumerate(self.column_names):
				col_x = self.menu_rect.left + col_index * self.column_width + self.column_width / 2
				
				selected_idx = self.selected_indices[col_name]
				monster_list = list(self.monster_lists[col_name].values())
				if selected_idx < len(monster_list):
					selected_monster = monster_list[selected_idx]
					
					frames = self.monster_frames['monsters'][selected_monster.name]['idle']
					current_frame = frames[int(self.animation_frame_index) % len(frames)]
					
					max_animation_size = self.animation_display_height * 0.9
					animation_scale = min(max_animation_size / current_frame.get_width(), max_animation_size / current_frame.get_height())
					if animation_scale < 1:
						new_size = (int(current_frame.get_width() * animation_scale), int(current_frame.get_height() * animation_scale))
						current_frame = pygame.transform.scale(current_frame, new_size)
					
					animation_rect = current_frame.get_frect(center=(col_x, animation_y))
					self.display_surface.blit(current_frame, animation_rect)

	def draw_menu_background(self):
		"""Draw the menu background and monster list"""
		pygame.draw.rect(self.display_surface, COLORS['dark'], self.menu_rect, 0, 12)
		
		title_rect = pygame.FRect(self.menu_rect.left, self.menu_rect.top, self.menu_rect.width, self.title_height)
		pygame.draw.rect(self.display_surface, COLORS['light-gray'], title_rect, 0, 12, 12, 0, 0)
		
		animation_rect = pygame.FRect(self.menu_rect.left, self.menu_rect.top + self.title_height, self.menu_rect.width, self.animation_display_height)
		pygame.draw.rect(self.display_surface, COLORS['gray'], animation_rect, 0)
		
		for col_index, col_name in enumerate(self.column_names):
			base_x = self.menu_rect.left + col_index * self.column_width
			
			if col_index == self.current_column and self.selection_mode == 'monster':
				column_highlight = pygame.FRect(base_x, self.monster_list_top, self.column_width, self.monster_list_height)
				pygame.draw.rect(self.display_surface, COLORS['light-gray'], column_highlight, 3)
			
			list_clip_rect = pygame.Rect(int(base_x), int(self.monster_list_top), int(self.column_width), int(self.monster_list_height))
			
			current_col_index = self.current_index if col_name == self.column_names[self.current_column] else self.selected_indices[col_name]
			v_offset = 0 if current_col_index < self.visible_items else -(current_col_index - self.visible_items + 1) * self.item_height
			
			for i, monster in enumerate(list(self.monster_lists[col_name].values())):
				item_top = self.monster_list_top + i * self.item_height + v_offset
				item_rect = pygame.FRect(base_x, item_top, self.column_width, self.item_height)
				
				if item_rect.colliderect(list_clip_rect):
					if self.selection_mode == 'monster' and col_index == self.current_column and self.current_index == i:
						pygame.draw.rect(self.display_surface, COLORS['light'], item_rect, 0)
					
					if self.selected_indices[col_name] == i:
						selection_surf = pygame.Surface((item_rect.width, item_rect.height))
						selection_surf.fill(COLORS['gold'])
						selection_surf.set_alpha(50)
						self.display_surface.blit(selection_surf, item_rect.topleft)
					
					icon_surf = self.monster_frames['icons'][monster.name]
					
					max_icon_size = self.item_height * 0.6
					icon_scale = min(max_icon_size / icon_surf.get_width(), max_icon_size / icon_surf.get_height())
					if icon_scale < 1:
						new_size = (int(icon_surf.get_width() * icon_scale), int(icon_surf.get_height() * icon_scale))
						icon_surf = pygame.transform.scale(icon_surf, new_size)
					
					icon_rect = icon_surf.get_frect(midleft=(item_rect.left + 10, item_rect.centery))
					self.display_surface.blit(icon_surf, icon_rect)
					
					name_surf = self.fonts['small'].render(monster.name, False, COLORS['white'])
					name_rect = name_surf.get_frect(midleft=(icon_rect.right + 10, item_rect.centery))
					self.display_surface.blit(name_surf, name_rect)
					
					if i == self.default_indices.get(col_name, 0):
						default_text = self.fonts['small'].render('(default)', False, COLORS['gold'])
						default_rect = default_text.get_frect(topright=(item_rect.right - 5, item_rect.top + 5))
						self.display_surface.blit(default_text, default_rect)
					
					if i < len(self.monster_lists[col_name]) - 1:
						y = item_rect.bottom
						if self.monster_list_top <= y <= self.monster_list_top + self.monster_list_height:
							pygame.draw.line(self.display_surface, COLORS['light-gray'], (base_x + 5, y), (base_x + self.column_width - 5, y), 1)
			
			if col_index < self.num_columns - 1:
				separator_x = base_x + self.column_width
				pygame.draw.line(self.display_surface, COLORS['white'], (separator_x, self.monster_list_top), (separator_x, self.monster_list_top + self.monster_list_height), 2)

	def draw_exit_button(self):
		"""Draw exit button at bottom of menu"""
		button_width = 200
		button_height = 50
		button_x = self.menu_rect.centerx - button_width / 2
		button_y = self.menu_rect.bottom - 60
		
		button_rect = pygame.FRect(button_x, button_y, button_width, button_height)
		button_color = COLORS['gold'] if self.selection_mode == 'exit' else COLORS['white']
		pygame.draw.rect(self.display_surface, button_color, button_rect, 0, 10)
		
		text = "EXIT (SPACE)"
		text_surf = self.fonts['regular'].render(text, False, COLORS['black'])
		text_rect = text_surf.get_frect(center=button_rect.center)
		self.display_surface.blit(text_surf, text_rect)

	def draw_instructions(self):
		"""Draw instruction text at bottom"""
		if self.selection_mode == 'monster':
			if self.num_columns > 1:
				text = "UP/DOWN: Navigate | LEFT/RIGHT: Change Column | SPACE: Select"
			else:
				text = "UP/DOWN: Navigate | SPACE: Select"
		else:
			text = "UP: Back to Monsters | SPACE: Exit Battle"
		
		text_surf = self.fonts['small'].render(text, False, COLORS['light'])
		text_rect = text_surf.get_frect(center=(self.menu_rect.centerx, self.menu_rect.bottom - 20))
		self.display_surface.blit(text_surf, text_rect)

	def update(self, dt):
		# Handle input based on character type
		if self.is_factory2:
			self.input_factory2()
		else:
			self.input_standard()
			self.animation_frame_index += INDEX_ANIMATION_SPEED * dt

		# Drawing
		self.display_surface.blit(self.bg_surf, (0, 0))
		self.display_surface.blit(self.tint_surf, (0, 0))
		
		if self.is_factory2:
			self.draw_factory2_screen()
		else:
			self.draw_standard_screen(dt)