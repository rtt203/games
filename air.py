import sys, os, pygame, random
from pygame.locals import *
from os import path
x_coord = 1
y_coord = 320
x_speed = 0
y_speed = 0
score = 1000
shag = 0
go1 = 0
go2 = 0





def init_window():
    pygame.init()
    window = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption('Future-Z')


def load_data(name, colorkey = None):
    fullname = os.path.join('image', name)
    image = pygame.image.load(fullname)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


def draw_background():
    screen = pygame.display.get_surface()
    back, back_rect = load_data("sky.jpg")
    screen.blit(back, (0, 0))
    pygame.display.flip()
    return back




class Skything(pygame.sprite.Sprite):
    def __init__(self, img, cX, cY):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_data(img, -1)
        screen = pygame.display.get_surface()
        self.area = screen.get_rect()
        self.rect.x = cX
        self.rect.y = cY


class Our_air(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "1.png", cX, cY)


class Enemy_air(Skything):
    def __init__(self, cX, cY):
        Skything.__init__(self, "2.png", cX, cY)





def input (events):
    global x_coord, y_coord, x_speed, y_speed, life
    for event in events:
        if (event.type == QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: x_speed = -2
            if event.key == pygame.K_RIGHT: x_speed = 2
            if event.key == pygame.K_UP: y_speed = -2
            if event.key == pygame.K_DOWN: y_speed = 2
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: x_speed = 0
            if event.key == pygame.K_RIGHT: x_speed = 0
            if event.key == pygame.K_UP: y_speed = 0
            if event.key == pygame.K_DOWN: y_speed = 0
    x_coord = x_coord + x_speed
    y_coord = y_coord + y_speed
    if (x_coord < 0): x_coord = 0
    if (x_coord > 1100): x_coord = 1100
    if (y_coord < 0): y_coord = 0
    if (y_coord > 500): y_coord = 500


def action(bk):
    pygame.mixer.music.load('nir.mp3')
    pygame.mixer.music.play(-1)
    global x_coord, y_coord, score, shag, go1, go2
    screen = pygame.display.get_surface()
    airplane = Our_air(1, 320)
    enemy_air = Enemy_air(1280, 225)
    enemy_air2 = Enemy_air(1280,0)
    en_air = []
    en_air.append(enemy_air)
    en_air.append(enemy_air2)
    air = []
    air.append(airplane)
    enemy_airs = pygame.sprite.RenderPlain(en_air)
    our_airplane = pygame.sprite.RenderPlain(air)
    timer = pygame.time.Clock()
    while 1:
        timer.tick(200)
        input(pygame.event.get())
        blocks_hit_list = pygame.sprite.spritecollide(airplane, enemy_airs, False)
        if len(blocks_hit_list) > 0:
            score -= len(blocks_hit_list)
            enemy_airs.draw(screen)
            our_airplane.draw(screen)
            if (score < 1):
                pygame.quit()
                sys.exit(0)
        airplane.rect.x = x_coord
        airplane.rect.y = y_coord
        enemy_air.rect.x = enemy_air.rect.x - 1
        enemy_air2.rect.x = enemy_air2.rect.x - 1
        if (enemy_air.rect.x < -300):
            enemy_air.rect.x = 1280
            enemy_air.rect.y = 220
        if (enemy_air2.rect.x < -300):
            enemy_air2.rect.x = 1280
            enemy_air.rect.y = 15
        if (shag > 70):
            shag = 0
            go1 = random.randint(-2, 2)
            go2 = random.randint(-2, 2)
        enemy_air.rect.y += go1
        enemy_air2.rect.y += go2
        shag += 1
        screen.blit(bk, (0, 0))
        font = pygame.font.Font(None, 25)
        white = (255, 255, 255)
        life = int(score / 10)
        text = font.render("Health Point: " + str(life), True, white)
        screen.blit(text, [10, 10])
        enemy_airs.update()
        our_airplane.update()
        enemy_airs.draw(screen)
        our_airplane.draw(screen)
        pygame.display.flip()


def main():
    init_window()
    bk = draw_background()
    action(bk)


main()