import pygame
from pygame import mixer
import time
import random
import os

pygame.init(); mixer.init()
screen_width, screen_height = (900, 700)
fps = 40
img_width, img_height = (70, 60)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Legend of Zelda: Level 2")
mixer.music.load("level3_theme.mp3")
mixer.music.play()

max_beams = 5
velocity = 3; beam_velocity = 5
bg_img = pygame.transform.scale(pygame.image.load("level2_bg.png"), (screen_width, screen_height))
link = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("link.png"), (img_width, img_height)), 0)
link_rect = pygame.Rect(10,10, img_width,img_height)
blue = (0, 0, 255); red = (255, 0, 0); green = (0, 255, 0)
running = True; score = 0

font1 = pygame.font.SysFont('freesansbold.ttf', 32)
gameOver = font1.render('Game Over!', True, red)
gameOver_rect = gameOver.get_rect()
gameOver_rect.center = (screen_width // 2, screen_height // 2)
winner = font1.render('You Win!', True, green)
winner_rect = winner.get_rect()
winner_rect.center = (screen_width // 2, screen_height // 2)

lev_3_portal = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("oB4Td7TviwwZqSH3of6xN-1200-80.png"), (200, 100)), 0)
lev_3_portal_rect = pygame.Rect(screen_width//2, screen_height - 100, img_width,img_height)

class Link:
    beam_damage = 10
    health = 1000
    def take_damage(damage):
        Link.health -= damage
        if Link.health <= 0:
            Link.die()

    def attack_up():
        link_attack_up = pygame.transform.scale(pygame.image.load("link_attack_up.png"), (img_width, img_height))
        draw_normal(link_beams_right, link_beams_left, link_beams_up, link_beams_down)
        screen.blit(link_attack_up, (link_rect.x, link_rect.y))
        pygame.display.update()
        time.sleep(0.1)

    def attack_down():
        link_attack_down = pygame.transform.scale(pygame.image.load("link_attack_down.png"), (img_width, img_height))
        draw_normal(link_beams_right, link_beams_left, link_beams_up, link_beams_down)
        screen.blit(link_attack_down, (link_rect.x, link_rect.y))
        pygame.display.update()
        time.sleep(0.1)

    def attack_left():
        link_attack_left = pygame.transform.scale(pygame.image.load("link_attack_left.png"), (img_width, img_height))
        draw_normal(link_beams_right, link_beams_left, link_beams_up, link_beams_down)
        screen.blit(link_attack_left, (link_rect.x, link_rect.y))
        pygame.display.update()
        time.sleep(0.1)

    def attack_right():
        link_attack_right = pygame.transform.scale(pygame.image.load("link_attack_right.png"), (img_width, img_height))
        draw_normal(link_beams_right, link_beams_left, link_beams_up, link_beams_down)
        screen.blit(link_attack_right, (link_rect.x, link_rect.y))
        pygame.display.update()
        time.sleep(0.1)

    def die():
        link_dead = pygame.transform.scale(pygame.image.load("dead.png"), (0, 0))
        screen.blit(link_dead, (link_rect.x, link_rect.y))
        screen.blit(gameOver, gameOver_rect)
        font2 = pygame.font.SysFont('freesansbold.ttf', 55)
        SCORE = font2.render('Score: ' + str(score), True, blue)
        SCORERect = SCORE.get_rect()
        SCORERect.center = (screen_width // 2, screen_height // 2 + 33)
        screen.blit(SCORE, SCORERect)
        pygame.display.update()
        pygame.mixer.music.stop()
        time.sleep(2)
        pygame.display.quit()
        os.system("python zelda_level_2.py")

    def win():
        font2 = pygame.font.SysFont('freesansbold.ttf', 55)
        SCORE = font2.render('Score: ' + str(score), True, blue)
        SCORERect = SCORE.get_rect()
        SCORERect.center = (screen_width // 2, screen_height // 2 + 33)
        screen.blit(winner, winner_rect)
        screen.blit(SCORE, SCORERect)
        pygame.display.update()
        pygame.mixer.music.stop()
        time.sleep(2)
        pygame.display.quit()
        os.system("python zelda_level_3.py")

class Enemy:
    num_enemies = 0
    def __init__(self, enemy_name, enemy, enemy_rect, enemy_positions, enemy_velocity, health, enemy_damage):
        self.enemy_name = enemy_name
        self.enemy = enemy
        self.enemy_rect = enemy_rect
        self.enemy_positions = enemy_positions
        self.enemy_velocity = enemy_velocity
        self.health = health
        self.enemy_damage = enemy_damage
        Enemy.num_enemies += 1
    
    def get_enemy_name(self):
        return self.enemy_name

    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.modify_enemy(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("dead.png"), (0,0)), 0))
            self.modify_enemy_rect(pygame.Rect(screen_width + 10,screen_height + 10, img_width,img_height))
            self.enemy_velocity = 0
            Enemy.num_enemies -= 1

    def give_damage(self):
        return self.enemy_damage

    def is_killed(self):
        return self.health <= 0

    def modify_enemy(self, enemy_new):
        self.enemy = enemy_new
    
    def modify_enemy_rect(self, new_rect):
        self.enemy_rect = new_rect

    def get_enemy_health(self):
        return self.health

    def get_enemy(self):
        return self.enemy
    
    def get_enemy_rect(self):
        return self.enemy_rect

    def get_enemy_x(self):
        return self.enemy_rect.x

    def get_enemy_y(self):
        return self.enemy_rect.y

    def move_left(self):
        self.modify_enemy(self.enemy_positions[0])
        if self.enemy_rect.x > 0:
            self.enemy_rect.x -= self.enemy_velocity
        else:
            self.move_right()

    def move_right(self):
        self.modify_enemy(self.enemy_positions[1])
        if self.enemy_rect.x < screen_width:
            self.enemy_rect.x += self.enemy_velocity
        else:
            self.move_left()

    def move_up(self):
        self.modify_enemy(self.enemy_positions[2])
        if self.enemy_rect.y > 0:
            self.enemy_rect.y -= self.enemy_velocity
        else:
            self.move_down()

    def move_down(self):
        self.modify_enemy(self.enemy_positions[3])
        if self.enemy_rect.y < screen_height:
           self.enemy_rect.y += self.enemy_velocity
        else:
            self.move_up()

    def attack_link(self):
        if self.enemy_rect.x >= link_rect.x + img_width:
            self.move_left()
        if self.enemy_rect.y <= link_rect.y:
            self.move_down()
        if self.enemy_rect.x <= link_rect.x + img_width:
            self.move_right()
        if self.enemy_rect.y >= link_rect.y:
            self.move_up()

randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
bokoblin_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_left.png"), (img_width, img_height)), 0)
bokoblin_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_right.png"), (img_width, img_height)), 0)
bokoblin_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_up.png"), (img_width, img_height)), 0)
bokoblin_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_down.png"), (img_width, img_height)), 0)
bokoblin_pos = [bokoblin_left, bokoblin_right, bokoblin_up, bokoblin_down]
bokoblin1 = Enemy("bokoblin", bokoblin_down, pygame.Rect(randx,randy, img_width,img_height), bokoblin_pos, 1, 35, 10)
randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
bokoblin2 = Enemy("bokoblin", bokoblin_down, pygame.Rect(randx,randy, img_width,img_height), bokoblin_pos, 1, 35, 10)

randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
moblin_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_left.png"), (img_width, img_height)), 0)
moblin_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_right.png"), (img_width, img_height)), 0)
moblin_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_up.png"), (img_width, img_height)), 0)
moblin_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_down.png"), (img_width, img_height)), 0)
moblin_pos = [moblin_left, moblin_right, moblin_up, moblin_down]
moblin1 = Enemy("moblin", moblin_down, pygame.Rect(randx,randy, img_width,img_height), moblin_pos, 1.5, 80, 25)
randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
moblin2 = Enemy("moblin", moblin_down, pygame.Rect(randx,randy, img_width,img_height), moblin_pos, 1.5, 80, 25)
randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
moblin3 = Enemy("moblin", moblin_down, pygame.Rect(randx,randy, img_width,img_height), moblin_pos, 1.5, 80, 25)

def draw(link_beams_right, link_beams_left, link_beams_up, link_beams_down, c):
    screen.blit(bg_img, (0, 0))
    if c == 0:
        screen.blit(link, (link_rect.x, link_rect.y))
    screen.blit(bokoblin1.get_enemy(), (bokoblin1.get_enemy_x(), bokoblin1.get_enemy_y()))
    screen.blit(bokoblin2.get_enemy(), (bokoblin2.get_enemy_x(), bokoblin2.get_enemy_y()))
    screen.blit(moblin1.get_enemy(), (moblin1.get_enemy_x(), moblin1.get_enemy_y()))
    screen.blit(moblin2.get_enemy(), (moblin2.get_enemy_x(), moblin2.get_enemy_y()))
    screen.blit(moblin3.get_enemy(), (moblin3.get_enemy_x(), moblin3.get_enemy_y()))
    font1 = pygame.font.SysFont('freesansbold.ttf', 32)
    HEALTH = font1.render('Health: ' + str(Link.health), True, green)
    HEALTH_rect = HEALTH.get_rect()
    HEALTH_rect.center = (screen_width // 2, 11)
    screen.blit(HEALTH, HEALTH_rect)
    screen.blit(lev_3_portal, lev_3_portal_rect)
    font2 = pygame.font.SysFont('freesansbold.ttf', 20)
    OCTHEALTH1 = font2.render(str(bokoblin1.get_enemy_health()), True, red)
    OCTHEALTH1_rect = OCTHEALTH1.get_rect()
    OCTHEALTH1_rect.center = (bokoblin1.get_enemy_x() + img_width//2, bokoblin1.get_enemy_y() - 5)
    screen.blit(OCTHEALTH1, OCTHEALTH1_rect)
    OCTHEALTH2 = font2.render(str(bokoblin2.get_enemy_health()), True, red)
    OCTHEALTH2_rect = OCTHEALTH2.get_rect()
    OCTHEALTH2_rect.center = (bokoblin2.get_enemy_x() + img_width//2, bokoblin2.get_enemy_y() - 5)
    screen.blit(OCTHEALTH2, OCTHEALTH2_rect)
    OCTHEALTH3 = font2.render(str(moblin1.get_enemy_health()), True, red)
    OCTHEALTH3_rect = OCTHEALTH3.get_rect()
    OCTHEALTH3_rect.center = (moblin1.get_enemy_x() + img_width//2, moblin1.get_enemy_y() - 5)
    screen.blit(OCTHEALTH3, OCTHEALTH3_rect)
    OCTHEALTH4 = font2.render(str(moblin2.get_enemy_health()), True, red)
    OCTHEALTH4_rect = OCTHEALTH4.get_rect()
    OCTHEALTH4_rect.center = (moblin2.get_enemy_x() + img_width//2, moblin2.get_enemy_y() - 5)
    screen.blit(OCTHEALTH4, OCTHEALTH4_rect)
    BOKHEALTH = font2.render(str(moblin3.get_enemy_health()), True, red)
    BOKHEALTH_rect = BOKHEALTH.get_rect()
    BOKHEALTH_rect.center = (moblin3.get_enemy_x() + img_width//2, moblin3.get_enemy_y() - 5)
    screen.blit(BOKHEALTH, BOKHEALTH_rect)
    for beam in link_beams_right:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_left:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_up:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_down:
        pygame.draw.rect(screen, blue, beam) 
    pygame.display.update()
draw([], [], [], [], 0)

def draw_normal(link_beams_right, link_beams_left, link_beams_up, link_beams_down):
    screen.blit(bg_img, (0, 0))
    screen.blit(bokoblin1.get_enemy(), (bokoblin1.get_enemy_x(), bokoblin1.get_enemy_y()))
    screen.blit(bokoblin2.get_enemy(), (bokoblin2.get_enemy_x(), bokoblin2.get_enemy_y()))
    screen.blit(moblin1.get_enemy(), (moblin1.get_enemy_x(), moblin1.get_enemy_y()))
    screen.blit(moblin2.get_enemy(), (moblin2.get_enemy_x(), moblin2.get_enemy_y()))
    screen.blit(moblin3.get_enemy(), (moblin3.get_enemy_x(), moblin3.get_enemy_y()))
    font1 = pygame.font.SysFont('freesansbold.ttf', 32)
    HEALTH = font1.render('Health: ' + str(Link.health), True, green)
    HEALTH_rect = HEALTH.get_rect()
    HEALTH_rect.center = (screen_width // 2, 11)
    screen.blit(HEALTH, HEALTH_rect)
    screen.blit(lev_3_portal, lev_3_portal_rect)
    font2 = pygame.font.SysFont('freesansbold.ttf', 20)
    OCTHEALTH1 = font2.render(str(bokoblin1.get_enemy_health()), True, red)
    OCTHEALTH1_rect = OCTHEALTH1.get_rect()
    OCTHEALTH1_rect.center = (bokoblin1.get_enemy_x() + img_width//2, bokoblin1.get_enemy_y() - 5)
    screen.blit(OCTHEALTH1, OCTHEALTH1_rect)
    OCTHEALTH2 = font2.render(str(bokoblin2.get_enemy_health()), True, red)
    OCTHEALTH2_rect = OCTHEALTH2.get_rect()
    OCTHEALTH2_rect.center = (bokoblin2.get_enemy_x() + img_width//2, bokoblin2.get_enemy_y() - 5)
    screen.blit(OCTHEALTH2, OCTHEALTH2_rect)
    OCTHEALTH3 = font2.render(str(moblin1.get_enemy_health()), True, red)
    OCTHEALTH3_rect = OCTHEALTH3.get_rect()
    OCTHEALTH3_rect.center = (moblin1.get_enemy_x() + img_width//2, moblin1.get_enemy_y() - 5)
    screen.blit(OCTHEALTH3, OCTHEALTH3_rect)
    OCTHEALTH4 = font2.render(str(moblin2.get_enemy_health()), True, red)
    OCTHEALTH4_rect = OCTHEALTH4.get_rect()
    OCTHEALTH4_rect.center = (moblin2.get_enemy_x() + img_width//2, moblin2.get_enemy_y() - 5)
    screen.blit(OCTHEALTH4, OCTHEALTH4_rect)
    BOKHEALTH = font2.render(str(moblin3.get_enemy_health()), True, red)
    BOKHEALTH_rect = BOKHEALTH.get_rect()
    BOKHEALTH_rect.center = (moblin3.get_enemy_x() + img_width//2, moblin3.get_enemy_y() - 5)
    screen.blit(BOKHEALTH, BOKHEALTH_rect)
    for beam in link_beams_right:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_left:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_up:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_down:
        pygame.draw.rect(screen, blue, beam) 
    pygame.display.update()

def Link_move(k):
    if k[pygame.K_UP] and link_rect.y > 0:
        link_rect.y -= velocity
    if k[pygame.K_DOWN] and link_rect.y < screen_height - img_height:
        link_rect.y += velocity
    if k[pygame.K_LEFT] and link_rect.x > 0:
        link_rect.x -= velocity
    if k[pygame.K_RIGHT] and link_rect.x < screen_width - img_width:
        link_rect.x += velocity  
    if k[pygame.K_w]:
        Link.attack_up()
    if k[pygame.K_s]:
        Link.attack_down()
    if k[pygame.K_a]:
        Link.attack_left()
    if k[pygame.K_d]:
        Link.attack_right()
    for beam in link_beams_right:
        beam.x += beam_velocity
    for beam in link_beams_left:
        beam.x -= beam_velocity
    for beam in link_beams_up:
        beam.y -= beam_velocity
    for beam in link_beams_down:
        beam.y += beam_velocity

bokoblin_score = 5
moblin_score = 7
def Link_hits(enemy):
    global score
    for beam in link_beams_right:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_right.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
        if beam.x > screen_width:
            link_beams_right.remove(beam)
    for beam in link_beams_left:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_left.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
        if beam.x < 0:
            link_beams_left.remove(beam)
    for beam in link_beams_up:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_up.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
        if beam.y < 0:
            link_beams_up.remove(beam)
    for beam in link_beams_down:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_down.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
        if beam.y > screen_height:
            link_beams_down.remove(beam)

def Link_gets_hit(enemy):
    if link_rect.colliderect(enemy.get_enemy_rect()):
        Link.take_damage(enemy.give_damage())
        
link_beams_right = []
link_beams_left = []
link_beams_up = []
link_beams_down = []
while running:
    clock.tick(fps)
    beam_wid_hor, beam_hei_hor = 15, 8
    beam_wid_ver, beam_hei_ver = 8, 15
    c = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d and len(link_beams_right) < max_beams:
                    beam = pygame.Rect(link_rect.x + img_width//2,link_rect.y + img_height//2, beam_wid_hor,beam_hei_hor)
                    link_beams_right.append(beam)
                    c = 1
            if event.key == pygame.K_a and len(link_beams_left) < max_beams:
                    beam = pygame.Rect(link_rect.x - img_width//2,link_rect.y + img_height//2, beam_wid_hor,beam_hei_hor)
                    link_beams_left.append(beam)
                    c = 1
            if event.key == pygame.K_w and len(link_beams_up) < max_beams:
                    beam = pygame.Rect(link_rect.x + img_width//2,link_rect.y + img_height//2, beam_wid_ver,beam_hei_ver)
                    link_beams_up.append(beam)
                    c = 1
            if event.key == pygame.K_s and len(link_beams_down) < max_beams:
                    beam = pygame.Rect(link_rect.x + img_width//2,link_rect.y + img_height//2, beam_wid_ver,beam_hei_ver)
                    link_beams_down.append(beam)
                    c = 1
    key_pressed = pygame.key.get_pressed()
    Link_move(key_pressed)
    draw(link_beams_right, link_beams_left, link_beams_up, link_beams_down, c)
    if not(bokoblin1.is_killed()):
        bokoblin1.attack_link()
        Link_gets_hit(bokoblin1)
    Link_hits(bokoblin1)
    if not(bokoblin2.is_killed()):
        bokoblin2.attack_link()
        Link_gets_hit(bokoblin2)
    Link_hits(bokoblin2)
    if not(moblin1.is_killed()):
        moblin1.attack_link()
        Link_gets_hit(moblin1)
    Link_hits(moblin1)
    if not(moblin2.is_killed()):
        moblin2.attack_link()
        Link_gets_hit(moblin2)
    Link_hits(moblin2)
    if not(moblin3.is_killed()):
        moblin3.attack_link()
        Link_gets_hit(moblin3)
    Link_hits(moblin3)
    if Enemy.num_enemies == 0 and link_rect.colliderect(lev_3_portal_rect):
        Link.win()