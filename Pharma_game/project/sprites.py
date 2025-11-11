from settings import *
from random import uniform, randint, choice
from support import draw_bar
from timer import Timer
import math

# overworld sprites
class Sprite(pygame.sprite.Sprite):
	def __init__(self, pos, surf, groups, z = WORLD_LAYERS['main']):
		super().__init__(groups)
		self.image = surf 
		self.rect = self.image.get_frect(topleft = pos)
		self.z = z
		self.y_sort = self.rect.centery
		self.hitbox = self.rect.copy()

class BorderSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.copy()

class TransitionSprite(Sprite):
	def __init__(self, pos, size, target, groups):
		surf = pygame.Surface(size)
		super().__init__(pos, surf, groups)
		self.target = target

class CollidableSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.inflate(-self.rect.width * 0.2, -self.rect.height * 0.6)
		self.hitbox.top = self.rect.top + self.rect.height * 0.4

class BuildingSprite(Sprite):
	def __init__(self, pos, surf, groups):
		super().__init__(pos, surf, groups)
		self.hitbox = self.rect.inflate(0, -80)
		self.hitbox.bottom = self.rect.bottom - 20

class AnimatedSprite(Sprite):
	def __init__(self, pos, frames, groups, z = WORLD_LAYERS['main']):
		self.frame_index, self.frames = 0, frames
		super().__init__(pos, frames[self.frame_index], groups, z)
	
	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.image = self.frames[int(self.frame_index % len(self.frames))]
	
	def update(self, dt):
		self.animate(dt)

# battle sprites (modified for non-combat)
class MonsterSprite(pygame.sprite.Sprite):
	def __init__(self, pos, frames, groups, monster, index, pos_index, entity, apply_attack, create_monster):
		#data
		self.index = index
		self.pos_index = pos_index
		self.entity = entity
		self.monster = monster
		self.frame_index, self.frames, self.state = 0, frames, 'idle'
		self.animation_speed = ANIMATION_SPEED + uniform(-1,1)
		self.z = BATTLE_LAYERS['monster']
		self.create_monster = create_monster

		#sprite
		super().__init__(groups)
		self.image = self.frames[self.state][self.frame_index]
		self.rect = self.image.get_frect(center = pos)

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		self.adjusted_frame_index = int(self.frame_index % len(self.frames[self.state]))
		self.image = self.frames[self.state][self.adjusted_frame_index]

	def update(self, dt):
		self.animate(dt)
		# Monster stats no longer update automatically (no initiative system)

class MonsterOutlineSprite(pygame.sprite.Sprite):
	def __init__(self, monster_sprite, groups, frames):
		super().__init__(groups)
		self.z = BATTLE_LAYERS['outline']
		self.monster_sprite = monster_sprite
		self.frames = frames

		self.image = self.frames[self.monster_sprite.state][self.monster_sprite.frame_index]
		self.rect = self.image.get_frect(center = self.monster_sprite.rect.center)

	def update(self, _):
		self.image = self.frames[self.monster_sprite.state][self.monster_sprite.adjusted_frame_index]
		if not self.monster_sprite.groups():
			self.kill()

class MonsterNameSprite(pygame.sprite.Sprite):
	def __init__(self, pos, monster_sprite, groups, font):
		super().__init__(groups)
		self.monster_sprite = monster_sprite
		self.z = BATTLE_LAYERS['name']

		text_surf = font.render(monster_sprite.monster.name, False, COLORS['black'])
		padding = 4

		self.image = pygame.Surface((text_surf.get_width() + 2 * padding, text_surf.get_height() + 2 * padding)) 
		self.image.fill(COLORS['white'])
		self.image.blit(text_surf, (padding, padding))
		self.rect = self.image.get_frect(midtop = pos)

	def update(self, _):
		if not self.monster_sprite.groups():
			self.kill()

class MonsterLevelSprite(pygame.sprite.Sprite):
	def __init__(self, entity, pos, monster_sprite, groups, font):
		super().__init__(groups)
		self.monster_sprite = monster_sprite
		self.font = font
		self.z = BATTLE_LAYERS['name']

		self.image = pygame.Surface((60,26))
		self.rect = self.image.get_frect(topleft = pos) if entity == 'player' else self.image.get_frect(topright = pos)
		self.xp_rect = pygame.FRect(0,self.rect.height - 2,self.rect.width,2)

	def update(self, _):
		self.image.fill(COLORS['white'])

		text_surf = self.font.render(f'Lvl {self.monster_sprite.monster.level}', False, COLORS['black'])
		text_rect = text_surf.get_frect(center = (self.rect.width / 2, self.rect.height / 2))
		self.image.blit(text_surf, text_rect)

		draw_bar(self.image, self.xp_rect, self.monster_sprite.monster.xp, self.monster_sprite.monster.level_up, COLORS['black'], COLORS['white'], 0)

		if not self.monster_sprite.groups():
			self.kill()

class MonsterStatsSprite(pygame.sprite.Sprite):
	def __init__(self, pos, monster_sprite, size, groups, font):
		super().__init__(groups)
		self.monster_sprite = monster_sprite
		self.image = pygame.Surface(size) 
		self.rect = self.image.get_frect(midleft = pos)  # Changed from midbottom to midleft
		self.font = font
		self.z = BATTLE_LAYERS['overlay']

	def update(self, _):
		self.image.fill(COLORS['white'])

		# Display health and energy stacked vertically
		stats_info = [
			('HP', self.monster_sprite.monster.health, self.monster_sprite.monster.get_stat('max_health'), COLORS['red']),
			('EP', self.monster_sprite.monster.energy, self.monster_sprite.monster.get_stat('max_energy'), COLORS['blue'])
		]

		stat_height = self.rect.height / 2
		
		for index, (label, value, max_value, color) in enumerate(stats_info):
			y_offset = index * stat_height
			
			# Label and value text
			text = f'{label}: {int(value)}/{int(max_value)}'
			text_surf = self.font.render(text, False, COLORS['black'])
			text_rect = text_surf.get_frect(topleft = (10, y_offset + 5))
			
			# Bar underneath text
			bar_rect = pygame.FRect(10, text_rect.bottom + 2, self.rect.width - 20, 6)
			
			self.image.blit(text_surf, text_rect)
			draw_bar(self.image, bar_rect, value, max_value, color, COLORS['light-gray'], 2)

		if not self.monster_sprite.groups():
			self.kill()

class AttackSprite(AnimatedSprite):
	def __init__(self, pos, frames, groups):
		super().__init__(pos, frames, groups, BATTLE_LAYERS['overlay'])
		self.rect.center = pos

	def animate(self, dt):
		self.frame_index += ANIMATION_SPEED * dt
		if self.frame_index < len(self.frames):
			self.image = self.frames[int(self.frame_index)]
		else:
			self.kill()

	def update(self, dt):
		self.animate(dt)

class TimedSprite(Sprite):
	def __init__(self, pos, surf, groups, duration):
		super().__init__(pos, surf, groups, z = BATTLE_LAYERS['overlay'])
		self.rect.center = pos
		self.death_timer = Timer(duration, autostart = True, func = self.kill)

	def update(self, _):
		self.death_timer.update()

class ParticleSprite(pygame.sprite.Sprite):
	"""A particle sprite for visual effects like sparkles, stars, confetti"""
	def __init__(self, pos, groups, particle_type='sparkle', z=WORLD_LAYERS['top']):
		super().__init__(groups)
		self.z = z
		self.y_sort = pos[1]

		# Particle properties
		self.particle_type = particle_type
		self.lifetime = uniform(0.5, 1.5)  # How long particle lives (seconds)
		self.age = 0  # Current age

		# Movement
		self.pos = vector(pos)
		if particle_type == 'sparkle':
			# Sparkles float upward and slightly sideways
			self.velocity = vector(uniform(-20, 20), uniform(-80, -40))
			self.acceleration = vector(0, -10)  # Slow upward acceleration
			self.size = randint(2, 5)
			self.color = choice([COLORS['gold'], COLORS['white'], '#ffeb3b', '#ffd54f'])
		elif particle_type == 'star':
			# Stars shoot outward
			angle = uniform(0, 2 * math.pi)
			speed = uniform(50, 150)
			self.velocity = vector(math.cos(angle) * speed, math.sin(angle) * speed)
			self.acceleration = vector(0, 50)  # Gravity
			self.size = randint(3, 6)
			self.color = choice([COLORS['gold'], '#fff59d', '#ffee58'])
		elif particle_type == 'confetti':
			# Confetti falls and spins
			self.velocity = vector(uniform(-30, 30), uniform(-100, -50))
			self.acceleration = vector(0, 200)  # Strong gravity
			self.size = randint(3, 7)
			self.color = choice([COLORS['blue'], COLORS['red'], COLORS['gold'], '#4caf50', '#9c27b0'])
			self.rotation = uniform(0, 360)
			self.rotation_speed = uniform(-500, 500)

		# Create initial surface
		self.original_size = self.size
		self.update_surface()

	def update_surface(self):
		"""Update the particle surface based on type and current properties"""
		if self.particle_type == 'sparkle':
			# Draw a diamond/star shape
			self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
			points = [
				(self.size, 0),  # top
				(self.size * 2, self.size),  # right
				(self.size, self.size * 2),  # bottom
				(0, self.size)  # left
			]
			pygame.draw.polygon(self.image, self.color, points)
		elif self.particle_type == 'star':
			# Draw a 4-pointed star
			self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
			center = self.size
			# Draw horizontal and vertical lines forming a star
			pygame.draw.line(self.image, self.color, (center, 0), (center, self.size * 2), 2)
			pygame.draw.line(self.image, self.color, (0, center), (self.size * 2, center), 2)
		elif self.particle_type == 'confetti':
			# Draw a rotated rectangle
			surf_size = int(self.size * 2)
			self.image = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)
			rect_surf = pygame.Surface((self.size, self.size * 1.5))
			rect_surf.fill(self.color)
			rotated = pygame.transform.rotate(rect_surf, self.rotation)
			rect = rotated.get_rect(center=(surf_size // 2, surf_size // 2))
			self.image.blit(rotated, rect)

		self.rect = self.image.get_frect(center=self.pos)

	def update(self, dt):
		# Age the particle
		self.age += dt

		# Kill particle if it's too old
		if self.age >= self.lifetime:
			self.kill()
			return

		# Update physics
		self.velocity += self.acceleration * dt
		self.pos += self.velocity * dt

		# Update rotation for confetti
		if self.particle_type == 'confetti':
			self.rotation += self.rotation_speed * dt

		# Fade out as particle ages
		fade_ratio = 1 - (self.age / self.lifetime)
		self.size = max(1, int(self.original_size * fade_ratio))

		# Update surface with new properties
		self.update_surface()

		# Apply alpha based on age
		alpha = int(255 * fade_ratio)
		self.image.set_alpha(alpha)

class VictoryParticleEffect:
	"""Manages spawning victory particles around the player"""
	def __init__(self, player, groups, duration=3.0, on_complete=None):
		self.player = player
		self.groups = groups
		self.duration = duration  # How long the effect lasts
		self.elapsed = 0
		self.spawn_timer = 0
		self.spawn_interval = 0.05  # Spawn particles every 50ms
		self.active = True
		self.on_complete = on_complete  # Callback function when effect finishes
		self.completed = False  # Track if we've already called the callback

	def update(self, dt):
		if not self.active:
			return

		self.elapsed += dt
		self.spawn_timer += dt

		# Check if effect is complete
		if self.elapsed >= self.duration:
			self.active = False
			# Call the completion callback once
			if not self.completed and self.on_complete:
				self.on_complete()
				self.completed = True
			return

		# Spawn particles at regular intervals
		if self.spawn_timer >= self.spawn_interval:
			self.spawn_timer = 0
			self.spawn_particles()

	def spawn_particles(self):
		"""Spawn particles around the player"""
		# Spawn multiple particles in a burst
		for _ in range(randint(2, 4)):
			# Random position around player
			offset_x = uniform(-30, 30)
			offset_y = uniform(-30, 30)
			pos = (self.player.rect.centerx + offset_x, self.player.rect.centery + offset_y)

			# Mix of particle types for variety
			particle_type = choice(['sparkle', 'sparkle', 'star'])  # More sparkles than stars
			ParticleSprite(pos, self.groups, particle_type)