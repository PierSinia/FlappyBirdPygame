import pygame
import random
from os import *

WIDTH = 700 # breedte van het scherm
HEIGHT = 550 # hoogte van het scherm
FPS = 60 # Frames per Second
gap = 150 # De ruimte tussen de buizen

# de kleuren
white = (255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
groundcolour = (238,232,170)
blue = (0, 190, 255)
yellow = (255, 255, 0)

# pygame initialiseren en een scherm maken
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy")
clock = pygame.time.Clock()

# De locatie van de img folder en de snd folder
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')

# De geluiden
hit_sound = pygame.mixer.Sound(path.join(snd_dir, 'hit-2.wav'))
score_sound = pygame.mixer.Sound(path.join(snd_dir, 'score-2.wav'))
flap_sound = pygame.mixer.Sound(path.join(snd_dir, 'flap.wav'))

# De afbeeldingen
background = pygame.image.load(path.join(img_dir, "background2.png")).convert()
ground_img = pygame.image.load(path.join(img_dir, "ground.png")).convert()
player_img = pygame.image.load(path.join(img_dir, "flappybird.png")).convert()

# Draw text functie
def draw_text(surf, text, size, x, y, color):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# De speler sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        self.score = 0
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 3, HEIGHT / 2)

    def update(self):
        global game_over
        self.speedy = 0
        self.gravity = (9.8 * self.rect.y) / 1500
        key = pygame.key.get_pressed()  # Lijst die alle toetsen aangeeft waar op gedrukt word
        self.speedy += self.gravity
        self.speedy += 6.5
        if key[pygame.K_SPACE]:
            self.speedy -= 15.3
            flap_sound.play()

        self.rect.y += self.speedy

        if self.rect.y < 0 and self.rect.right == upper_pipe.rect.right:
            game_over = True
            hit_sound.play()

        self.hit = pygame.sprite.spritecollide(player, obstacles, False)


class Ground(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((WIDTH, 20))
        self.image.fill(groundcolour)
        self.rect = self.image.get_rect()
        self.rect.y = HEIGHT - 20
        self.rect.x = 0

class Upper_pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.upper_pipe_height = random.randrange(0, HEIGHT - gap)
        self.upper_pipe_width = 69
        self.upper_pipe_size = (self.upper_pipe_width, self.upper_pipe_height)
        self.image = pygame.Surface(self.upper_pipe_size)
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH -100
        self.rect.y = 0

    def update(self):

        self.speedx = 0

        self.speedx -= 4

        if self.rect.right < 0:
            self.rect.left = WIDTH

        if self.rect.left == WIDTH:
            self.upper_pipe_height = random.randrange(0, HEIGHT - gap)

            self.upper_pipe_size = (self.upper_pipe_width, self.upper_pipe_height)
            self.image = pygame.Surface(self.upper_pipe_size)
            self.image.fill(green)


        self.rect.x += self.speedx

        def create_new_pipe(self):
            if self.rect.center == WIDTH / 2:
                create_new_pipe = True

            if create_new_pipe == True:
                obstacles.copy()


class Lower_pipe(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((upper_pipe.upper_pipe_width, HEIGHT - upper_pipe.upper_pipe_height + gap))
        self.image.fill(green)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH - 100
        self.rect.y = upper_pipe.upper_pipe_height + gap

    def update(self):
        self.speedx = 0

        self.speedx -= 4

        if self.rect.right < 0:
            self.rect.left = WIDTH

            self.rect.y = upper_pipe.upper_pipe_height + gap

        self.rect.x += self.speedx


def show_go_screen():
    backgroundrect = background.get_rect()  # vraag afmetingen van het bordplaatje op
    screen.blit( background, backgroundrect )  # teken het bord
    draw_text(screen, "Flappy!", 64, WIDTH / 2, HEIGHT / 4, black)
    draw_text(screen, "Space to go up", 28, WIDTH /2,  HEIGHT /4 + 100, black)
    draw_text(screen, "Press a key to start" , 22, WIDTH /2, HEIGHT /4 + 200, black)
    draw_text(screen, "Score: {}".format(player.score) , 30, WIDTH /2, HEIGHT/ 4 + 300 , black)
    pygame.display.flip()
    waiting = True

    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYUP:
                waiting = False

all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
player = Player()
upper_pipe = Upper_pipe()
lower_pipe = Lower_pipe()
ground = Ground()
all_sprites.add( player, upper_pipe, lower_pipe, ground )
obstacles.add( upper_pipe, lower_pipe, ground )

# Game loop
game_over = True
running = True
while running:
    global hit
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        obstacles = pygame.sprite.Group()
        player = Player()
        upper_pipe = Upper_pipe()
        lower_pipe = Lower_pipe()
        ground = Ground()
        all_sprites.add( player, upper_pipe, lower_pipe, ground )
        obstacles.add( upper_pipe, lower_pipe, ground )
        player.score = 0

    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    if upper_pipe.rect.right and lower_pipe.rect.right == player.rect.left:
        player.score += 1
        score_sound.play()

    # Update
    all_sprites.update()

    # Draw / render
    backgroundrect = background.get_rect()  # vraag afmetingen van het bordplaatje op
    screen.blit(background, backgroundrect)  # teken het bord

    all_sprites.draw(screen)

    draw_text(screen, "Score: {}".format(player.score), 30, 80, 20, black)

    if player.hit:
        game_over = True
        hit_sound.play()

    # Scherm updaten
    pygame.display.flip()

pygame.quit()
quit()
