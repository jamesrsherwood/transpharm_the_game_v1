from settings import *
from support import import_image

class TitleScreen:
    def __init__(self, fonts):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.active = True
        
        # Load background image
        try:
            self.bg_image = import_image('graphics', 'backgrounds', 'title')
            # Scale to fit screen if needed
            if self.bg_image.get_size() != (WINDOW_WIDTH, WINDOW_HEIGHT):
                self.bg_image = pygame.transform.scale(self.bg_image, (WINDOW_WIDTH, WINDOW_HEIGHT))
        except:
            # Fallback if image doesn't exist
            self.bg_image = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            self.bg_image.fill(COLORS['dark'])
        
        # Title text at top
        self.title_text = "Sustainable Pharmaceuticals"
        self.title_y = 100
        
        # Text box dimensions (single centered box)
        self.box_width = WINDOW_WIDTH * 0.6
        self.box_height = WINDOW_HEIGHT * 0.4
        self.box_x = (WINDOW_WIDTH - self.box_width) / 2
        self.box_y = WINDOW_HEIGHT * 0.3
        
        # Bottom buttons
        self.button_y = WINDOW_HEIGHT - 150
        self.button_width = 200
        self.button_height = 50
        self.button_spacing = 20

        # Calculate button positions (centered)
        total_width = (3 * self.button_width) + (2 * self.button_spacing)
        start_x = (WINDOW_WIDTH - total_width) / 2

        self.buttons = {
            'start': {
                'rect': pygame.FRect(start_x, self.button_y, self.button_width, self.button_height),
                'text': 'Start Game',
                'color': COLORS['fire']
            },
            'controls': {
                'rect': pygame.FRect(start_x + self.button_width + self.button_spacing, self.button_y, self.button_width, self.button_height),
                'text': 'Controls',
                'color': COLORS['water']
            },
            'credits': {
                'rect': pygame.FRect(start_x + 2 * (self.button_width + self.button_spacing), self.button_y, self.button_width, self.button_height),
                'text': 'Credits',
                'color': COLORS['plant']
            }
        }

        # Bottom instruction
        self.instruction_text = "Use LEFT/RIGHT arrows to navigate, SPACE to select"
        self.instruction_y = WINDOW_HEIGHT - 80
        
        # text for box
        self.box_content = [
            "You are an intrepid citizen scientist who is on a mission to find the source of the environmental pollution that is negatively effecting your town.",
            "The local drug manufacturing plant is the most likely source.",
            "Your objective is to find out about drug design, manufacturing processes, policy, and medical practices in order to minimise the environmental impact of pharmaceuticals.",
            "Talk to the characters to get information and negotiate improvements."
        ]
        
        # Blinking effect for instruction
        self.blink_timer = 0
        self.blink_speed = 0.001  # Blinks per second
        self.show_instruction = True

        # Button selection for keyboard navigation
        self.button_names = ['start', 'controls', 'credits']
        self.selected_button = 0
    
    def draw_text_box(self, x, y, width, height, content):
        """Draw a text box with background and content"""
        # Background
        box_rect = pygame.FRect(x, y, width, height)
        pygame.draw.rect(self.display_surface, COLORS['gray'], box_rect, 0, 10)
        pygame.draw.rect(self.display_surface, COLORS['white'], box_rect, 3, 10)

        # Combine all content into one paragraph
        paragraph = ' '.join(line for line in content if line)

        # Content with text wrapping
        padding = 15
        line_height = 30
        max_text_width = width - (2 * padding)

        # Split text into words and wrap them
        words = paragraph.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.fonts['title_subtext'].render(test_line, False, COLORS['white'])

            if test_surf.get_width() <= max_text_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Calculate total text height and center it vertically
        total_text_height = len(lines) * line_height
        start_y = y + (height - total_text_height) / 2

        # Draw the wrapped lines
        for i, line in enumerate(lines):
            text_surf = self.fonts['title_subtext'].render(line, False, COLORS['white'])
            text_rect = text_surf.get_frect(centerx=x + width / 2, top=start_y + i * line_height)
            self.display_surface.blit(text_surf, text_rect)

    def input(self):
        """Check for keyboard navigation"""
        keys = pygame.key.get_just_pressed()

        # Left/Right arrow keys to navigate
        if keys[pygame.K_LEFT]:
            self.selected_button = (self.selected_button - 1) % len(self.button_names)
        elif keys[pygame.K_RIGHT]:
            self.selected_button = (self.selected_button + 1) % len(self.button_names)

        # Space to activate selected button
        if keys[pygame.K_SPACE]:
            button_name = self.button_names[self.selected_button]
            if button_name == 'start':
                self.active = False
            return button_name

        return None
    
    def update(self, dt):
        """Update and draw the title screen"""
        if not self.active:
            return False
        
        # Update blink timer
        self.blink_timer += dt
        if self.blink_timer >= 1.0 / self.blink_speed:
            self.blink_timer = 0
            self.show_instruction = not self.show_instruction
        
        # Draw background
        self.display_surface.blit(self.bg_image, (0, 0))
        
        # Draw title
        title_surf = self.fonts['title_big'].render(self.title_text, False, COLORS['white'])
        # Scale up the title for bigger text
        title_surf = pygame.transform.scale2x(title_surf)
        title_rect = title_surf.get_frect(centerx=WINDOW_WIDTH / 2, top=self.title_y)

        # Add shadow for title
        shadow_surf = self.fonts['title_big'].render(self.title_text, False, COLORS['black'])
        shadow_surf = pygame.transform.scale2x(shadow_surf)
        shadow_rect = shadow_surf.get_frect(centerx=WINDOW_WIDTH / 2 + 3, top=self.title_y + 3)
        self.display_surface.blit(shadow_surf, shadow_rect)
        self.display_surface.blit(title_surf, title_rect)

        # Draw centered text box
        self.draw_text_box(
            self.box_x,
            self.box_y,
            self.box_width,
            self.box_height,
            self.box_content
        )

        # Draw buttons
        for i, button_name in enumerate(self.button_names):
            button_data = self.buttons[button_name]
            rect = button_data['rect']
            is_selected = i == self.selected_button

            # Button background
            button_color = COLORS['white'] if is_selected else button_data['color']
            pygame.draw.rect(self.display_surface, button_color, rect, 0, 10)
            pygame.draw.rect(self.display_surface, COLORS['white'], rect, 3, 10)

            # Button text
            text_color = button_data['color'] if is_selected else COLORS['white']
            text_surf = self.fonts['title_subtext'].render(button_data['text'], False, text_color)
            text_rect = text_surf.get_frect(center=rect.center)
            self.display_surface.blit(text_surf, text_rect)

        # Draw instruction (with blink effect)
        if self.show_instruction:
            instruction_surf = self.fonts['title_subtext'].render(self.instruction_text, False, COLORS['fire'])
            instruction_rect = instruction_surf.get_frect(centerx=WINDOW_WIDTH / 2, top=self.instruction_y)
            
            box_padding = 15
            box_rect = pygame.FRect(
                instruction_rect.left - box_padding,
                instruction_rect.top - box_padding,
                instruction_rect.width + (2 * box_padding),
                instruction_rect.height + (2 * box_padding)
            )
            pygame.draw.rect(self.display_surface, COLORS['white'], box_rect, 0, 8)
            self.display_surface.blit(instruction_surf, instruction_rect)

        # Check input
        return self.input()


class ControlsScreen:
    def __init__(self, fonts, bg_image):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.bg_image = bg_image
        self.active = True

        # Title text at top
        self.title_text = "Controls"
        self.title_y = 100

        # Text box for controls
        self.box_width = WINDOW_WIDTH * 0.7
        self.box_height = WINDOW_HEIGHT * 0.5
        self.box_x = (WINDOW_WIDTH - self.box_width) / 2
        self.box_y = WINDOW_HEIGHT * 0.25

        # Controls content (moved from title screen right box)
        self.controls_content = [
            "Navigate the character with the arrow keys.",
            "Interact with characters using the SPACE bar.",
            "Check the progress menu with ENTER. This will access the current practices and drug substance.",
            "ENTER will return you to the main game.",
            "Make choices that improve the supply chain, patient care, and protect the environment. Changes will show up in the progress menu",
            "Once the benefits of the medicine outweigh the negative impacts the game will conclude."
        ]

        # Return button
        self.button_width = 200
        self.button_height = 50
        self.return_button = {
            'rect': pygame.FRect((WINDOW_WIDTH - self.button_width) / 2, WINDOW_HEIGHT - 120, self.button_width, self.button_height),
            'text': 'Return',
            'color': COLORS['fire']
        }

    def draw_text_box(self, x, y, width, height, content):
        """Draw a text box with background and content"""
        # Background
        box_rect = pygame.FRect(x, y, width, height)
        pygame.draw.rect(self.display_surface, COLORS['gray'], box_rect, 0, 10)
        pygame.draw.rect(self.display_surface, COLORS['white'], box_rect, 3, 10)

        # Combine all content into one paragraph
        paragraph = ' '.join(line for line in content if line)

        # Content with text wrapping
        padding = 15
        line_height = 30
        max_text_width = width - (2 * padding)

        # Split text into words and wrap them
        words = paragraph.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            test_surf = self.fonts['title_subtext'].render(test_line, False, COLORS['white'])

            if test_surf.get_width() <= max_text_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]

        if current_line:
            lines.append(' '.join(current_line))

        # Calculate total text height and center it vertically
        total_text_height = len(lines) * line_height
        start_y = y + (height - total_text_height) / 2

        # Draw the wrapped lines
        for i, line in enumerate(lines):
            text_surf = self.fonts['title_subtext'].render(line, False, COLORS['white'])
            text_rect = text_surf.get_frect(centerx=x + width / 2, top=start_y + i * line_height)
            self.display_surface.blit(text_surf, text_rect)

    def input(self):
        """Check for space bar to return"""
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            self.active = False
            return True
        return False

    def update(self, dt):
        """Update and draw the controls screen"""
        if not self.active:
            return False

        # Draw background
        self.display_surface.blit(self.bg_image, (0, 0))

        # Draw title
        title_surf = self.fonts['title_big'].render(self.title_text, False, COLORS['white'])
        title_surf = pygame.transform.scale2x(title_surf)
        title_rect = title_surf.get_frect(centerx=WINDOW_WIDTH / 2, top=self.title_y)

        # Add shadow for title
        shadow_surf = self.fonts['title_big'].render(self.title_text, False, COLORS['black'])
        shadow_surf = pygame.transform.scale2x(shadow_surf)
        shadow_rect = shadow_surf.get_frect(centerx=WINDOW_WIDTH / 2 + 3, top=self.title_y + 3)
        self.display_surface.blit(shadow_surf, shadow_rect)
        self.display_surface.blit(title_surf, title_rect)

        # Draw text box
        self.draw_text_box(
            self.box_x,
            self.box_y,
            self.box_width,
            self.box_height,
            self.controls_content
        )

        # Draw return button
        rect = self.return_button['rect']

        # Button always highlighted since it's the only option
        button_color = COLORS['white']
        pygame.draw.rect(self.display_surface, button_color, rect, 0, 10)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 3, 10)

        text_color = self.return_button['color']
        text_surf = self.fonts['title_subtext'].render(self.return_button['text'], False, text_color)
        text_rect = text_surf.get_frect(center=rect.center)
        self.display_surface.blit(text_surf, text_rect)

        # Check input
        return self.input()


class CreditsScreen:
    def __init__(self, fonts, bg_image):
        self.display_surface = pygame.display.get_surface()
        self.fonts = fonts
        self.bg_image = bg_image
        self.active = True

        # Title text at top
        self.title_text = "Credits"
        self.title_y = 100

        # Text box for credits
        self.box_width = WINDOW_WIDTH * 0.7
        self.box_height = WINDOW_HEIGHT * 0.5
        self.box_x = (WINDOW_WIDTH - self.box_width) / 2
        self.box_y = WINDOW_HEIGHT * 0.25

        # Credits content
        self.credits_content = [
            "TransPharm is an EU-Funded project promoting the transformation towards a sustainable pharmaceutical sector (https://transforming-pharma.eu/)",
            "",
            "Created using Pygame. Game mechanics based on a tutorial by https://www.youtube.com/@ClearCode at https://github.com/clear-code-projects/Python-Monsters",
            "",
            "Character animations from Universal LPC Spritesheet Generator (https://liberatedpixelcup.github.io/ Universal-LPC-Spritesheet-Character-Generator)",
            "Artists: Barbara Riviera, Benjamin K. Smith (BenCreating), bluecarrot16, Charles Sanchez (CharlesGabriel), DarkwallLKE, drjamgo@hotmail.com, Durrani, Eliza Wyatt (ElizaWy), Evert, Fabzy, JaidynReiman, Joe White, Johannes Sjölund (wulax), kcilds/Rocetti/Eredah, laetissima, Lanea Zimmerman (Sharm), Luke Mehl, Mandi Paugh, Manuel Riecke (MrBeast), Matthew Krohn (makrohn), MuffinElZangano, Nila122, Nyom, Pierre Vigier (pvigier), Stephen Challener (Redshrike), Thane Brimhall (pennomi), thecilekli, TheraHedwig, William.Thompsonj",
            "Creative Commons Licenses: CC0, CC-BY, CC-BY 3.0, CC-BY 3.0+, CC-BY 4.0, CC-BY-SA 3.0, GPL 2.0, GPL 3.0, OGA-BY 3.0, OGA-BY 3.0+",
            "",
            "World graphics from FisherG (https://opengameart.org/content/12x12-city-tiles-top-down, @TheFish523)",
            "",
            "Water animations from Scarloxy (https://scarloxy.itch.io/mpwsp01)",
            ""
        ]

        # Return button
        self.button_width = 200
        self.button_height = 50
        self.return_button = {
            'rect': pygame.FRect((WINDOW_WIDTH - self.button_width) / 2, WINDOW_HEIGHT - 120, self.button_width, self.button_height),
            'text': 'Return',
            'color': COLORS['fire']
        }

        # Scrolling text setup
        self.scroll_y_offset = 0
        self.scroll_speed = 30  # pixels per second
        self.line_height = 30
        self.padding = 15
        self.max_text_width = self.box_width - (2 * self.padding)

        # Pre-render all wrapped lines to a surface
        self.text_surface = self._create_text_surface()

    def _create_text_surface(self):
        """Create a surface with all the wrapped text pre-rendered"""
        # First, wrap all text and determine total height needed
        all_wrapped_lines = []

        for line in self.credits_content:
            if not line:  # Empty line
                all_wrapped_lines.append(None)  # Marker for empty line
                continue

            # Split long lines into multiple wrapped lines
            words = line.split(' ')
            wrapped_lines = []
            current_line = []

            for word in words:
                test_line = ' '.join(current_line + [word])
                test_surf = self.fonts['title_subtext'].render(test_line, False, COLORS['white'])

                if test_surf.get_width() <= self.max_text_width:
                    current_line.append(word)
                else:
                    if current_line:
                        wrapped_lines.append(' '.join(current_line))
                    current_line = [word]

            if current_line:
                wrapped_lines.append(' '.join(current_line))

            all_wrapped_lines.extend(wrapped_lines)

        # Add some blank lines at the end for smooth loop
        all_wrapped_lines.extend([None] * 5)

        # Calculate total height needed
        total_height = len(all_wrapped_lines) * self.line_height + self.box_height

        # Create a surface to hold all text
        text_surface = pygame.Surface((int(self.box_width), int(total_height)), pygame.SRCALPHA)

        # Render all lines onto the surface
        current_y = 0
        for wrapped_line in all_wrapped_lines:
            if wrapped_line is None:  # Empty line
                current_y += self.line_height
                continue

            text_surf = self.fonts['title_subtext'].render(wrapped_line, False, COLORS['white'])
            text_rect = text_surf.get_frect(centerx=self.box_width / 2, top=current_y)
            text_surface.blit(text_surf, text_rect)
            current_y += self.line_height

        return text_surface

    def draw_scrolling_text_box(self, x, y, width, height):
        """Draw a text box with scrolling content that loops seamlessly"""
        # Draw background box
        box_rect = pygame.FRect(x, y, width, height)
        pygame.draw.rect(self.display_surface, COLORS['gray'], box_rect, 0, 10)
        pygame.draw.rect(self.display_surface, COLORS['white'], box_rect, 3, 10)

        # Create a clipping rect for the text area (inside padding)
        clip_rect = pygame.Rect(
            int(x + self.padding),
            int(y + self.padding),
            int(width - 2 * self.padding),
            int(height - 2 * self.padding)
        )

        # Set clipping region
        self.display_surface.set_clip(clip_rect)

        # Calculate the source rect (what part of text_surface to show)
        source_y = int(self.scroll_y_offset)
        dest_x = int(x + self.padding)
        dest_y = int(y + self.padding)

        # Calculate the content height (total height minus the extra padding at the end)
        content_height = self.text_surface.get_height() - self.box_height

        # Blit the visible portion of the text
        self.display_surface.blit(
            self.text_surface,
            (dest_x, dest_y),
            (0, source_y, int(width - 2 * self.padding), int(height - 2 * self.padding))
        )

        # If we're near the end, also blit the beginning to create seamless loop
        if source_y + (height - 2 * self.padding) > content_height:
            # Calculate how much of the beginning we need to show
            overflow = source_y + int(height - 2 * self.padding) - content_height

            # Blit the beginning of the text below the end
            self.display_surface.blit(
                self.text_surface,
                (dest_x, dest_y + content_height - source_y),
                (0, 0, int(width - 2 * self.padding), overflow)
            )

        # Reset clipping
        self.display_surface.set_clip(None)

    def input(self):
        """Check for space bar to return"""
        keys = pygame.key.get_just_pressed()
        if keys[pygame.K_SPACE]:
            self.active = False
            return True
        return False

    def update(self, dt):
        """Update and draw the credits screen"""
        if not self.active:
            return False

        # Update scroll position (dt is already in seconds)
        self.scroll_y_offset += self.scroll_speed * dt

        # Loop the scroll seamlessly when it reaches the end
        content_height = self.text_surface.get_height() - self.box_height
        if self.scroll_y_offset >= content_height:
            self.scroll_y_offset = self.scroll_y_offset - content_height

        # Draw background
        self.display_surface.blit(self.bg_image, (0, 0))

        # Draw title
        title_surf = self.fonts['title_big'].render(self.title_text, False, COLORS['white'])
        title_surf = pygame.transform.scale2x(title_surf)
        title_rect = title_surf.get_frect(centerx=WINDOW_WIDTH / 2, top=self.title_y)

        # Add shadow for title
        shadow_surf = self.fonts['title_big'].render(self.title_text, False, COLORS['black'])
        shadow_surf = pygame.transform.scale2x(shadow_surf)
        shadow_rect = shadow_surf.get_frect(centerx=WINDOW_WIDTH / 2 + 3, top=self.title_y + 3)
        self.display_surface.blit(shadow_surf, shadow_rect)
        self.display_surface.blit(title_surf, title_rect)

        # Draw scrolling text box
        self.draw_scrolling_text_box(
            self.box_x,
            self.box_y,
            self.box_width,
            self.box_height
        )

        # Draw return button
        rect = self.return_button['rect']

        # Button always highlighted since it's the only option
        button_color = COLORS['white']
        pygame.draw.rect(self.display_surface, button_color, rect, 0, 10)
        pygame.draw.rect(self.display_surface, COLORS['white'], rect, 3, 10)

        text_color = self.return_button['color']
        text_surf = self.fonts['title_subtext'].render(self.return_button['text'], False, text_color)
        text_rect = text_surf.get_frect(center=rect.center)
        self.display_surface.blit(text_surf, text_rect)

        # Check input
        return self.input()