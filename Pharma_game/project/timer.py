import random
from pygame.time import get_ticks

class Timer:
    def __init__(self, duration, repeat=False, autostart=False, func=None, randomize=False, min_time=2000, max_time=6000):
        self.duration = duration
        self.repeat = repeat
        self.func = func
        self.randomize = randomize
        self.min_time = min_time
        self.max_time = max_time
        self.active = False
        self.start_time = 0

        if autostart:
            self.activate()

    def _set_duration(self):
        if self.randomize:
            self.duration = random.randint(self.min_time, self.max_time)

    def activate(self):
        self._set_duration()
        self.active = True
        self.start_time = get_ticks()

    def deactivate(self):
        self.active = False
        self.start_time = 0
        if self.repeat:
            self.activate()

    def update(self):
        if self.active:
            current_time = get_ticks()
            if current_time - self.start_time >= self.duration:
                if self.func:
                    self.func()
                self.deactivate()
