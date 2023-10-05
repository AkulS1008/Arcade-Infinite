import pygame
import time
from pygame import mixer
import random
                     
pygame.init(); mixer.init()
screen_width, screen_height = (900, 700)
fps = 40
img_width, img_height = (70, 60)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Legend of Zelda")
max_beams = 5


velocity = 3; beam_velocity = 5
bg_img = pygame.transform.scale(pygame.image.load("bg.png"), (screen_width, screen_height))
link = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("link.png"), (img_width, img_height)), 0)
link_rect = pygame.Rect(10,10, img_width,img_height)
blue = (0, 0, 255); red = (255, 0, 0); green = (0, 255, 0)
running = True; score = 0

font1 = pygame.font.Font('freesansbold.ttf', 32)
gameOver = font1.render('Game Over!', True, red, blue)
gameOver_rect = gameOver.get_rect()
gameOver_rect.center = (screen_width // 2, screen_height // 2)
winner = font1.render('You Win!', True, green, blue)
winner_rect = winner.get_rect()
winner_rect.center = (screen_width // 2, screen_height // 2)

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
        link_dead = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("dead.png"), (0.1, 0.1)), 0)
        screen.blit(link_dead, (link_rect.x, link_rect.y))
        screen.blit(gameOver, gameOver_rect) 
        font2 = pygame.font.Font('freesansbold.ttf', 25)
        SCORE = font2.render('Score: ' + str(score), True, green, blue)
        SCORERect = SCORE.get_rect()
        SCORERect.center = (screen_width // 2, screen_height // 2 + 33)
        screen.blit(SCORE, SCORERect)
        pygame.display.update()
        time.sleep(1)
        pygame.display.quit()
        
    def win():
        font2 = pygame.font.Font('freesansbold.ttf', 25)
        SCORE = font2.render('Score: ' + str(score), True, green, blue)
        SCORERect = SCORE.get_rect()
        SCORERect.center = (screen_width // 2, screen_height // 2 + 33)
        screen.blit(winner, winner_rect) 
        screen.blit(SCORE, SCORERect) 
        pygame.display.update()
        time.sleep(1)
        pygame.display.quit()
        
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
octorock_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("octorock_left.png"), (img_width, img_height)), 0)
octorock_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("octorock_right.png"), (img_width, img_height)), 0)
octorock_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("octorock_up.png"), (img_width, img_height)), 0)
octorock_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("octorock_down.png"), (img_width, img_height)), 0)
octorock_pos = [octorock_left, octorock_right, octorock_up, octorock_down]
octorock = Enemy("octorock", octorock_left, pygame.Rect(randx,randy, img_width,img_height), octorock_pos, 0.1, 10, 5)

randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
bokoblin_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_left.png"), (img_width, img_height)), 0)
bokoblin_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_right.png"), (img_width, img_height)), 0)
bokoblin_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_up.png"), (img_width, img_height)), 0)
bokoblin_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("bokoblin_down.png"), (img_width, img_height)), 0)
bokoblin_pos = [bokoblin_left, bokoblin_right, bokoblin_up, bokoblin_down]
bokoblin = Enemy("bokoblin", bokoblin_down, pygame.Rect(randx,randy, img_width,img_height), bokoblin_pos, 1, 35, 10)

randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
darknut_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("darknut_left.png"), (img_width, img_height)), 0)
darknut_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("darknut_right.png"), (img_width, img_height)), 0)
darknut_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("darknut_up.png"), (img_width, img_height)), 0)
darknut_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("darknut_down.png"), (img_width, img_height)), 0)
darknut_pos = [darknut_left, darknut_right, darknut_up, darknut_down]
darknut = Enemy("darknut", darknut_down, pygame.Rect(randx,randy, img_width,img_height), darknut_pos, 1.5, 50, 20)

randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
moblin_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_left.png"), (img_width, img_height)), 0)
moblin_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_right.png"), (img_width, img_height)), 0)
moblin_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_up.png"), (img_width, img_height)), 0)
moblin_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("moblin_down.png"), (img_width, img_height)), 0)
moblin_pos = [moblin_left, moblin_right, moblin_up, moblin_down]
moblin = Enemy("moblin", moblin_down, pygame.Rect(randx,randy, img_width,img_height), moblin_pos, 1.5, 80, 25)

randx = random.randrange(20 + img_width, screen_width - img_width)
randy = random.randrange(20 + img_height, screen_height - img_height)
lynel_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("lynel_left.png"), (img_width, img_height)), 0)
lynel_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("lynel_right.png"), (img_width, img_height)), 0)
lynel_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("lynel_up.png"), (img_width, img_height)), 0)
lynel_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("lynel_down.png"), (img_width, img_height)), 0)
lynel_pos = [lynel_left, lynel_right, lynel_up, lynel_down]
lynel = Enemy("lynel", lynel_down, pygame.Rect(randx,randy, img_width,img_height), lynel_pos, 2, 100, 30)

def draw(link_beams_right, link_beams_left, link_beams_up, link_beams_down, c):
    screen.blit(bg_img, (0, 0))
    if c == 0:
        screen.blit(link, (link_rect.x, link_rect.y))
    screen.blit(octorock.get_enemy(), (octorock.get_enemy_x(), octorock.get_enemy_y()))
    screen.blit(bokoblin.get_enemy(), (bokoblin.get_enemy_x(), bokoblin.get_enemy_y()))
    screen.blit(lynel.get_enemy(), (lynel.get_enemy_x(), lynel.get_enemy_y()))
    screen.blit(darknut.get_enemy(), (darknut.get_enemy_x(), darknut.get_enemy_y()))
    screen.blit(moblin.get_enemy(), (moblin.get_enemy_x(), moblin.get_enemy_y()))
    font1 = pygame.font.Font('freesansbold.ttf', 20)
    HEALTH = font1.render('Health: ' + str(Link.health), True, green, blue)
    HEALTH_rect = HEALTH.get_rect()
    HEALTH_rect.center = (screen_width // 2, 11)
    screen.blit(HEALTH, HEALTH_rect) 
    font2 = pygame.font.Font('freesansbold.ttf', 15)
    OCTOHEALTH = font2.render(str(octorock.get_enemy_health()), True, red, blue)
    OCTOHEALTH_rect = OCTOHEALTH.get_rect()
    OCTOHEALTH_rect.center = (octorock.get_enemy_x() + img_width//2, octorock.get_enemy_y() - 5)
    screen.blit(OCTOHEALTH, OCTOHEALTH_rect)
    BOKOHEALTH = font2.render(str(bokoblin.get_enemy_health()), True, red, blue)
    BOKOHEALTH_rect = BOKOHEALTH.get_rect()
    BOKOHEALTH_rect.center = (bokoblin.get_enemy_x() + img_width//2, bokoblin.get_enemy_y() - 5)
    screen.blit(BOKOHEALTH, BOKOHEALTH_rect)
    MOBHEALTH = font2.render(str(moblin.get_enemy_health()), True, red, blue)
    MOBHEALTH_rect = MOBHEALTH.get_rect()
    MOBHEALTH_rect.center = (moblin.get_enemy_x() + img_width//2, moblin.get_enemy_y() - 5)
    screen.blit(MOBHEALTH, MOBHEALTH_rect)
    DNHEALTH = font2.render(str(darknut.get_enemy_health()), True, red, blue)
    DNHEALTH_rect = DNHEALTH.get_rect()
    DNHEALTH_rect.center = (darknut.get_enemy_x() + img_width//2, darknut.get_enemy_y() - 5)
    screen.blit(DNHEALTH, DNHEALTH_rect)
    LYNHEALTH = font2.render(str(lynel.get_enemy_health()), True, red, blue)
    LYNHEALTH_rect = LYNHEALTH.get_rect()
    LYNHEALTH_rect.center = (lynel.get_enemy_x() + img_width//2, lynel.get_enemy_y() - 5)
    screen.blit(LYNHEALTH, LYNHEALTH_rect)
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
    screen.blit(octorock.get_enemy(), (octorock.get_enemy_x(), octorock.get_enemy_y()))
    screen.blit(bokoblin.get_enemy(), (bokoblin.get_enemy_x(), bokoblin.get_enemy_y()))
    screen.blit(lynel.get_enemy(), (lynel.get_enemy_x(), lynel.get_enemy_y()))
    screen.blit(darknut.get_enemy(), (darknut.get_enemy_x(), darknut.get_enemy_y()))
    screen.blit(moblin.get_enemy(), (moblin.get_enemy_x(), moblin.get_enemy_y()))
    font1 = pygame.font.Font('freesansbold.ttf', 20)
    HEALTH = font1.render('Health: ' + str(Link.health), True, green, blue)
    HEALTH_rect = HEALTH.get_rect()
    HEALTH_rect.center = (screen_width // 2, 11)
    screen.blit(HEALTH, HEALTH_rect) 
    font2 = pygame.font.Font('freesansbold.ttf', 15)
    OCTOHEALTH = font2.render(str(octorock.get_enemy_health()), True, red, blue)
    OCTOHEALTH_rect = OCTOHEALTH.get_rect()
    OCTOHEALTH_rect.center = (octorock.get_enemy_x() + img_width//2, octorock.get_enemy_y() - 5)
    screen.blit(OCTOHEALTH, OCTOHEALTH_rect)
    BOKOHEALTH = font2.render(str(bokoblin.get_enemy_health()), True, red, blue)
    BOKOHEALTH_rect = BOKOHEALTH.get_rect()
    BOKOHEALTH_rect.center = (bokoblin.get_enemy_x() + img_width//2, bokoblin.get_enemy_y() - 5)
    screen.blit(BOKOHEALTH, BOKOHEALTH_rect)
    MOBHEALTH = font2.render(str(moblin.get_enemy_health()), True, red, blue)
    MOBHEALTH_rect = MOBHEALTH.get_rect()
    MOBHEALTH_rect.center = (moblin.get_enemy_x() + img_width//2, moblin.get_enemy_y() - 5)
    screen.blit(MOBHEALTH, MOBHEALTH_rect)
    DNHEALTH = font2.render(str(darknut.get_enemy_health()), True, red, blue)
    DNHEALTH_rect = DNHEALTH.get_rect()
    DNHEALTH_rect.center = (darknut.get_enemy_x() + img_width//2, darknut.get_enemy_y() - 5)
    screen.blit(DNHEALTH, DNHEALTH_rect)
    LYNHEALTH = font2.render(str(lynel.get_enemy_health()), True, red, blue)
    LYNHEALTH_rect = LYNHEALTH.get_rect()
    LYNHEALTH_rect.center = (lynel.get_enemy_x() + img_width//2, lynel.get_enemy_y() - 5)
    screen.blit(LYNHEALTH, LYNHEALTH_rect)
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

octorock_score = 3
bokoblin_score = 5
moblin_score = 7
darknut_score = 8
lynel_score = 10
def Link_hits(enemy):
    global score
    for beam in link_beams_right:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_right.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "octorock":
                score += octorock_score
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
            if enemy.get_enemy_name() == "darknut":
                score += darknut_score
            if enemy.get_enemy_name() == "lynel":
                score += lynel_score
        if beam.x > screen_width:
            link_beams_right.remove(beam)
    for beam in link_beams_left:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_left.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "octorock":
                score += octorock_score
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
            if enemy.get_enemy_name() == "darknut":
                score += darknut_score
            if enemy.get_enemy_name() == "lynel":
                score += lynel_score
        if beam.x < 0:
            link_beams_left.remove(beam)
    for beam in link_beams_up:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_up.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "octorock":
                score += octorock_score
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
            if enemy.get_enemy_name() == "darknut":
                score += darknut_score
            if enemy.get_enemy_name() == "lynel":
                score += lynel_score
        if beam.y < 0:
            link_beams_up.remove(beam)
    for beam in link_beams_down:
        if enemy.get_enemy_rect().colliderect(beam):
            link_beams_down.remove(beam)
            enemy.damage(Link.beam_damage)
            if enemy.get_enemy_name() == "octorock":
                score += octorock_score
            if enemy.get_enemy_name() == "bokoblin":
                score += bokoblin_score
            if enemy.get_enemy_name() == "moblin":
                score += moblin_score
            if enemy.get_enemy_name() == "darknut":
                score += darknut_score
            if enemy.get_enemy_name() == "lynel":
                score += lynel_score
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
    if not(octorock.is_killed()):
        octorock.attack_link()
        Link_gets_hit(octorock)
    Link_hits(octorock)
    if not(bokoblin.is_killed()):
        bokoblin.attack_link()
        Link_gets_hit(bokoblin)
    Link_hits(bokoblin)
    if not(darknut.is_killed()):
        darknut.attack_link()
        Link_gets_hit(darknut)
    Link_hits(darknut)
    if not(moblin.is_killed()):
        moblin.attack_link()
        Link_gets_hit(moblin)
    Link_hits(moblin)
    if not(lynel.is_killed()):
        lynel.attack_link()
        Link_gets_hit(lynel)
    Link_hits(lynel)
    if Enemy.num_enemies == 0:
        Link.win()