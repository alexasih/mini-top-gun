# Import pygame module
import random
import pygame

# import key coordinates
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# set constant width and height of screen
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# define Player object extending sprite (2D representation of something on screen)
# surface drawn is now attribute of player
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        # Icon Creator: https://www.flaticon.com/authors/dooder
        self.surface = pygame.image.load("my_plane.png").convert()
        self.surface = pygame.transform.scale(self.surface, (60, 60))
        self.surface.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surface.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        # Icon Creator: https://www.flaticon.com/authors/flat-icons
        self.surface = pygame.image.load("enemy.png").convert()
        self.surface = pygame.transform.scale(self.surface, (20, 20))
        self.surface.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surface.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # move sprite based on speed
    # remove sprite after passing left edge of screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# cloud object with image
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surface = pygame.image.load("cloud.png").convert()
        self.surface.set_colorkey((0, 0, 0), RLEACCEL)
        # start pos random
        self.rect = self.surface.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
    
    # move cloud on constant speed, remove after passing left edge of screen
    def update(self):
        self.rect.move_ip(-5, 0)
        if self.rect.right < 0:
            self.kill()
    
# setup sounds
pygame.mixer.init()

# Initialize pygame
pygame.init()

# setup clock for decent framerate
clock = pygame.time.Clock()

# create screen object of size SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# create custom event to add new enemy
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# instantiate player
my_player = Player()

# create sprite group, an object holding group of Sprite objects to hold enemy sprites
# used for collision detection and position updates
# all_sprites to render
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(my_player)

# background music
# Sound source: http://ccmixter.org/files/Apoxode/59262
# License: https://creativecommons.org/licenses/by/3.0/
pygame.mixer.music.load("Apoxode_-_Electric_1.mp3")
pygame.mixer.music.play(loops=-1)

# sound files
# sound source: Jon Fincher
up_sound = pygame.mixer.Sound("Rising_putter.ogg")
down_sound = pygame.mixer.Sound("Falling_putter.ogg")
collision_sound = pygame.mixer.Sound("Collision.ogg")

# Set base volume
up_sound.set_volume(0.5)
down_sound.set_volume(0.5)
collision_sound.set_volume(0.5)

# keep main loop running aka variable to keep game running
running = True

# Main loop
while running:
    # look at every event in queue
    for event in pygame.event.get():
        # if user hits a key
        if event.type == KEYDOWN:
            # check if escape key to stop loop
            if event.key == K_ESCAPE:
                running = False

        # if user closes window, stop loop also
        elif event.type == QUIT:
            running = False

        # add new enemy
        elif event.type == ADDENEMY:
            # create new enemy, add to sprite group
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

        # add new cloud
        elif event.type == ADDCLOUD:
            # create new cloud and add to sprite group
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

    # get keys pressed, check for user input
    pressed_keys = pygame.key.get_pressed()

    # update my player sprite based on user key presses
    my_player.update(pressed_keys)

    # update enemy position and cloud pos every frame
    enemies.update()
    clouds.update()

    # make screen white
    screen.fill((135, 206, 250))

    # draw all sprites
    for charSprite in all_sprites:
        screen.blit(charSprite.surface, charSprite.rect)

    # check if any enemies collided with player
    if pygame.sprite.spritecollideany(my_player, enemies):
        # remove player and stop loop -> game ends
        my_player.kill()

        # stop moving sounds, play collision sound
        up_sound.stop()
        down_sound.stop()
        collision_sound.play()

        running = False

    # update display
    pygame.display.flip()

    # ensure program has rate of 30 frames per second
    clock.tick(30)

# stop and quit mixer
pygame.mixer.music.stop()
pygame.mixer.quit()