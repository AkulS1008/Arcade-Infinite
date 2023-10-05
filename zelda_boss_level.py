import pygame
from pygame import mixer
import time
import os

pygame.init()#; mixer.init()
screen_width, screen_height = (900, 700)
fps = 30
img_width, img_height = (70, 60)
boss_width, boss_height = (85, 75)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("The Legend of Zelda: Boss")
mixer.music.load("boss_theme.mp3")
mixer.music.play()

beam_velocity = 5
max_beams = 5
bg_img = pygame.transform.scale(pygame.image.load("boss_arena.jpg"), (screen_width, screen_height))
link = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("link.png"), (img_width, img_height)), 0)
link_rect = pygame.Rect(10,10, img_width,img_height)
blue = (0, 0, 255); red = (255, 0, 0); green = (0, 255, 0)
running = True; score = 0; do = False

font1 = pygame.font.SysFont('freesansbold.ttf', 32)
gameOver = font1.render('Game Over!', True, red)
gameOver_rect = gameOver.get_rect()
gameOver_rect.center = (screen_width // 2, screen_height // 2)
winner = font1.render('You Win!', True, blue)
winner_rect = winner.get_rect()
winner_rect.center = (screen_width // 2, screen_height // 2)

class Link:
    health = 1000
    beam_damage = 10
    velocity = 3
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
        font2 = pygame.font.SysFont('freesansbold.ttf', 55)
        SCORE = font2.render('Score: ' + str(score), True, blue)
        SCORERect = SCORE.get_rect()
        SCORERect.center = (screen_width // 2, screen_height // 2 + 33)
        screen.blit(SCORE, SCORERect)
        pygame.display.update()
        pygame.mixer.music.stop()
        time.sleep(2)
        pygame.display.quit()
        os.system("python zelda_boss_level.py")
        
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
        os.system("python HOME_GUI.py")

class Item:
    def __init__(self, item_name, item_img, item_rect):
        self.item_name = item_name
        self.item_img = item_img
        self.item_rect = item_rect
    
    def modify_item_img(self, new_img):
        self.item_img = new_img

    def modify_item_rect(self, new_rect):
        self.item_rect = new_rect
    
    def get_item_rect(self):
        return self.item_rect
    
    def get_item_x(self):
        return self.item_rect.x

    def get_item_y(self):
        return self.item_rect.y

    def get_img(self):
        return self.item_img

    def taken(self):
        if self.item_name == "life up":
            Link.health += 100
        if self.item_name == "attack up":
            Link.beam_damage += 10
        self.modify_item_img(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("dead.png"), (0,0)), 0))
        self.modify_item_rect(pygame.Rect(screen_width + 10,screen_height + 10, boss_width,boss_height))

class Boss:
    num_bosses = 0
    def __init__(self, boss_name, boss, boss_rect, boss_positions, boss_velocity, health, boss_damage):
        self.boss_name = boss_name
        self.boss = boss
        self.boss_rect = boss_rect
        self.boss_positions = boss_positions
        self.boss_velocity = boss_velocity
        self.health = health
        self.boss_damage = boss_damage
        Boss.num_bosses += 1
    
    def get_boss_name(self):
        return self.boss_name

    def damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.modify_boss(pygame.transform.rotate(pygame.transform.scale(pygame.image.load("dead.png"), (0,0)), 0))
            self.modify_boss_rect(pygame.Rect(screen_width + 10,screen_height + 10, boss_width,boss_height))
            self.boss_velocity = 0
            Boss.num_bosses -= 1

    def modify_boss_positions(self, new_pos):
        self.boss_positions = new_pos

    def give_damage(self):
        return self.boss_damage

    def is_killed(self):
        return self.health <= 0

    def modify_boss(self, boss_new):
        self.boss = boss_new
    
    def modify_boss_rect(self, new_rect):
        self.boss_rect = new_rect

    def get_boss_health(self):
        return self.health

    def get_boss(self):
        return self.boss
    
    def get_boss_rect(self):
        return self.boss_rect

    def get_boss_x(self):
        return self.boss_rect.x

    def get_boss_y(self):
        return self.boss_rect.y

    def move_left(self):
        self.modify_boss(self.boss_positions[0])
        if self.boss_rect.x > 0:
            self.boss_rect.x -= self.boss_velocity
        else:
            self.move_right()

    def move_right(self):
        self.modify_boss(self.boss_positions[1])
        if self.boss_rect.x < screen_width:
            self.boss_rect.x += self.boss_velocity
        else:
            self.move_left()

    def move_up(self):
        self.modify_boss(self.boss_positions[2])
        if self.boss_rect.y > 0:
            self.boss_rect.y -= self.boss_velocity
        else:
            self.move_down()

    def move_down(self):
        self.modify_boss(self.boss_positions[3])
        if self.boss_rect.y < screen_height:
           self.boss_rect.y += self.boss_velocity
        else:
            self.move_up()

    def attack_link(self):
        if self.health <= 500:
            gl = pygame.transform.scale(pygame.image.load("ganon2_left.png"), (boss_width, boss_height))
            gr = pygame.transform.scale(pygame.image.load("ganon2_left.png"), (boss_width, boss_height))
            gu = pygame.transform.scale(pygame.image.load("ganon2_down.png"), (boss_width, boss_height))
            gd = pygame.transform.scale(pygame.image.load("ganon2_down.png"), (boss_width, boss_height))
            self.modify_boss_positions([gl, gr, gu, gd])
        if self.boss_rect.x >= link_rect.x + img_width:
            self.move_left()
        if self.boss_rect.y <= link_rect.y:
            self.move_down()
        if self.boss_rect.x <= link_rect.x + img_width:
            self.move_right()
        if self.boss_rect.y >= link_rect.y:
            self.move_up()

    def attack(self):
        global do
        do = True

ganondorf_left = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ganon_left.png"), (boss_width, boss_height)), 0)
ganondorf_right = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ganon_right.png"), (boss_width, boss_height)), 0)
ganondorf_up = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ganon_up.png"), (boss_width, boss_height)), 0)
ganondorf_down = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("ganon_down.png"), (boss_width, boss_height)), 0)
ganondorf_pos = [ganondorf_left, ganondorf_right, ganondorf_up, ganondorf_down]
ganondorf = Boss("ganondorf", ganondorf_down, pygame.Rect(screen_width//2,screen_height//2, boss_width,boss_height), ganondorf_pos, 2, 1000, 70)

attack_up_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("attack_up.png"), (img_width, img_height)), 0)
attack_up_rect = pygame.Rect(screen_width - 100,30, img_width,img_height)
attack_up = Item("attack up", attack_up_img, attack_up_rect)

life_up_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("life_up.png"), (img_width, img_height)), 0)
life_up_rect = pygame.Rect(100, 500, img_width,img_height)
life_up = Item("life up", life_up_img, life_up_rect)

def draw(link_beams_right, link_beams_left, link_beams_up, link_beams_down, c):
    global do
    screen.blit(bg_img, (0, 0))
    if c == 0:
        screen.blit(link, (link_rect.x, link_rect.y))
    screen.blit(ganondorf.get_boss(), (ganondorf.get_boss_x(), ganondorf.get_boss_y()))
    screen.blit(attack_up.get_img(), (attack_up.get_item_x(), attack_up.get_item_y()))
    screen.blit(life_up.get_img(), (life_up.get_item_x(), life_up.get_item_y()))
    font1 = pygame.font.SysFont('freesansbold.ttf', 32)
    HEALTH = font1.render('Health: ' + str(Link.health), True, green)
    HEALTH_rect = HEALTH.get_rect()
    HEALTH_rect.center = (screen_width // 2, 11)
    screen.blit(HEALTH, HEALTH_rect) 
    font2 = pygame.font.SysFont('freesansbold.ttf', 20)
    BOSSHEALTH = font2.render(str(ganondorf.get_boss_health()), True, red)
    BOSSHEALTH_rect = BOSSHEALTH.get_rect()
    BOSSHEALTH_rect.center = (ganondorf.get_boss_x() + boss_width//2, ganondorf.get_boss_y() - 5)
    screen.blit(BOSSHEALTH, BOSSHEALTH_rect)
    for beam in link_beams_right:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_left:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_up:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_down:
        pygame.draw.rect(screen, blue, beam)
    if do: 
        for attack in battacks:
            screen.blit(pygame.transform.scale(pygame.image.load("beam.png"), (img_width, img_height)), (attack.x, attack.y))
        #do = False   
    pygame.display.update()
draw([], [], [], [], 0)

def draw_normal(link_beams_right, link_beams_left, link_beams_up, link_beams_down):
    global do
    screen.blit(bg_img, (0, 0))
    screen.blit(ganondorf.get_boss(), (ganondorf.get_boss_x(), ganondorf.get_boss_y()))
    screen.blit(attack_up.get_img(), (attack_up.get_item_x(), attack_up.get_item_y()))
    screen.blit(life_up.get_img(), (life_up.get_item_x(), life_up.get_item_y()))
    font1 = pygame.font.SysFont('freesansbold.ttf', 32)
    HEALTH = font1.render('Health: ' + str(Link.health), True, green)
    HEALTH_rect = HEALTH.get_rect()
    HEALTH_rect.center = (screen_width // 2, 11)
    screen.blit(HEALTH, HEALTH_rect) 
    font2 = pygame.font.SysFont('freesansbold.ttf', 20)
    BOSSHEALTH = font2.render(str(ganondorf.get_boss_health()), True, red)
    BOSSHEALTH_rect = BOSSHEALTH.get_rect()
    BOSSHEALTH_rect.center = (ganondorf.get_boss_x() + boss_width//2, ganondorf.get_boss_y() - 5)
    screen.blit(BOSSHEALTH, BOSSHEALTH_rect)
    for beam in link_beams_right:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_left:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_up:
        pygame.draw.rect(screen, blue, beam)
    for beam in link_beams_down:
        pygame.draw.rect(screen, blue, beam) 
    if do:
        for attack in battacks:
            screen.blit(pygame.transform.scale(pygame.image.load("beam.png"), (img_width, img_height)), (attack.x, attack.y))
        #do = False
    pygame.display.update()

def Link_move(k):
    if k[pygame.K_UP] and link_rect.y > 0:
        link_rect.y -= Link.velocity
    if k[pygame.K_DOWN] and link_rect.y < screen_height - img_height:
        link_rect.y += Link.velocity
    if k[pygame.K_LEFT] and link_rect.x > 0:
        link_rect.x -= Link.velocity
    if k[pygame.K_RIGHT] and link_rect.x < screen_width - img_width:
        link_rect.x += Link.velocity  
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

boss_score = 15
def Link_hits(boss):
    global score
    for beam in link_beams_right:
        if boss.get_boss_rect().colliderect(beam):
            link_beams_right.remove(beam)
            boss.damage(Link.beam_damage)
            if boss.get_boss_name() == "ganondorf":
                score += boss_score
        if beam.x > screen_width:
            link_beams_right.remove(beam)
    for beam in link_beams_left:
        if boss.get_boss_rect().colliderect(beam):
            link_beams_left.remove(beam)
            boss.damage(Link.beam_damage)
            if boss.get_boss_name() == "ganondorf":
                score += boss_score
        if beam.x < 0:
            link_beams_left.remove(beam)
    for beam in link_beams_up:
        if boss.get_boss_rect().colliderect(beam):
            link_beams_up.remove(beam)
            boss.damage(Link.beam_damage)
            if boss.get_boss_name() == "ganondorf":
                score += boss_score
        if beam.y < 0:
            link_beams_up.remove(beam)
    for beam in link_beams_down:
        if boss.get_boss_rect().colliderect(beam):
            link_beams_down.remove(beam)
            boss.damage(Link.beam_damage)
            if boss.get_boss_name() == "ganondorf":
                score += boss_score
        for attack in battacks:
            if attack.colliderect(beam):
                link_beams_down.remove(beam)
                battacks.remove(attack)
        if beam.y > screen_height:
            link_beams_down.remove(beam)
        
def attack_movements():
    for attack in battacks:
        if ganondorf.get_boss_x() >= link_rect.x + img_width:
            attack.x -= 3
        elif ganondorf.get_boss_y() <= link_rect.y:
            attack.y += 3
        elif ganondorf.get_boss_x() <= link_rect.x + img_width:
            attack.x += 3
        elif ganondorf.get_boss_y() >= link_rect.y:
            attack.y -= 3

def counters():
    for beam in link_beams_right:
        for attack in battacks:
            if attack.colliderect(beam):
                link_beams_right.remove(beam)
                battacks.remove(attack)
    for beam in link_beams_left:
        for attack in battacks:
            if attack.colliderect(beam):
                link_beams_left.remove(beam)
                battacks.remove(attack)
    for beam in link_beams_up:
        for attack in battacks:
            if attack.colliderect(beam):
                link_beams_up.remove(beam)
                battacks.remove(attack)
    for beam in link_beams_down:
        for attack in battacks:
            if attack.colliderect(beam):
                link_beams_down.remove(beam)
                battacks.remove(attack)
    

def Link_gets_hit(boss):
    if link_rect.colliderect(boss.get_boss_rect()):
        Link.take_damage(boss.give_damage())
    if link_rect.colliderect(life_up.get_item_rect()):
        life_up.taken()
    if link_rect.colliderect(attack_up.get_item_rect()):
        attack_up.taken()
    for attack in battacks:
        if link_rect.colliderect(attack):
            Link.take_damage(100)
            battacks.remove(attack)
        if attack.x == 0 or attack.x == screen_width or attack.y == 0 or attack.y == screen_height:
            battacks.remove(attack)

attack_timer = pygame.USEREVENT + 1
pygame.time.set_timer(attack_timer, 4500)
link_beams_right = []
link_beams_left = []
link_beams_up = []
link_beams_down = []
battacks = []
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
        if event.type == attack_timer:
            attack = pygame.Rect(ganondorf.get_boss_x() + boss_width//2, ganondorf.get_boss_y() + boss_height//2, beam_wid_hor,beam_hei_hor)
            battacks.append(attack)
            ganondorf.attack()
    key_pressed = pygame.key.get_pressed()
    Link_move(key_pressed)
    draw(link_beams_right, link_beams_left, link_beams_up, link_beams_down, c)
    if not(ganondorf.is_killed()):
        ganondorf.attack_link()
        attack_movements()
        counters()
        Link_gets_hit(ganondorf)
    Link_hits(ganondorf)
    if Boss.num_bosses == 0:
        Link.win()