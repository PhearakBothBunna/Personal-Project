# Phearak Both Bunna
# Personal project 2020
# Reverse flappy bird game with new background and slightly different playing style
# Instead of the bird flying up when left clicking/mouse pressing, the bird goes in downward direction

import pygame
import random

pygame.init()

# Frame rate
clock = pygame.time.Clock()
fps = 80
# Game window
scr_w = 746
scr_h = 668
screen = pygame.display.set_mode((scr_w, scr_h))
pygame.display.set_caption("Reverse Flappy Bird")

# Load flappy bird images
bg = pygame.image.load("bg(fb).gif")
ground = pygame.image.load("ground.png")
button = pygame.image.load("restart.png")
# font for text
font = pygame.font.SysFont('Helvetica', 50)
white_color = (255, 255, 255)
# Variables of our game
score = 0
gr_scroll = 0
scroll_sp = 5
pipe_gap = 140
pipe_freq = 1700  # milli secs
flying = False
game_over = False
pass_pipe = False
last_pipe = pygame.time.get_ticks()


def restart_game():
    pipe_group.empty()
    flappyBird.rect.x = 100
    flappyBird.rect.y = int(scr_h / 2)
    score = 0
    return score


def write_text(text, font, text_color, x, y):
    txt = font.render(text, True, text_color)
    screen.blit(txt, (x, y))


class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img = pygame.image.load(f'bird{num}.png')
            self.images.append(img)

        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.clicked = False

    def update(self):
        if flying:
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < 550:
                self.rect.y -= int(self.vel)

        if not game_over:
            # bird jumping
            # Check for mouse clicking (exclude holding mouse)
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -7
            # Check for mouse release
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

            # Animation handler
            self.counter += 1
            flap_cooldown = 5

            if self.counter > flap_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images):
                    self.index = 0
            self.image = self.images[self.index]

            # Rotate the bird
            self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.images[self.index], -90)


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('pipe.png')
        self.rect = self.image.get_rect()
        # 1 is from the top & -1 is from bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(pipe_gap / 1.5)]
        if position == -1:
            self.rect.topleft = [x, y + int(pipe_gap / 1.5)]

    def update(self):
        self.rect.x -= scroll_sp
        # remove pipes after got out of screen
        if self.rect.right < 0:
            self.kill()


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = [x, y]

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        # Check to see if user click on restart button
        if self.rect.collidepoint(pos):
            # Check to see if there's a left-mouse click
            if pygame.mouse.get_pressed()[0] == 1:
                action = True

        screen.blit(self.image, (self.rect.x, self.rect.y))
        return action


bird_group = pygame.sprite.Group()
pipe_group = pygame.sprite.Group()

flappyBird = Bird(100, int(scr_h / 2))
bird_group.add(flappyBird)

# Restart button
restart_but = Button(scr_w / 2 - 50, scr_h / 2 - 100, button)

run = True
while run:
    clock.tick(fps)
    # Game background
    screen.blit(bg, (0, 0))

    # Bird
    bird_group.draw(screen)
    bird_group.update()
    # Pipe
    pipe_group.draw(screen)

    # Moving ground
    screen.blit(ground, (gr_scroll, 340))

    # Check for scores
    if len(pipe_group) > 0:
        if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < pipe_group.sprites()[0].rect.right \
                and pass_pipe == False:
            pass_pipe = True
        if pass_pipe == True:
            if bird_group.sprites()[0].rect.left > pipe_group.sprites()[0].rect.right:
                score += 1
                pass_pipe = False
    write_text(str(score), font, white_color, int(scr_w / 2), 22)
    # Check for collisions
    if pygame.sprite.groupcollide(bird_group, pipe_group, False, False) or flappyBird.rect.top < 0:
        game_over = True

    # Check when the bird hits the ground
    if flappyBird.rect.bottom >= 540:
        game_over = True
        flying = False

    if game_over == False and flying == True:
        time_cur = pygame.time.get_ticks()
        if time_cur - last_pipe > pipe_freq:
            pipe_height = random.randint(-50, 50)
            btm_pipe = Pipe(scr_w, int(scr_h / 2) + pipe_height, -1)
            top_pipe = Pipe(scr_w, int(scr_h / 2) + pipe_height, 1)
            pipe_group.add(btm_pipe)
            pipe_group.add(top_pipe)
            last_pipe = time_cur
        # Groud scrolling to the left
        gr_scroll -= scroll_sp
        if abs(gr_scroll) > 100:
            gr_scroll = 0
        pipe_group.update()

    # Checking for game over to restart
    if game_over:
        write_text("Better luck next time...", font, (255, 0, 0), 200, 300)
        if restart_but.draw():
            game_over = False
            score = restart_game()

    # Exit the game/close game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN and flying == False and game_over == False:
            flying = True

    pygame.display.update()

pygame.quit()
