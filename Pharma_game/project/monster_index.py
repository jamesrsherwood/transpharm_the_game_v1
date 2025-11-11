from settings import * 
from support import draw_bar
from game_data import MONSTER_DATA
from calculations import (
    calculate_city_scale_indicators,
    check_compliance_thresholds,
    calculate_factory_waste_per_gram,
    calculate_worker_risk,
    calculate_ecotoxicity,
    get_doses_per_gram_from_choices,
    get_patient_count,
    molecule_stats,
    get_drug_code_from_choices
)
from item_descriptions import get_item_description, get_drug_description

class MonsterIndex:
	def __init__(self, monsters, fonts, monster_frames):
		self.display_surface = pygame.display.get_surface()
		self.fonts = fonts
		self.monsters = monsters
		self.frame_index = 0

		# frames 
		self.icon_frames = monster_frames['icons']
		self.monster_frames = monster_frames['monsters']
		self.ui_frames = monster_frames['ui']

		# tint surf 
		self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_surf.set_alpha(200)

		# dimensions
		self.main_rect = pygame.FRect(0,0,WINDOW_WIDTH * 0.8, WINDOW_HEIGHT * 0.9).move_to(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))

		# list 
		self.visible_items = 6
		self.list_width = self.main_rect.width * 0.25
		self.item_height = self.main_rect.height / self.visible_items
		self.index = 0

		# Display list will be created dynamically
		self.display_monsters = {}
		
		# Calculate max values for bar scaling
		self.max_values = self._calculate_bar_max_values()
		
		# Calculate mean ecotoxicity threshold
		self.mean_ecotoxicity = self._calculate_mean_ecotoxicity()

		# Message scrolling
		self.message_scroll_offset = 0
		self.message_scroll_timer = 0
		self.message_scroll_speed = 2.5  # seconds per scroll

	def _calculate_mean_ecotoxicity(self):
		"""Calculate mean ecotoxicity across all compounds for threshold"""
		from calculations import molecule_stats
		
		raw_api = 0.02
		max_scale_factor = 20  # 60 patients / 3 min doses
		
		ecotox_values = []
		for drug_code, stats in molecule_stats.items():
			biodeg_api = stats['biodegAPI']
			biodeg_meta = stats['biodegMeta']
			tox_api = stats['toxAPI']
			tox_meta = stats['toxMeta']
			
			final_api = raw_api * (1 - biodeg_api)
			final_meta = ((raw_api * biodeg_api) + 1) * (1 - biodeg_meta)
			
			ecotoxicity_per_g = (final_api * tox_api) + (final_meta * tox_meta)
			city_ecotoxicity = ecotoxicity_per_g * max_scale_factor
			
			ecotox_values.append(city_ecotoxicity)
		
		return sum(ecotox_values) / len(ecotox_values)

	def _calculate_bar_max_values(self):
		"""Calculate maximum possible values for each metric from molecule stats"""
		max_values = {
			'worker_exposure': 0,
			'city_cost': 0,
			'city_impact': 0,
			'city_waste': 0,
			'city_pollution': 0,
			'city_ecotoxicity': 0
		}
		
		# Import necessary functions
		from calculations import (
			molecule_stats, 
			total_patients,
			cost_closed_safety,
			cost_cup2,
			penalty_basic,
			gwp_cup2
		)
		
		# City scale factor using actual minimum doses (3, not 2)
		# Doses range from 3-6 based on efficacy, so max scale is at min doses
		min_doses = 3
		max_scale_factor = total_patients / min_doses  # 60 / 3 = 20
		
		# Find max worker exposure (no safety equipment)
		for drug_code, stats in molecule_stats.items():
			max_values['worker_exposure'] = max(max_values['worker_exposure'], stats['exposureNo'])
		
		# Find max waste (city scale)
		for drug_code, stats in molecule_stats.items():
			city_waste = stats['waste'] * max_scale_factor
			max_values['city_waste'] = max(max_values['city_waste'], city_waste)
		
		# Find max cost (city scale = factory cost scaled + daily costs)
		# Max daily costs: closed safety (75) + expensive cups (0.5 * 60) + fine (40)
		max_daily_cost = cost_closed_safety + (cost_cup2 * total_patients) + penalty_basic
		for drug_code, stats in molecule_stats.items():
			factory_city_cost = stats['cost'] * max_scale_factor
			total_city_cost = factory_city_cost + max_daily_cost
			max_values['city_cost'] = max(max_values['city_cost'], total_city_cost)
		
		# Find max CO2 impact across all combinations
		for drug_code, stats in molecule_stats.items():
			# Worst case: highest base impact + energy at max temp/duration with normal energy
			max_temp = 100
			max_duration = 8
			energy_kwh = 0.001 * ((8 * (max_temp - 20)) + (1.33 * (max_temp - 20) * max_duration))
			energy_impact = energy_kwh * 250  # normal_energy_gwp
			
			factory_impact = stats['impact'] + energy_impact
			
			# Calculate actual doses per gram for this drug based on efficacy
			import math
			efficacy = stats['efficacy']
			doses_per_gram = 2 + math.ceil(3 * (efficacy - 1.94) / 1.85)
			
			# Scale up by actual doses per gram (lower doses = higher scale factor = more CO2)
			scale_factor = total_patients / doses_per_gram
			scaled_impact = factory_impact * scale_factor
			
			# Add cup impact
			cup_impact = gwp_cup2 * total_patients
			
			total_impact = scaled_impact + cup_impact
			max_values['city_impact'] = max(max_values['city_impact'], total_impact)

		# Find max pollution (city scale)
		for drug_code, stats in molecule_stats.items():
			# Calculate per-gram pollution
			raw_api = 0.02
			biodeg_api = stats['biodegAPI']
			biodeg_meta = stats['biodegMeta']
			
			final_api = raw_api * (1 - biodeg_api)
			final_meta = ((raw_api * biodeg_api) + 1) * (1 - biodeg_meta)
			
			pollution_per_g = final_api + final_meta
			city_pollution = pollution_per_g * max_scale_factor
			max_values['city_pollution'] = max(max_values['city_pollution'], city_pollution)
		
		# Find max ecotoxicity (city scale)
		for drug_code, stats in molecule_stats.items():
			# Calculate per-gram ecotoxicity
			raw_api = 0.02
			biodeg_api = stats['biodegAPI']
			biodeg_meta = stats['biodegMeta']
			tox_api = stats['toxAPI']
			tox_meta = stats['toxMeta']
			
			final_api = raw_api * (1 - biodeg_api)
			final_meta = ((raw_api * biodeg_api) + 1) * (1 - biodeg_meta)
			
			ecotoxicity_per_g = (final_api * tox_api) + (final_meta * tox_meta)
			city_ecotoxicity = ecotoxicity_per_g * max_scale_factor
			max_values['city_ecotoxicity'] = max(max_values['city_ecotoxicity'], city_ecotoxicity)
		
		return max_values

	def _create_display_list(self):
		"""Create display list combining scientist monsters (slots 0-3) into one entry"""
		display_list = {}
		
		# Combine scientist monsters (slots 0-3) into one entry
		if all(i in self.monsters for i in range(4)):
			display_list[0] = {
				'type': 'combined',
				'name': 'Molecule',
				'monsters': [self.monsters[i] for i in range(4)],
				'slots': [0, 1, 2, 3]
			}
			next_index = 1
		else:
			next_index = 0
		
		# Add remaining monsters individually (excluding slots 12 and 13 - temperature and duration)
		for slot_index in range(4, len(self.monsters)):
			if slot_index in self.monsters and slot_index not in [12, 13]:
				display_list[next_index] = {
					'type': 'single',
					'monster': self.monsters[slot_index],
					'slot': slot_index
				}
				next_index += 1
		
		return display_list
		"""Create display list combining scientist monsters (slots 0-3) into one entry"""
		display_list = {}
		
		# Combine scientist monsters (slots 0-3) into one entry
		if all(i in self.monsters for i in range(4)):
			display_list[0] = {
				'type': 'combined',
				'name': 'Molecule',
				'monsters': [self.monsters[i] for i in range(4)],
				'slots': [0, 1, 2, 3]
			}
			next_index = 1
		else:
			next_index = 0
		
		# Add remaining monsters individually
		for slot_index in range(4, len(self.monsters)):
			if slot_index in self.monsters:
				display_list[next_index] = {
					'type': 'single',
					'monster': self.monsters[slot_index],
					'slot': slot_index
				}
				next_index += 1
		
		return display_list

	def input(self):
		keys = pygame.key.get_just_pressed()
		
		# Regenerate display list to reflect any changes
		self.display_monsters = self._create_display_list()
		
		if keys[pygame.K_UP]:
			self.index -= 1
		if keys[pygame.K_DOWN]:
			self.index += 1

		self.index = self.index % len(self.display_monsters)

	def display_list(self):
		# Regenerate display list to reflect current monster state
		self.display_monsters = self._create_display_list()
		
		bg_rect = pygame.FRect(self.main_rect.topleft,(self.list_width, self.main_rect.height))
		pygame.draw.rect(self.display_surface, COLORS['gray'], bg_rect, 0, 0, 12, 0, 12, 0)
		
		v_offset = 0 if self.index < self.visible_items else -(self.index - self.visible_items + 1) * self.item_height
		for index, entry in self.display_monsters.items():
			# colours
			bg_color = COLORS['gray'] if self.index != index else COLORS['light']
			text_color = COLORS['white']
			
			top = self.main_rect.top + index * self.item_height + v_offset
			item_rect = pygame.FRect(self.main_rect.left, top, self.list_width, self.item_height)

			if entry['type'] == 'combined':
				# Draw combined entry
				if item_rect.colliderect(self.main_rect):
					# Draw background
					if item_rect.collidepoint(self.main_rect.topleft):
						pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 12)
					elif item_rect.collidepoint(self.main_rect.bottomleft + vector(1, -1)):
						pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 0, 0, 12, 0)
					else:
						pygame.draw.rect(self.display_surface, bg_color, item_rect)

					# Draw 4 icons in 2x2 grid with no gaps at 25% size
					for i, monster in enumerate(entry['monsters']):
						# Try to get icon, create placeholder if missing
						if monster.name in self.icon_frames:
							icon_surf = self.icon_frames[monster.name]
							# Scale to 25% of original size (15% of item height)
							max_icon_size = self.item_height * 0.15
							icon_scale = min(max_icon_size / icon_surf.get_width(), max_icon_size / icon_surf.get_height())
							new_size = (int(icon_surf.get_width() * icon_scale), int(icon_surf.get_height() * icon_scale))
							icon_surf = pygame.transform.scale(icon_surf, new_size)
						else:
							# Create placeholder icon at 25% size
							icon_size = int(self.item_height * 0.1)
							icon_surf = pygame.Surface((icon_size, icon_size))
							icon_surf.fill(COLORS['light-gray'])
							pygame.draw.rect(icon_surf, COLORS['white'], icon_surf.get_rect(), 1)

						# Position in 2x2 grid with no gaps
						row = i // 2
						col = i % 2
						icon_width = icon_surf.get_width()
						icon_height = icon_surf.get_height()
						grid_width = icon_width * 2
						grid_height = icon_height * 2

						# Center the grid in the icon area
						grid_start_x = item_rect.left + (90 - grid_width) / 2
						grid_start_y = item_rect.centery - grid_height / 2

						icon_x = grid_start_x + col * icon_width
						icon_y = grid_start_y + row * icon_height

						self.display_surface.blit(icon_surf, (icon_x, icon_y))

					# Draw text with wrapping
					max_text_width = self.list_width - 100  # Leave space for icons
					words = entry['name'].split(' ')
					lines = []
					current_line = []

					for word in words:
						test_line = ' '.join(current_line + [word])
						test_surf = self.fonts['regular'].render(test_line, False, text_color)
						if test_surf.get_width() <= max_text_width:
							current_line.append(word)
						else:
							if current_line:
								lines.append(' '.join(current_line))
							current_line = [word]
					if current_line:
						lines.append(' '.join(current_line))

					# Draw wrapped lines
					line_height = 18
					start_y = item_rect.midleft[1] - (len(lines) * line_height) / 2
					for i, line in enumerate(lines[:2]):  # Max 2 lines
						text_surf = self.fonts['regular'].render(line, False, text_color)
						text_rect = text_surf.get_frect(midleft = (item_rect.midleft[0] + 90, start_y + i * line_height))
						self.display_surface.blit(text_surf, text_rect)
			else:
				# Draw single entry
				monster = entry['monster']

				# Try to get icon, create placeholder if missing
				if monster.name in self.icon_frames:
					icon_surf = self.icon_frames[monster.name]
					max_icon_size = self.item_height * 0.8
					icon_scale = min(max_icon_size / icon_surf.get_width(), max_icon_size / icon_surf.get_height())
					if icon_scale < 1:
						new_size = (int(icon_surf.get_width() * icon_scale), int(icon_surf.get_height() * icon_scale))
						icon_surf = pygame.transform.scale(icon_surf, new_size)
				else:
					# Create placeholder icon for monsters without graphics
					icon_size = int(self.item_height * 0.6)
					icon_surf = pygame.Surface((icon_size, icon_size))
					icon_surf.fill(COLORS['light-gray'])
					pygame.draw.rect(icon_surf, COLORS['white'], icon_surf.get_rect(), 2)

				icon_rect = icon_surf.get_frect(center = item_rect.midleft + vector(45, 0))

				if item_rect.colliderect(self.main_rect):
					if item_rect.collidepoint(self.main_rect.topleft):
						pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 12)
					elif item_rect.collidepoint(self.main_rect.bottomleft + vector(1, -1)):
						pygame.draw.rect(self.display_surface, bg_color, item_rect, 0, 0, 0, 0, 12, 0)
					else:
						pygame.draw.rect(self.display_surface, bg_color, item_rect)

					# Draw text with wrapping
					max_text_width = self.list_width - 100  # Leave space for icon
					words = monster.name.split(' ')
					lines = []
					current_line = []

					for word in words:
						test_line = ' '.join(current_line + [word])
						test_surf = self.fonts['regular'].render(test_line, False, text_color)
						if test_surf.get_width() <= max_text_width:
							current_line.append(word)
						else:
							if current_line:
								lines.append(' '.join(current_line))
							current_line = [word]
					if current_line:
						lines.append(' '.join(current_line))

					# Draw wrapped lines
					line_height = 18
					start_y = item_rect.midleft[1] - (len(lines) * line_height) / 2
					for i, line in enumerate(lines[:2]):  # Max 2 lines
						text_surf = self.fonts['regular'].render(line, False, text_color)
						text_rect = text_surf.get_frect(midleft = (item_rect.midleft[0] + 90, start_y + i * line_height))
						self.display_surface.blit(text_surf, text_rect)

					self.display_surface.blit(icon_surf, icon_rect)
		
		# lines between monsters on menu
		for i in range(1, min(self.visible_items, len(self.display_monsters))):
			y = self.main_rect.top + self.item_height * i
			left = self.main_rect.left
			right = self.main_rect.left + self.list_width
			pygame.draw.line(self.display_surface, COLORS['light-gray'], (left, y), (right, y))

		# shadow on menu
		shadow_surf = pygame.Surface((4, self.main_rect.height))
		shadow_surf.set_alpha(100)
		self.display_surface.blit(shadow_surf,(self.main_rect.left + self.list_width - 4, self.main_rect.top))
	
	def display_main(self, dt):
		"""Display environmental and compliance data"""
		# Regenerate display list
		self.display_monsters = self._create_display_list()
		
		# Get current entry
		entry = self.display_monsters[self.index]

		# main bg
		rect = pygame.FRect(self.main_rect.left + self.list_width,self.main_rect.top, self.main_rect.width - self.list_width, self.main_rect.height)
		pygame.draw.rect(self.display_surface, COLORS['dark'], rect, 0, 12,0, 12,0)

		# Calculate all indicators and compliance
		try:
			indicators = calculate_city_scale_indicators(self.monsters)
			compliance = check_compliance_thresholds(self.monsters)
			drug_code = get_drug_code_from_choices(self.monsters)
			
			# Title section with icon display
			title_height = rect.height * 0.15
			title_rect = pygame.FRect(rect.left, rect.top, rect.width, title_height)
			pygame.draw.rect(self.display_surface, COLORS['light-gray'], title_rect, 0, 0, 0, 12)
			
			# Get description for current item and prepare display
			if entry['type'] == 'combined':
				description_data = get_drug_description(drug_code)
				title_text = f"{description_data['name']}"
				description_text = description_data.get('description', '')
			else:
				monster = entry['monster']
				description_data = get_item_description(monster.name)
				title_text = description_data['name']
				description_text = description_data.get('description', '')
			
			# Display title
			title_surf = self.fonts['bold'].render(title_text, False, COLORS['white'])
			title_text_rect = title_surf.get_frect(topleft=(title_rect.left + 10, title_rect.top + 5))
			self.display_surface.blit(title_surf, title_text_rect)
			
			# Word wrap and display description text below title
			if description_text:
				words = description_text.split(' ')
				lines_list = []
				current_line = []
				max_width = title_rect.width - 300  # Leave room for icons
				
				for word in words:
					test_line = ' '.join(current_line + [word])
					test_surf = self.fonts['small'].render(test_line, False, COLORS['white'])
					if test_surf.get_width() <= max_width:
						current_line.append(word)
					else:
						if current_line:
							lines_list.append(' '.join(current_line))
						current_line = [word]
				if current_line:
					lines_list.append(' '.join(current_line))
				
				# Display description lines below title
				line_y = title_text_rect.bottom + 5
				for line in lines_list[:3]:  # Max 3 lines
					line_surf = self.fonts['small'].render(line, False, COLORS['light'])
					line_rect = line_surf.get_frect(topleft=(title_rect.left + 10, line_y))
					self.display_surface.blit(line_surf, line_rect)
					line_y += 15
			
			# Display icon/animation for currently selected entry
			if entry['type'] == 'combined':
				# Show all 4 molecule icons side by side
				self.frame_index += INDEX_ANIMATION_SPEED * dt
				scaled_frames = []
				for monster in entry['monsters']:
					if monster.name in self.monster_frames:
						frames = self.monster_frames[monster.name]['idle']
						current_frame = frames[int(self.frame_index) % len(frames)]
						# Scale down to fit
						max_size = title_height * 0.7
						scale = min(max_size / current_frame.get_width(), max_size / current_frame.get_height())
						if scale < 1:
							new_size = (int(current_frame.get_width() * scale), int(current_frame.get_height() * scale))
							current_frame = pygame.transform.scale(current_frame, new_size)
						scaled_frames.append(current_frame)
				
				if scaled_frames:
					total_width = sum(f.get_width() for f in scaled_frames)
					start_x = title_rect.right - total_width - 20
					current_x = start_x
					for frame in scaled_frames:
						frame_rect = frame.get_frect(midleft=(current_x, title_rect.centery))
						self.display_surface.blit(frame, frame_rect)
						current_x += frame.get_width()
			else:
				# Show single monster animation
				if monster.name in self.monster_frames:
					self.frame_index += INDEX_ANIMATION_SPEED * dt
					frames = self.monster_frames[monster.name]['idle']
					current_frame = frames[int(self.frame_index) % len(frames)]
					# Scale to fit in title area
					max_size = title_height * 0.8
					scale = min(max_size / current_frame.get_width(), max_size / current_frame.get_height())
					if scale < 1:
						new_size = (int(current_frame.get_width() * scale), int(current_frame.get_height() * scale))
						current_frame = pygame.transform.scale(current_frame, new_size)
					frame_rect = current_frame.get_frect(midright=(title_rect.right - 20, title_rect.centery))
					self.display_surface.blit(current_frame, frame_rect)

			# Drug code and patient info below title
			info_y = title_rect.bottom + 5
			
			# Drug code info
			code_surf = self.fonts['small'].render(f'Drug Code: {drug_code}', False, COLORS['gold'])
			code_rect = code_surf.get_frect(topleft=(rect.left + 10, info_y))
			self.display_surface.blit(code_surf, code_rect)
			
			# Patients info
			patient_surf = self.fonts['small'].render(f'Patients: {indicators["num_patients"]}  |  Doses/g: {indicators["doses_per_gram"]}', False, COLORS['white'])
			patient_rect = patient_surf.get_frect(topright=(rect.right - 10, info_y))
			self.display_surface.blit(patient_surf, patient_rect)
			
			# Process Conditions section
			process_y = info_y + 30
			process_height = 60
			process_rect = pygame.FRect(rect.left + 20, process_y, rect.width - 40, process_height)
			pygame.draw.rect(self.display_surface, COLORS['light-gray'], process_rect, 0, 5)
			
			# Get reaction parameters and conversion
			from calculations import get_reaction_parameters, get_conversion_from_player_choices
			temperature, duration = get_reaction_parameters(self.monsters)
			conversion = get_conversion_from_player_choices(self.monsters)
			
			# Process conditions title
			process_title = self.fonts['bold'].render('Process Conditions', False, COLORS['white'])
			process_title_rect = process_title.get_frect(midtop=(process_rect.centerx, process_rect.top + 5))
			self.display_surface.blit(process_title, process_title_rect)
			
			# Display the three parameters in a row
			param_y = process_title_rect.bottom + 5
			param_spacing = process_rect.width / 3
			
			# Temperature
			temp_text = f'Temp: {temperature}°C'
			temp_surf = self.fonts['regular'].render(temp_text, False, COLORS['fire'])
			temp_rect = temp_surf.get_frect(center=(process_rect.left + param_spacing * 0.5, param_y + 10))
			self.display_surface.blit(temp_surf, temp_rect)
			
			# Duration
			duration_text = f'Time: {duration}h'
			duration_surf = self.fonts['regular'].render(duration_text, False, COLORS['water'])
			duration_rect = duration_surf.get_frect(center=(process_rect.left + param_spacing * 1.5, param_y + 10))
			self.display_surface.blit(duration_surf, duration_rect)
			
			# Conversion
			conversion_text = f'Conversion: {conversion}%'
			conversion_surf = self.fonts['regular'].render(conversion_text, False, COLORS['gold'])
			conversion_rect = conversion_surf.get_frect(center=(process_rect.left + param_spacing * 2.5, param_y + 10))
			self.display_surface.blit(conversion_surf, conversion_rect)
			
			# Main content area - adjusted to start below process conditions
			content_rect = pygame.FRect(rect.left + 20, process_rect.bottom + 10, rect.width - 40, rect.height - title_height - process_height - 90)
			
			# Compliance status at top
			status_y = content_rect.top
			status_text = "COMPLIANT" if compliance['overall_compliant'] else "NON-COMPLIANT"
			status_color = COLORS['plant'] if compliance['overall_compliant'] else COLORS['red']
			status_surf = self.fonts['bold'].render(status_text, False, status_color)
			status_rect = status_surf.get_frect(centerx=content_rect.centerx, top=status_y)
			self.display_surface.blit(status_surf, status_rect)
			
			bar_start_y = status_rect.bottom + 15
			# Define bars to display
			bar_height = 30
			bar_spacing = 45
			bar_width = (content_rect.width - 20) * 0.6  # 60% of original width
			
			bars_data = [
				{
					'label': 'Worker Safety',
					'value': compliance['worker_safety']['exposure'],
					'max_value': self.max_values['worker_exposure'],
					'threshold': compliance['worker_safety']['threshold'],
					'color': COLORS['red'] if compliance['worker_safety']['exposure'] > 1 else COLORS['plant'],
					'status': f"{(compliance['worker_safety']['exposure'] / compliance['worker_safety']['threshold'] * 100):.0f}% exposure limit",
					'invert': False  # Lower is better
				},
				{
					'label': 'Daily Cost',
					'value': indicators['city_cost'],
					'max_value': self.max_values['city_cost'],
					'threshold': compliance['price']['price_cap'],
					'color': COLORS['gold'],
					'status': f"${indicators['city_cost']:.1f}/day (Cap: ${compliance['price']['price_cap']})",
					'invert': False
				},
				{
					'label': 'CO2 Impact',
					'value': indicators['city_impact'],
					'max_value': self.max_values['city_impact'],
					'threshold': compliance['co2_impact']['target'] if compliance['co2_impact']['required'] else None,
					'color': COLORS['fire'],
					'status': f"{indicators['city_impact']:.1f} gCO2/day",
					'invert': False
				},
				{
					'label': 'Waste Generation',
					'value': indicators['city_waste'],
					'max_value': self.max_values['city_waste'],
					'threshold': None,
					'color': COLORS['light-gray'],
					'status': f"{indicators['city_waste']:.1f} g/day",
					'invert': False
				},
				{
					'label': 'Biodegradation (API)',
					'value': molecule_stats[drug_code]['biodegAPI'] * 100 if drug_code in molecule_stats else 0,
					'max_value': 100,
					'threshold': compliance['biodegradation']['threshold'] * 100 if compliance['biodegradation']['required'] else None,
					'color': COLORS['plant'],
					'status': f"{molecule_stats[drug_code]['biodegAPI']*100:.0f}%",
					'invert': True
				},
				{
					'label': 'Water Pollution',
					'value': compliance['pollution']['total_pollution'],
					'max_value': self.max_values['city_pollution'],
					'threshold': compliance['pollution']['limit'] if compliance['pollution']['limit'] < 1000 else None,
					'color': COLORS['water'],
					'status': f"{compliance['pollution']['total_pollution']:.3f} mg/litre",
					'invert': False
				},
				{
					'label': 'Ecotoxicity',
					'value': indicators['city_ecotoxicity'],
					'max_value': self.max_values['city_ecotoxicity'],
					'threshold': self.mean_ecotoxicity,
					'color': COLORS['red'],
					'status': f"{indicators['city_ecotoxicity']:.4f}",
					'invert': False
				}
			]
			
			# Draw bars
			current_y = bar_start_y
			for bar_info in bars_data:
				# Label
				label_surf = self.fonts['regular'].render(bar_info['label'], False, COLORS['white'])
				label_rect = label_surf.get_frect(topleft=(content_rect.left + 10, current_y))
				self.display_surface.blit(label_surf, label_rect)
				
				# Bar
				bar_rect = pygame.FRect(content_rect.left + 10, label_rect.bottom + 3, bar_width, bar_height - 15)
				
				# Draw bar with appropriate color
				display_value = bar_info['value']
				
				draw_bar(
					self.display_surface,
					bar_rect,
					display_value,
					bar_info['max_value'],
					bar_info['color'],
					COLORS['black'],
					2
				)
				
				# Status text on right, aligned with bar center
				status_surf = self.fonts['small'].render(bar_info['status'], False, COLORS['light'])
				status_rect = status_surf.get_frect(topright=(content_rect.right - 10, bar_rect.centery - status_surf.get_height() / 2))
				self.display_surface.blit(status_surf, status_rect)
				
				# Draw threshold line and status text
				if bar_info['threshold'] is not None:
					threshold_x = content_rect.left + 10 + (bar_info['threshold'] / bar_info['max_value']) * bar_width
					
					threshold_x = max(content_rect.left + 10, min(threshold_x, content_rect.left + 10 + bar_width))
					pygame.draw.line(
						self.display_surface,
						COLORS['white'],
						(threshold_x, bar_rect.top - 2),
						(threshold_x, bar_rect.bottom + 2),
						2
					)
					
					# Determine threshold status and add text to the right of bar
					# For inverted bars (like biodegradation), higher values are better
					if bar_info['invert']:
						# Higher is better (e.g., biodegradation)
						if bar_info['value'] >= bar_info['threshold']:
							threshold_text = "Above threshold"
							threshold_color = COLORS['plant']
						else:
							threshold_text = "Below threshold"
							threshold_color = COLORS['red']
					else:
						# Lower is better (e.g., pollution, ecotoxicity)
						if bar_info['value'] <= bar_info['threshold']:
							threshold_text = "Below threshold"
							threshold_color = COLORS['plant']
						else:
							threshold_text = "Above threshold"
							threshold_color = COLORS['red']
					
					threshold_surf = self.fonts['small'].render(threshold_text, False, threshold_color)
					threshold_rect = threshold_surf.get_frect(midleft=(bar_rect.right + 10, bar_rect.centery))
					self.display_surface.blit(threshold_surf, threshold_rect)
				else:
					# No threshold applied
					no_threshold_text = "No threshold"
					no_threshold_surf = self.fonts['small'].render(no_threshold_text, False, COLORS['light-gray'])
					no_threshold_rect = no_threshold_surf.get_frect(midleft=(bar_rect.right + 10, bar_rect.centery))
					self.display_surface.blit(no_threshold_surf, no_threshold_rect)
				
				current_y += bar_spacing
			
			# Compliance messages at bottom
			bottom_y = content_rect.bottom - 60
			message_lines = []
			
			# Check Worker Safety threshold
			if compliance['worker_safety']['exposure'] > compliance['worker_safety']['threshold']:
				message_lines.append(('Safety measures insufficient. Chemical exposure exceeds legal limit.', COLORS['red']))
			
			# Check Daily Cost threshold
			if indicators['city_cost'] > compliance['price']['price_cap']:
				message_lines.append(('Medicine is too expensive.', COLORS['red']))
			
			# Check CO2 Impact threshold
			if compliance['co2_impact']['required']:
				if indicators['city_impact'] > compliance['co2_impact']['target']:
					message_lines.append(('Global warming potential is unsustainable.', COLORS['red']))
			else:
				message_lines.append(('CO2 emissions are not monitored.', COLORS['light-gray']))
			
			# Check Biodegradation threshold
			if compliance['biodegradation']['required']:
				if not compliance['biodegradation']['has_certification']:
					# Policy exists but no certification system
					message_lines.append(('There is a legal biodegradability requirement but no certification scheme to prove it.', COLORS['red']))
				else:
					# Both policy and certification exist - check if molecule passes
					biodeg_value = molecule_stats[drug_code]['biodegAPI'] if drug_code in molecule_stats else 0
					if biodeg_value < compliance['biodegradation']['threshold']:
						message_lines.append(('The active pharmaceutical ingredient fails biodegradation tests.', COLORS['red']))
			else:
				message_lines.append(('Biodegradability is not a requirement.', COLORS['light-gray']))
			
			# Check Water Pollution threshold
			if compliance['pollution']['limit'] < 1000:  # Threshold exists
				if compliance['pollution']['total_pollution'] > compliance['pollution']['limit']:
					message_lines.append(('Pollution levels are dangerously high.', COLORS['red']))
			else:
				message_lines.append(('Water pollution is not being measured.', COLORS['light-gray']))
			
			# Check Ecotoxicity threshold
			biodeg_value = molecule_stats[drug_code]['biodegAPI'] if drug_code in molecule_stats else 0
			if indicators['city_ecotoxicity'] > self.mean_ecotoxicity:
				message_lines.append(('Ecotoxicity is above average.', COLORS['red']))
				
				# Check for long-term environmental damage warning
				if biodeg_value < 0.5 and indicators['city_ecotoxicity'] > self.mean_ecotoxicity:
					message_lines.append(('May cause long term environmental damage.', COLORS['red']))
			else:
				pass
			
			# Display messages with scrolling (max 5 visible)
			max_visible_messages = 5
			total_messages = len(message_lines)

			if total_messages > 0:
				# Loop the scroll offset
				scroll_offset = self.message_scroll_offset % total_messages

				# Display up to 5 messages starting from scroll offset
				for i in range(max_visible_messages):
					if i < total_messages:
						# Get message index with wrapping
						message_index = (scroll_offset + i) % total_messages
						message, color = message_lines[message_index]

						message_surf = self.fonts['small'].render(message, False, color)
						message_rect = message_surf.get_frect(centerx=content_rect.centerx, top=bottom_y + i * 20)
						self.display_surface.blit(message_surf, message_rect)
			
		except Exception as e:
			# If calculations fail, show error
			error_surf = self.fonts['regular'].render(f'Error calculating data: {str(e)}', False, COLORS['red'])
			error_rect = error_surf.get_frect(center=rect.center)
			self.display_surface.blit(error_surf, error_rect)

	def update(self, dt):
		self.input()

		# Update message scrolling timer
		self.message_scroll_timer += dt
		if self.message_scroll_timer >= self.message_scroll_speed:
			self.message_scroll_timer = 0
			self.message_scroll_offset += 1

		self.display_surface.blit(self.tint_surf, (0,0))
		self.display_list()
		self.display_main(dt)