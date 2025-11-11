from settings import * 
from support import check_connections
from timer import Timer
from random import choice
from monster import Monster

class Entity(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, facing_direction):
		super().__init__(groups)
		self.z = WORLD_LAYERS['main']

		#graphics
		self.frame_index, self.frames = 0, frames
		self.facing_direction = facing_direction

		#movement
		self.direction = vector()
		self.speed = 80 #animation is of a slow walk - other sprites with 4 frames can go 250!
		self.blocked = False

		#sprite setup
		self.image = self.frames[self.get_state()][self.frame_index]
		self.rect = self.image.get_frect(center = pos)
		# Sprite is 64x64 but has 14px empty top, 14px empty left/right
		# Hitbox covers the actual visible character image with adjustments
		self.hitbox = self.rect.inflate(-28, -38)  # Remove 14px from each side width, 19px from height
		self.hitbox.top = self.rect.top + 30  # Position hitbox lower on character

		self.y_sort = self.rect.centery

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[self.get_state()][int(self.frame_index % len(self.frames[self.get_state()]))]	

	def get_state(self):
		moving = bool(self.direction)
		# Only update facing direction from movement if not in dialog
		if moving and not getattr(self, 'in_dialog', False):
			if self.direction.x != 0:
				self.facing_direction = 'right' if self.direction.x > 0 else 'left'
			if self.direction.y != 0:
				self.facing_direction = 'down' if self.direction.y > 0 else 'up'
		return f'{self.facing_direction}{"" if moving else "_idle"}'

	def change_facing_direction(self, target_pos):
		relation = vector(target_pos) - vector(self.rect.center)
		if abs(relation.y) < 15: #small sprites so low tolerance here
			self.facing_direction = 'right' if relation.x > 0 else 'left'
		else:
			self.facing_direction = 'down' if relation.y > 0 else 'up'

	def block(self):
		self.blocked = True
		self.direction = vector(0,0)

	def unblock(self):
		self.blocked = False

class Character(Entity):
	def __init__(self, pos, frames, groups, facing_direction, character_data, player, create_dialog, collision_sprites, radius, chattycharacter, game=None):
		super().__init__(pos, frames, groups, facing_direction)
		self.character_data = character_data
		self.player = player
		self.create_dialog = create_dialog
		self.collision_rects = [sprite.rect for sprite in collision_sprites if sprite is not self]
		self.chattycharacter = chattycharacter
		self.game = game  # Store reference to game object for accessing player_monsters

		# movement
		self.speed = 48  # 60% of player speed (80 * 0.6 = 48)
		self.has_moved = False
		self.can_rotate = True
		self.has_noticed = False
		self.radius = int(radius)
		self.view_directions = character_data['directions']

		# patrol movement
		self.patrol = character_data.get('patrol', False)
		self.patrol_distance = character_data.get('patrol_distance', 600)
		self.start_pos = vector(pos)
		self.patrol_direction = 1 if 'right' in self.view_directions else -1
		self.in_dialog = False
		self.facing_before_dialog = None
		self.returning_to_start = False

		self.timers = {
			'look around': Timer(duration=2000, repeat=True, autostart=True, func=self.random_view_direction, randomize=True),
			'notice': Timer(300, func = self.start_move)
		}

	def random_view_direction(self):
		if self.can_rotate:
			self.facing_direction = choice(self.view_directions)

	def start_dialog(self):
		"""Called when dialog begins - save current facing direction"""
		self.facing_before_dialog = self.facing_direction
		self.in_dialog = True
		self.direction = vector(0, 0)  # Stop moving immediately

	def end_dialog_movement(self):
		"""Called when dialog ends - start returning to start position"""
		self.in_dialog = False
		self.returning_to_start = True
		self.can_rotate = False

	def patrol_move(self, dt):
		"""Handle patrol movement back and forth"""
		if self.patrol and not self.in_dialog:
			# Calculate distance from start position
			distance_from_start = self.rect.centerx - self.start_pos.x

			# Check if we've reached patrol boundary
			if abs(distance_from_start) >= self.patrol_distance:
				self.patrol_direction *= -1

			# Set movement direction (left/right patrol)
			self.direction.x = self.patrol_direction
			self.direction.y = 0

			# Move the character
			self.rect.center += self.direction * self.speed * dt
			self.hitbox.center = self.rect.center

	def get_dialog(self):
		"""Return dialogue branch based on visit state and compliance status."""
		# Check if the game is complete (COMPLIANT status achieved)
		from calculations import check_compliance_thresholds

		# Check for endgame status first
		if self.character_data.get("endgame", False):
			# Mission complete - show endgame dialog
			return self.character_data["dialog"]["endgame"]

		# Check if this is a sage character with dynamic dialog
		character_id = None
		if self.game:
			# Find this character's ID by checking NPC_DATA
			from game_data import NPC_DATA
			for char_id, char_data in NPC_DATA.items():
				if char_data is self.character_data:
					character_id = char_id
					break

		# Generate dynamic dialog for sages
		if character_id == 'safesage' and self.game:
			return self.get_safesage_dialog()
		if character_id == 'envirosage' and self.game:
			return self.get_envirosage_dialog()
		if character_id == 'chemsage' and self.game:
			return self.get_chemsage_dialog()

		# Normal dialog flow based on visit state
		if not self.character_data.get("visited", False):
			# First meeting - show default dialog
			return self.character_data["dialog"]["default"]
		elif self.character_data.get("visited", False) and not self.character_data.get("return", False):
			# After first visit - show return dialog
			return self.character_data["dialog"]["return"]
		else:
			# Subsequent visits - show return dialog
			return self.character_data["dialog"]["return"]

	def get_safesage_dialog(self):
		"""Generate dynamic dialog for safesage based on exposure and conversion values."""
		from calculations import calculate_conversion, get_drug_code_from_choices

		# Start with introduction if this is first visit
		dialog_lines = []
		if not self.character_data.get("visited", False):
			dialog_lines.append("Hello! I am the safety officer, but I am interested in chemical engineering too!")

		# Get molecule code (e.g., 'CABD')
		molecule_code = get_drug_code_from_choices(self.game.player_monsters)

		# Get safety choice (index 4: Standard PPE, PPE and extra ventilation, No PPE, Closed reactor system)
		safety_monster = self.game.player_monsters.get(4)
		safety_choice = safety_monster.name if safety_monster else 'Standard PPE'

		# Get molecule stats
		from calculations import molecule_stats
		mol_stats = molecule_stats.get(molecule_code, {})

		# Determine which exposure value to use based on safety choice
		exposure_value = None
		if 'No PPE' in safety_choice:
			exposure_value = mol_stats.get('exposureNo', 0)
		elif 'PPE and extra ventilation' in safety_choice:
			exposure_value = mol_stats.get('exposureVent', 0)
		elif 'Closed reactor system' in safety_choice:
			exposure_value = mol_stats.get('exposureClosed', 0)
		else:  # Standard PPE
			exposure_value = mol_stats.get('exposureBasic', 0)

		# Generate first dialog line about exposure
		if exposure_value is not None:
			if exposure_value <= 1:
				exposure_dialog = "The exposure to this molecule is acceptable given the safety measure implemented and its inherent human toxicity hazards."
			else:
				percentage = int(exposure_value * 100)
				exposure_dialog = f"Our current operating practices mean the exposure to this molecule is {percentage}% over legal limits for workers."
		else:
			exposure_dialog = "I need more information about the molecule to assess worker exposure."

		dialog_lines.append(exposure_dialog)

		# Get conversion percentage
		rate_const = mol_stats.get('rateConst', 0.0001)
		temperature_monster = self.game.player_monsters.get(12)  # reaction_temperature
		rxn_time_monster = self.game.player_monsters.get(13)  # reaction_hours

		temperature = temperature_monster.level if temperature_monster else 75
		rxn_time = rxn_time_monster.level if rxn_time_monster else 6

		conversion = calculate_conversion(rate_const, temperature, rxn_time)

		# Generate second dialog line about conversion
		if conversion <= 70:
			conversion_dialog = f"The reaction to make this molecule is incomplete at {conversion}%. Higher temperatures or longer reactions will help, otherwise you could think about more reactive molecules."
		elif conversion >= 95:
			conversion_dialog = f"The reaction is virtually complete at {conversion}%. We could reduce the temperature or reaction time to save energy."
		else:
			conversion_dialog = f"The reaction is quite productive at {conversion}%."

		dialog_lines.append(conversion_dialog)

		return dialog_lines

	def get_envirosage_dialog(self):
		"""Generate dynamic dialog for envirosage based on water pollution and ecotoxicity values."""
		from calculations import calculate_city_scale_indicators, pollution_limit_basic, pollution_limit_harsh, pollution_limit_none, penalty_basic

		# Start with introduction if this is first visit
		dialog_lines = []
		if not self.character_data.get("visited", False):
			dialog_lines.append("Welcome, I am the head of ecological stewardship here.")

		# Calculate city-scale indicators
		indicators = calculate_city_scale_indicators(self.game.player_monsters)
		total_pollution = indicators['city_api_emissions'] + indicators['city_meta_emissions']
		city_ecotoxicity = indicators['city_ecotoxicity']

		# Determine pollution policy (slot 10)
		pollution_policy = 'No water quality standards'
		if 10 in self.game.player_monsters:
			pollution_policy = self.game.player_monsters[10].name

		# Set pollution limit based on policy
		if pollution_policy == 'Lenient water quality standards':
			pollution_limit = pollution_limit_basic  # 4
			limit_name = "lenient"
		elif pollution_policy == 'Strict water quality standards':
			pollution_limit = pollution_limit_harsh  # 2
			limit_name = "strict"
		else:
			pollution_limit = pollution_limit_none  # 1000000 (effectively no limit)
			limit_name = "none"

		# Check if fine is applicable
		fine_applicable = total_pollution > pollution_limit and pollution_limit < pollution_limit_none
		regulatory_fines = penalty_basic if fine_applicable else 0

		# Dialog about water pollution and regulations
		if limit_name == "none":
			pollution_dialog = f"Currently, there are no water quality standards in place. The total water pollution is {total_pollution:.2f} mg/litre, but there is no regulatory limit to enforce."
		else:
			pollution_dialog = f"The current water quality standard is {limit_name}, with a limit of {pollution_limit} mg/litre. Total pollution is {total_pollution:.2f} mg/litre."
			if fine_applicable:
				pollution_dialog += f" This exceeds the limit, resulting in a regulatory fine of ${regulatory_fines}/day."
			else:
				pollution_dialog += f" This is within acceptable limits, so no fines are being applied."

		dialog_lines.append(pollution_dialog)

		# Explain the source and nature of pollution
		explanation = "Both pharmaceuticals and their metabolites enter the environment via wastewater. When excreted by patients, these chemicals undergo transformation by water and microbes in the environment. The degradation products of these chemicals may themselves be toxic to aquatic life."
		dialog_lines.append(explanation)

		# Calculate mean ecotoxicity threshold for comparison
		mean_ecotoxicity = 1.56  # Calculated as average across all 81 molecule combinations

		# Dialog about ecotoxicity
		if city_ecotoxicity < mean_ecotoxicity:
			ecotox_dialog = f"The ecotoxicity is currently {city_ecotoxicity:.3f}, which is relatively low. This suggests the molecule and its metabolites pose minimal threat to aquatic ecosystems."
		elif city_ecotoxicity < 2 * mean_ecotoxicity:
			ecotox_dialog = f"The ecotoxicity is {city_ecotoxicity:.2f}. This is moderate. There is some environmental impact, but it could be improved with better molecular design or more thorough water treatment."
		else:
			ecotox_dialog = f"The ecotoxicity is {city_ecotoxicity:.2f}, which is concerning. The pharmaceutical and its metabolites are causing significant harm to aquatic life. Consider redesigning the molecule or implementing advanced water treatment."

		dialog_lines.append(ecotox_dialog)

		return dialog_lines

	def get_chemsage_dialog(self):
		"""Generate dynamic dialog for chemsage based on molecule attributes."""
		from calculations import get_drug_code_from_choices, molecule_stats

		# Start with introduction if this is first visit
		dialog_lines = []
		if not self.character_data.get("visited", False):
			dialog_lines.append("Greetings! Yes I would love to talk about our current project some more!")

		# Get molecule code and stats
		molecule_code = get_drug_code_from_choices(self.game.player_monsters)
		mol_stats = molecule_stats.get(molecule_code, {})

		if not mol_stats:
			dialog_lines.append("I need more information about your molecule to provide guidance.")
			return dialog_lines

		# Get molecule attributes
		waste = mol_stats.get('waste', 0)
		impact = mol_stats.get('impact', 0)  # CO2 emissions in gCO2/g
		cost = mol_stats.get('cost', 0)
		efficacy = mol_stats.get('efficacy', 0)

		# Percentile thresholds (calculated from all 81 molecules)
		# Lower is better for waste, impact, and cost
		# Higher is better for efficacy
		waste_p30, waste_p70 = 5.25, 6.90
		impact_p30, impact_p70 = 83.0, 116.0
		cost_p30, cost_p70 = 2.58, 3.08
		efficacy_p30, efficacy_p70 = 2.57, 3.00

		# Analyze waste (lower is better)
		if waste <= waste_p30:
			waste_assessment = f"The synthesis produces {waste:.2f} g of waste per g of product, which is below average. This is an efficient process with minimal waste."
		elif waste >= waste_p70:
			waste_assessment = f"The synthesis produces {waste:.2f} g of waste per g of product, which is above average. Different reactants woudl be preferable."
		else:
			waste_assessment = f"The synthesis produces {waste:.2f} g of waste per g of product, which is about average for the sort of pharmaceuticals we manufacture."

		dialog_lines.append(waste_assessment)

		# Analyze impact/CO2 (lower is better)
		if impact <= impact_p30:
			impact_assessment = f"The carbon footprint is {impact:.0f} gCO2 per g of product, which is below average. This is a relatively low-impact synthesis."
		elif impact >= impact_p70:
			impact_assessment = f"The carbon footprint is {impact:.0f} gCO2 per g of product, which is above average. Producing the precusor chemicals is quite energy-intensive."
		else:
			impact_assessment = f"The carbon footprint is {impact:.0f} gCO2 per g of product, which is about average for this class of chemicals."

		dialog_lines.append(impact_assessment)

		# Analyze cost (lower is better)
		if cost <= cost_p30:
			cost_assessment = f"The reagent cost is ${cost:.2f} per g, which is below average. This is an economical synthesis which will please the funding agency."
		elif cost >= cost_p70:
			cost_assessment = f"The reagent cost is ${cost:.2f} per g, which is above average. The reagents are relatively expensive and I would prefer the students do not waste any."
		else:
			cost_assessment = f"The reagent cost is ${cost:.2f} per g, which is about average."

		dialog_lines.append(cost_assessment)

		# Analyze efficacy (higher is better)
		if efficacy >= efficacy_p70:
			efficacy_assessment = f"The efficacy is {efficacy:.2f} doses per gram, which is above average. This molecule is highly effective as a medicine, meaning less material is needed per dose."
		elif efficacy <= efficacy_p30:
			efficacy_assessment = f"The efficacy is {efficacy:.2f} doses per gram, which is below average. Patients will require bigger doses, increasing the environmental impact."
		else:
			efficacy_assessment = f"The efficacy is {efficacy:.2f} doses per gram, which meets our target."

		dialog_lines.append(efficacy_assessment)

		return dialog_lines

	def raycast(self):
		# Only raycast if not visited yet (prevents notice icon on subsequent interactions)
		# Special case: boss should only approach during endgame
		from game_data import NPC_DATA
		is_boss = False
		for char_id, char_data in NPC_DATA.items():
			if char_data is self.character_data and char_id == 'boss':
				is_boss = True
				break

		# Boss only approaches if endgame is triggered
		if is_boss and not self.character_data.get('endgame', False):
			return

		if not self.character_data.get('visited', False):
			if check_connections(self.radius, self, self.player) and self.has_los() and not self.has_moved and not self.has_noticed:
				self.player.block()
				self.player.change_facing_direction(self.rect.center)
				self.timers['notice'].activate()
				self.can_rotate = False
				self.has_noticed = True
				self.player.noticed = True

	def has_los(self): # line of sight between player and NPC
		if vector(self.rect.center).distance_to(self.player.rect.center) < self.radius:
			collisions = [bool(rect.clipline(self.rect.center, self.player.rect.center)) for rect in self.collision_rects]
			return not any(collisions) # considers collision objects between characters that break line of sight

	def start_move(self): #NCP moves towards player
		relation = (vector(self.player.rect.center) - vector(self.rect.center)).normalize()
		# Don't round the direction - use the full normalized vector for smooth diagonal movement
		self.direction = relation

	def return_to_start(self, dt):
		"""Move character back to start position and face down when reached"""
		if self.returning_to_start:
			# Calculate direction to start position
			relation = vector(self.start_pos) - vector(self.rect.center)
			distance = relation.length()

			# If close enough to start position, stop and face down
			if distance < 5:
				self.rect.center = self.start_pos
				self.hitbox.center = self.rect.center
				self.direction = vector(0, 0)
				self.facing_direction = 'down'
				self.returning_to_start = False
				self.has_moved = False
				self.has_noticed = False
				self.can_rotate = True
			else:
				# Move toward start position
				self.direction = relation.normalize()
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center

	def move(self, dt): # moving NPC
		if not self.has_moved and self.direction:
			# Special case: boss with limited approach distance
			if hasattr(self, 'approaching') and self.approaching:
				distance_traveled = abs(self.rect.centery - self.approach_start_y)
				if distance_traveled >= self.approach_distance:
					# Reached target distance - stop and trigger dialog
					self.direction = vector(0, 0)
					self.has_moved = True
					self.approaching = False
					self.start_dialog()
					self.create_dialog(self)
					return

			# Normal collision-based movement
			if not self.hitbox.inflate(50,50).colliderect(self.player.hitbox):
				self.rect.center += self.direction * self.speed * dt
				self.hitbox.center = self.rect.center
			else:
				self.direction = vector(0,0) #NCP stops moving
				self.has_moved = True
				self.start_dialog()  # Save facing direction and set in_dialog flag
				self.create_dialog(self)
				self.player.noticed = False

	def update(self, dt):
		for timer in self.timers.values():
			timer.update()

		self.animate(dt)

		# Prioritize returning to start over other behaviors
		if self.returning_to_start:
			self.return_to_start(dt)
		elif self.character_data['look_around']:
			self.raycast()
			self.move(dt)
		else:
			# Characters without look_around can still patrol
			self.patrol_move(dt)

class Player(Entity):
	def __init__(self, pos, frames, groups, facing_direction, collision_sprites):
		super().__init__(pos, frames, groups, facing_direction)
		self.collision_sprites = collision_sprites
		self.noticed = False

	def input(self):
		keys = pygame.key.get_pressed()
		input_vector = vector()
		if keys[pygame.K_UP]:
			input_vector.y -= 1
		if keys[pygame.K_DOWN]:
			input_vector.y += 1
		if keys[pygame.K_LEFT]:
			input_vector.x -= 1
		if keys[pygame.K_RIGHT]:
			input_vector.x += 1
		self.direction = input_vector.normalize() if input_vector else input_vector

	def move(self, dt):
		self.rect.centerx += self.direction.x * self.speed * dt
		self.hitbox.centerx = self.rect.centerx
		self.collisions('horizontal')

		self.rect.centery += self.direction.y * self.speed * dt
		self.hitbox.centery = self.rect.centery
		self.collisions('vertical')

	def collisions(self, axis):
		for sprite in self.collision_sprites:
			if sprite.hitbox.colliderect(self.hitbox):
				if axis == 'horizontal':
					if self.direction.x > 0: 
						self.hitbox.right = sprite.hitbox.left
					if self.direction.x < 0:
						self.hitbox.left = sprite.hitbox.right
					self.rect.centerx = self.hitbox.centerx
				else:
					if self.direction.y > 0:
						self.hitbox.bottom = sprite.hitbox.top
					if self.direction.y < 0:
						self.hitbox.top = sprite.hitbox.bottom
					self.rect.centery = self.hitbox.centery

	def update(self, dt):
		self.y_sort = self.rect.centery
		if not self.blocked:
			self.input()
			self.move(dt)
		self.animate(dt)