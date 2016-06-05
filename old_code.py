"""pastebin of sorts."""
class Machinegun(Pistol):
    """ fires burst of 3 bullets at a time. Inherits from pistol as its functionally similar"""
    def __init__(self, player):
        Pistol.__init__(self, player)
        self.images = []
        self.images.append(pygame.image.load("Resources/sprite_machinegun.png").convert_alpha())
        self.images.append(pygame.transform.flip(self.images[0], True, False)) # Flipped 
        self.image = self.images[0]

        self.min_fire_time = 2 # minimum time required to shoot
        self.clip_size = 12 # amount of ammo per clip
        self.clip_ammo = 12
        self.ammo_amount = 300
        self.reload_time = 100 
        self.firing = False # is the gun firing or not
        self._firing_time = 0 # working variable for burst fire

        self.rect = self.image.get_rect()
        self.fire_sound = pygame.mixer.Sound("Resources/machinegun_fire.wav")
        self.reload_sound = pygame.mixer.Sound("Resources/machinegun_reload.wav")

    def update(self):
        # Fire 3 times in quick succession. To do: fix similar soudning variables
        if self.fire_time >= self.min_fire_time:
            if self.state == 'firing':
                if self.firing == True:
                    if self._firing_time < 15:
                        if self._firing_time % 5 == 0:
                                if self.clip_ammo >= 1:
                                    self.clip_ammo +=- 1
                                    self.fire()
                        self._firing_time += 1
                    else:
                        self.firing = False
                        self._firing_time = 0
                        self.fire_time = 0

     
        Pistol.update(self)

    def use_weapon(self):
        self.firing = True