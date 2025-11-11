print("MAIN.PY: Module loading started")

from settings import *
from game_data import *
from pytmx.util_pygame import load_pygame #import tmx files into pygame
from os.path import join
from random import randint

from sprites import Sprite, AnimatedSprite, BorderSprite, CollidableSprite, BuildingSprite, TransitionSprite, VictoryParticleEffect
from entities import Player, Character
from groups import AllSprites
from dialog import DialogTree, MapTitleSprite
from monster_index import MonsterIndex
from battle import Battle
from title_screen import TitleScreen, ControlsScreen, CreditsScreen

from support import *
from monster import Monster
from calculations import calculate_city_scale_indicators, pollution_limit_harsh

print("MAIN.PY: All imports successful")

# Map titles for non-world maps
MAP_TITLES = {
	'castle': 'Government department of environment',
	'factory': 'Greentown pharmaceuticals',
	'hospital': 'Greentown hospital',
	'house': 'Retirement home',
	'laboratory': 'University of Greentown',
	'ngo': 'Citizen environmental action group'
}

class Game:
	#general
	def __init__(self):
		print("=== Starting Game Initialization ===")
		pygame.init()
		print("✓ Pygame initialized")
		self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
		print("✓ Display surface created")
		pygame.display.set_caption('Sustainable Pharmaceuticals')
		self.clock = pygame.time.Clock()
		print("✓ Clock created")

		# Import assets first (needed for title screen)
		print("Starting asset import...")
		self.import_assets()
		print("✓ Assets imported")
		
		# Title screen and menu screens
		print("Creating title screen...")
		self.title_screen = TitleScreen(self.fonts)
		print("✓ Title screen created")
		self.controls_screen = None
		self.credits_screen = None
		self.current_menu_screen = 'title'  # 'title', 'controls', or 'credits'
		self.game_started = False
		print("=== Game Initialization Complete ===")

		#player monsters # use to install initial stats? also update
		self.player_monsters = {
			0: Monster('molecule_C1', 1),      						# scientist - FG_left (default)
			1: Monster('molecule_A1', 1),     						# scientist - molecule_template_left (default)
			2: Monster('molecule_B1', 1),      						# scientist - molecule_template_right (default)
			3: Monster('molecule_D1', 1),      						# scientist - FG_right (default)
			4: Monster('Standard PPE', 1),          				# factory0 - safety (default)
			5: Monster('No wastewater treatment', 1),      			# factory0 - emissions (default)
			6: Monster('Standard energy', 1),          				# factory0 - energy (default)
			7: Monster('Single use dispensing cup', 1),     		# medic - cups (default)
			8: Monster('Prescribe as required', 1),    				# medic - normal prescribe (default)
			9: Monster('No procurement rules', 1),      			# ngo - procurement (default)
			10: Monster('Lenient water quality standards', 1),      # ngo - pollution_standards (default)
			11: Monster('No biodegradation standard', 1),           # ngo - biodegradation_standards (default)
			12: Monster('reaction_temperature', 75),         
			13: Monster('reaction_hours', 6)          
		}
		
		#groups
		self.all_sprites = AllSprites()
		self.collision_sprites = pygame.sprite.Group()
		self.character_sprites = pygame.sprite.Group()
		self.transition_sprites = pygame.sprite.Group()

		# map transitions
		self.transition_target = None
		self.tint_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
		self.tint_mode = 'untint'
		self.tint_progress = 0
		self.tint_direction = -1
		self.tint_speed = 600

		# Setup will be called after title screen
		self.monster_index = None
		self.index_open = False
		self.battle = None
		self.dialog_tree = None
		self.endgame_triggered = False
		self.current_tmx_map = None
		self.victory_particles = None  # For victory sparkle effect

	def import_assets(self):
		print("  Importing TMX maps...")
		self.tmx_maps = tmx_importer('data', 'maps')
		print(f"  ✓ TMX maps loaded: {list(self.tmx_maps.keys())}")

		print("  Importing overworld frames...")
		self.overworld_frames = {
			'greenwater': import_folder('graphics', 'tilesets', 'greenwater'),
			'bluewater': import_folder('graphics', 'tilesets', 'bluewater'),
			'characters': all_character_import('graphics', 'characters')
		}
		print("  ✓ Overworld frames loaded")

		print("  Importing monster frames...")
		self.monster_frames = {
			'icons': import_folder_dict('graphics', 'icons'),
			'monsters': monster_importer(4,2,'graphics', 'monsters'),
			'ui': import_folder_dict('graphics', 'ui')
		}
		print("  Creating outlines...")
		self.monster_frames['outlines'] = outline_creator(self.monster_frames['monsters'], 4) # will make a white border around image of 4 pixels in the shape of the image
		print("  ✓ Monster frames loaded")

		print("  Loading fonts...")
		self.fonts = {
			'dialog': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 18),
			'regular': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 12),
			'small': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 10),
			'bold': pygame.font.Font(join('graphics', 'fonts', 'dogicapixelbold.otf'), 12),
			'title_big': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 30),
			'title_subtext': pygame.font.Font(join('graphics', 'fonts', 'PixeloidSans.ttf'), 20),
		}
		print("  ✓ Fonts loaded")
		print("  Loading backgrounds...")
		self.bg_frames = import_folder_dict('graphics', 'backgrounds')
		print("  ✓ Backgrounds loaded")

	def setup(self, tmx_map, player_start_pos):
		# Store the current map
		self.current_tmx_map = tmx_map
		
		# clear main map
		for group in (self.all_sprites, self.collision_sprites, self.transition_sprites, self.character_sprites):
			group.empty()
		
		# terrain
		for layer in ['Terrain', 'Flowers', 'Terrain Top']:
			for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
				if surf:  # Only create sprite if tile has an image
					Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, WORLD_LAYERS['bg'])
		
		# water (check pollution level to determine color)
		# Calculate current pollution level
		indicators = calculate_city_scale_indicators(self.player_monsters)
		total_pollution = indicators['city_api_emissions'] + indicators['city_meta_emissions']
		
		# Use bluewater if pollution is below harsh limit, otherwise use greenwater
		water_frames = self.overworld_frames['bluewater'] if total_pollution < pollution_limit_harsh else self.overworld_frames['greenwater']
		
		for obj in tmx_map.get_layer_by_name('Water'):
			for x in range(int(obj.x), int(obj.x + obj.width), WATER_TILE_SIZE): #using water tiles of 64 pixels not 12
				for y in range(int(obj.y), int(obj.y + obj.height), WATER_TILE_SIZE):
					AnimatedSprite((x, y), water_frames, self.all_sprites, WORLD_LAYERS['water'])

		# objects
		for obj in tmx_map.get_layer_by_name('Objects'):
			if obj.image:  # Only create sprite if object has an image
				if obj.name == 'top':
					Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
				else:
					CollidableSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

		# buildings (separate objects because of scale difference
		for obj in tmx_map.get_layer_by_name('Buildings'):
			if obj.image:  # Only create sprite if object has an image
				if obj.name == 'top':
					Sprite((obj.x, obj.y), obj.image, self.all_sprites, WORLD_LAYERS['top'])
				else:
					BuildingSprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))

		# transition (between maps) objects
		for obj in tmx_map.get_layer_by_name('Transition'):
			TransitionSprite((obj.x, obj.y), (obj.width, obj.height), (obj.properties['target'], obj.properties['pos']), self.transition_sprites)

		# collision objects
		for obj in tmx_map.get_layer_by_name('Collisions'):
			BorderSprite((obj.x, obj.y), pygame.Surface((obj.width, obj.height)), self.collision_sprites)

		# entities
		for obj in tmx_map.get_layer_by_name('Entities'):
			if obj.name == 'player':
				if obj.properties['pos'] == player_start_pos:
					self.player = Player(
						pos = (obj.x, obj.y),
						frames = self.overworld_frames['characters']['player'],
						groups = self.all_sprites,
						facing_direction = obj.properties['direction'],
						collision_sprites = self.collision_sprites)
			else:
				Character(
					pos = (obj.x, obj.y),
					frames = self.overworld_frames['characters'][obj.properties['graphic']],
					groups = (self.all_sprites, self.collision_sprites, self.character_sprites),
					facing_direction = obj.properties['direction'],
					character_data = NPC_DATA[obj.properties['character_id']],
					player = self.player,
					create_dialog = self.create_dialog,
					collision_sprites = self.collision_sprites,
					radius = obj.properties['radius'],
					chattycharacter = obj.properties['interaction'] == 'chat',
					game = self)

		# Display map title for non-world maps
		# Get the map name from the tmx_maps dictionary
		for map_name, map_obj in self.tmx_maps.items():
			if map_obj == tmx_map and map_name in MAP_TITLES:
				MapTitleSprite(MAP_TITLES[map_name], self.all_sprites, self.fonts['dialog'], self.player)
				break

	# dialog system
	def input(self):
		if not self.dialog_tree and not self.battle:
			keys = pygame.key.get_just_pressed()
			if keys[pygame.K_SPACE] and not self.index_open:
				for character in self.character_sprites:
					if check_connections(100, self.player, character):
						self.player.block()
						character.start_dialog()  # Save facing direction and set in_dialog flag
						character.change_facing_direction(self.player.rect.center)  # Turn to face player
						self.create_dialog(character)
						character.can_rotate = False

			if keys[pygame.K_RETURN] and not self.dialog_tree:
				self.index_open = not self.index_open
				self.player.blocked = not self.player.blocked

	def create_dialog(self, character):
		if not self.dialog_tree:
			# Check if mission is complete (COMPLIANT status)
			from calculations import check_compliance_thresholds
			compliance = check_compliance_thresholds(self.player_monsters)
			
			# If overall compliant, set endgame flag for this character
			if compliance.get('overall_compliant', False):
				character.character_data['endgame'] = True
			
			self.dialog_tree = DialogTree(character, self.player, self.all_sprites, self.fonts['dialog'], self.end_dialog)

	def end_dialog(self, character):
		self.dialog_tree = None
		character.end_dialog_movement()  # Restore patrol behavior

		# Check if this character has a biome (which means it should trigger a battle)
		if character.character_data.get('biome'):
			# Restore monster health/energy
			for monster in self.player_monsters.values():
				monster.health = monster.get_stat('max_health')
				monster.energy = monster.get_stat('max_energy')

			# Trigger a battle after dialogue
			self.transition_target = Battle(
				player_monsters = self.player_monsters,
				opponent_monsters = {},  # Not used anymore, data comes from character_data
				monster_frames = self.monster_frames,
				bg_surf = self.bg_frames[character.character_data['biome']],
				fonts = self.fonts,
				end_battle = self.end_battle,
				character = character
			)
			self.tint_mode = 'tint'
		else:
			# For non-battle characters (including chattycharacters), update the visited and return flags
			if not character.character_data['visited']:
				# First interaction complete - mark as visited
				character.character_data['visited'] = True
			elif not character.character_data['return']:
				# Second interaction complete - mark that return dialog has been seen
				character.character_data['return'] = True
			self.player.unblock()

	# transition methods
	def transition_check(self):
		sprites = [sprite for sprite in self.transition_sprites if sprite.rect.colliderect(self.player.hitbox)]
		if sprites:
			self.player.block()
			self.transition_target = sprites[0].target
			self.tint_mode = 'tint'

	def tint_screen(self, dt):
		if self.tint_mode == 'untint':
			self.tint_progress -= self.tint_speed * dt

		if self.tint_mode == 'tint':
			self.tint_progress += self.tint_speed * dt
			if self.tint_progress >= 255:
				if type(self.transition_target) == Battle:
					self.battle = self.transition_target
				elif self.transition_target == 'endgame':
					# Transition to castle map at endgame spawn point
					self.setup(self.tmx_maps['castle'], 'endgame')
					self.player.unblock()
					# Start victory particle effect around the player
					# When particles finish, trigger boss to approach
					self.victory_particles = VictoryParticleEffect(
						self.player,
						self.all_sprites,
						duration=2.4,
						on_complete=self.trigger_boss_approach
					)
				elif isinstance(self.transition_target, tuple):  # for map transitions
					self.setup(self.tmx_maps[self.transition_target[0]], self.transition_target[1])
				elif self.transition_target == 'level':
					self.battle = None

				# reset tint and target only AFTER activating the battle
				self.tint_mode = 'untint'
				self.transition_target = None

		self.tint_progress = max(0, min(self.tint_progress, 255))
		self.tint_surf.set_alpha(self.tint_progress)
		self.display_surface.blit(self.tint_surf, (0,0))



	def end_battle(self, character):
		"""Called when a battle finishes."""
		if character:
			# Remove battle immediately
			self.battle = None
			self.tint_mode = 'untint'

			# Update visit flags
			if not character.character_data['visited']:
				character.character_data['visited'] = True
			else:
				character.character_data['return'] = True

			# Always show 'visited' dialog after battle if it exists
			visited_dialog = character.character_data['dialog'].get('visited')
			if visited_dialog:
				# Create a temporary dialog tree for visited message
				self.dialog_tree = DialogTree(
					character,
					self.player,
					self.all_sprites,
					self.fonts['dialog'],
					self._end_post_battle_dialog
				)
				# Override the dialog with visited dialog
				self.dialog_tree.dialog = visited_dialog if isinstance(visited_dialog, list) else [visited_dialog]
				self.dialog_tree.dialog_num = len(self.dialog_tree.dialog)
				self.dialog_tree.dialog_index = 0
				self.dialog_tree.current_dialog.kill()
				from dialog import DialogSprite
				self.dialog_tree.current_dialog = DialogSprite(self.dialog_tree.dialog[0], character, self.all_sprites, self.fonts['dialog'])
			else:
				# No dialog, check for endgame immediately
				if not self.endgame_triggered:
					from calculations import check_compliance_thresholds
					compliance = check_compliance_thresholds(self.player_monsters)
					
					if compliance.get('overall_compliant', False):
						self.endgame_triggered = True
						character.character_data['endgame'] = True
						
						# Trigger endgame transition
						self.player.block()
						self.transition_target = 'endgame'
						self.tint_mode = 'tint'
						return  # Exit early
				
				self.player.unblock()
		else:
			self.transition_target = 'level'
			self.tint_mode = 'tint'
			self.player.unblock()

	def _end_post_battle_dialog(self, character):
		"""Helper to unblock player after post-battle dialog."""
		self.dialog_tree = None
		character.end_dialog_movement()  # Restore patrol behavior

		# Check if player achieved COMPLIANT status
		if not self.endgame_triggered:
			from calculations import check_compliance_thresholds
			compliance = check_compliance_thresholds(self.player_monsters)

			if compliance.get('overall_compliant', False):
				self.endgame_triggered = True
				character.character_data['endgame'] = True

				# Trigger endgame transition
				self.player.block()
				self.transition_target = 'endgame'
				self.tint_mode = 'tint'
				return  # Exit early to trigger transition

		self.player.unblock()



	def _end_visited_dialog(self, character):
		self.dialog_tree = None
		character.end_dialog_movement()  # Restore patrol behavior
		self.player.unblock()

	def trigger_boss_approach(self):
		"""Called when victory particles finish - makes boss character approach player"""
		# Find the boss character in the castle map
		for character in self.character_sprites:
			# Check if this is the boss by looking at character_data
			from game_data import NPC_DATA
			for char_id, char_data in NPC_DATA.items():
				if char_data is character.character_data and char_id == 'boss':
					# Mark as endgame so raycast allows movement
					character.character_data['endgame'] = True
					# Reset visited flag so move() will trigger dialog properly
					character.character_data['visited'] = False

					# Block the player and make them face the boss
					self.player.block()
					self.player.change_facing_direction(character.rect.center)

					# Set up boss for limited movement
					character.can_rotate = False
					character.has_noticed = True
					character.has_moved = False

					# Store starting position and target distance
					character.approach_start_y = character.rect.centery
					character.approach_distance = 65  # Walk exactly 120 pixels down
					character.approaching = True

					# Force boss to walk straight down
					character.direction = vector(0, 1)

					return

	def start_game(self):
		"""Initialize the game after title screen"""
		self.setup(self.tmx_maps['world'], 'bank') #player start position in the world map
		self.monster_index = MonsterIndex(self.player_monsters, self.fonts, self.monster_frames)
		self.game_started = True


	async def run(self):
		while True:
			dt = self.clock.tick() / 1000
			self.display_surface.fill('black')

			# event loop
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					exit()

			# Show title screen or run game
			if not self.game_started:
				if self.current_menu_screen == 'title':
					result = self.title_screen.update(dt)
					if result == 'start':
						self.start_game()
					elif result == 'controls':
						# Create controls screen with same background as title screen
						self.controls_screen = ControlsScreen(self.fonts, self.title_screen.bg_image)
						self.current_menu_screen = 'controls'
					elif result == 'credits':
						# Create credits screen with same background as title screen
						self.credits_screen = CreditsScreen(self.fonts, self.title_screen.bg_image)
						self.current_menu_screen = 'credits'
				elif self.current_menu_screen == 'controls':
					if self.controls_screen.update(dt):
						# Return to title screen
						self.current_menu_screen = 'title'
						self.title_screen.active = True
				elif self.current_menu_screen == 'credits':
					if self.credits_screen.update(dt):
						# Return to title screen
						self.current_menu_screen = 'title'
						self.title_screen.active = True
			else:
				# update the game
				self.input()
				self.transition_check()
				self.all_sprites.update(dt)

				# Update victory particle effect if active
				if self.victory_particles:
					self.victory_particles.update(dt)

				# drawing
				self.all_sprites.draw(self.player)

				# overlays
				if self.dialog_tree: self.dialog_tree.update()
				if self.index_open:  self.monster_index.update(dt)
				if self.battle: 	 self.battle.update(dt) #need to modify from battle to the character interactions

				self.tint_screen(dt)

			pygame.display.update()
			await asyncio.sleep(0)  # Yield control to browser

# Pygbag entry point - must be named 'main' and be async
async def main():
	import asyncio
	print("=== Starting Application ===")
	try:
		game = Game()
		print("=== Starting Game Loop ===")
		await game.run()
	except Exception as e:
		print(f"ERROR: {type(e).__name__}: {e}")
		import traceback
		traceback.print_exc()

# For local testing
if __name__ == '__main__':
	import asyncio
	asyncio.run(main())