import pygame
import random
import Demon_Slayer_Character_Select   
import mysql.connector as sqltor
import os

mycon = sqltor.connect(host = "localhost", user = "root", passwd = "sairam", database = "test")
if mycon.is_connected():
    print("You have successfully connected to the database")
cursor = mycon.cursor()

pygame.init()
fps = 60
img_width, img_height = (80, 90)
clock = pygame.time.Clock()
velocity = 10
blue = (0, 0, 255); red = (255, 0, 0); green = (0, 255, 0)
running = True; score = 0; retry_rect = None; key = False
SCORE = 0; enemy_vel = 4
class Player:
    health = 100
    def __init__(self, name, img, rect, attack, attack_form):
        self.name = name
        self.img = img
        self.rect = rect
        self.attack = attack
        self.attack_form = attack_form
    
    def attacks(self):
        draw_normal()
        screen.blit(self.attack_form, self.rect)
        pygame.display.update()
        pygame.time.delay(150)

    def get_img(self):
        return self.img

    def get_rect(self):
        return self.rect
    
    def get_attack(self):
        return self.attack
    
    def get_name(self):
        return self.name
 
name, image, rect, attack, attack_form = Demon_Slayer_Character_Select.run_chr_select()
#mixer.music.load("level2_theme.mp3")
#mixer.music.play()
screen_width, screen_height = (1000, 700)
screen = pygame.display.set_mode((screen_width, screen_height))
bg_img = pygame.transform.scale(pygame.image.load("kny_bg.jpg"), (screen_width, screen_height))
pygame.display.set_caption("Kimetsu No Yaiba")
character = Player(name, image, rect, attack, attack_form)
character.get_rect().x = 100; character.get_rect().y = screen_height//2

def draw(c):
    global retry_rect, key, enemy_vel
    screen.blit(bg_img, (0, 0))
    font1 = pygame.font.SysFont('freesansbold.ttf', 50)
    score = font1.render("Score: " + str(SCORE), True, (225, 225, 0))
    score_rect = score.get_rect()
    score_rect.center = (screen_width//2, 20)
    screen.blit(score, score_rect)
    font2 = pygame.font.Font('freesansbold.ttf', 20)
    retry = font2.render('RETRY', True, (255, 255, 255), red)
    retry_rect = retry.get_rect()
    retry_rect.center = (screen_width - 40, 20)
    screen.blit(retry, retry_rect)
    if key == True:
        enemy_vel = 0
        game_over()
    if c == 0:
        screen.blit(character.get_img(), (character.get_rect().x, character.get_rect().y))
    for enemy in enemies:
        screen.blit(enemy[0], enemy[1])   
    for beam in beam_list:
        screen.blit(character.get_attack(), (beam.x, beam.y))
    pygame.display.update()

def draw_normal():
    global retry_rect, key, enemy_vel
    screen.blit(bg_img, (0, 0))
    font1 = pygame.font.SysFont('freesansbold.ttf', 50)
    score = font1.render("Score: " + str(SCORE), True, (225, 225, 0))
    score_rect = score.get_rect()
    score_rect.center = (screen_width//2, 20)
    screen.blit(score, score_rect)
    font2 = pygame.font.Font('freesansbold.ttf', 20)
    retry = font2.render('RETRY', True, (255, 255, 255), red)
    retry_rect = retry.get_rect()
    retry_rect.center = (screen_width - 40, 20)
    screen.blit(retry, retry_rect)
    if key == True:
        enemy_vel = 0
        game_over()
    for enemy in enemies:
        screen.blit(enemy[0], enemy[1])
    for beam in beam_list:
        screen.blit(character.get_attack(), (beam.x, beam.y))
    pygame.display.update()

def Tanjiro_movements(k):
    if k[pygame.K_SPACE] and 0 < character.get_rect().y <= screen_height - img_height and key == False:
        character.get_rect().y -= velocity
    if k[pygame.K_d] and key == False:
        character.attacks()
    if character.get_rect().y <= screen_height - img_height and key == False:
        character.get_rect().y += 5
    if character.get_rect().y == screen_height - img_height and key == False:
        game_over()
    for beam in beam_list:
        beam.x += 10

def enemy_movements():
    global enemy_vel
    for enemy in enemies:
        enemy[1].x -= enemy_vel
 
def game_over():
    global key
    global SCORE
    font1 = pygame.font.SysFont('freesansbold.ttf', 69)
    gameover = font1.render("GAME OVER!!!", True, red)
    gameover_rect = gameover.get_rect()
    gameover_rect.center = (screen_width//2, screen_height//2)
    screen.blit(gameover, gameover_rect)
    cursor.execute("INSERT INTO demon_slayer_scores values({});".format(SCORE))
    mycon.commit()
    cursor.execute("SELECT max(Score) FROM demon_slayer_scores;")
    hs = cursor.fetchone()[0]
    cursor.execute("INSERT INTO DemonSlayer_Scores WHERE Name = {")
    highscore = font1.render("Your Highest Score so far: {}".format(hs), True, blue)
    highscore_rect = highscore.get_rect()
    highscore_rect.center = (screen_width//2, screen_height//2 + 50)
    screen.blit(highscore, highscore_rect)
    pygame.display.update()
    key = True
                         
def Tanjiro_hits():
    global SCORE; global enemy_timer
    for beam in beam_list:
        if beam.x > screen_width:
            beam_list.remove(beam)
    for beam in beam_list:
        for enemy in enemies: 
            if beam.colliderect(enemy[1]):
                SCORE += 1
                if beam in beam_list:
                    beam_list.remove(beam)
                    enemies.remove(enemy)
                if SCORE > 5:
                    pygame.time.set_timer(enemy_timer, 1500)
                if SCORE > 10:
                    pygame.time.set_timer(enemy_timer, 1000)
                if SCORE > 15:
                    pygame.time.set_timer(enemy_timer, 500)
    for enemy in enemies:
        if character.get_rect().colliderect(enemy[1]):
            game_over()
        if enemy[1].x == 0:
            SCORE -= 1
    
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 4500)
scene_timer = pygame.USEREVENT + 3
pygame.time.set_timer(scene_timer, 10000)

akaza = pygame.transform.scale(pygame.image.load("akaza.png"), (img_width + 50, img_height + 50))
muzan = pygame.transform.scale(pygame.image.load("muzan.png"), (img_width + 50, img_height + 50))
subham = pygame.transform.scale(pygame.image.load("subham.png"), (img_width + 50, img_height + 50))
sukuna = pygame.transform.scale(pygame.image.load("sukuna.png"), (img_width + 50, img_height + 50))
max_beams = 5

enemy_imgs = [akaza, muzan, subham, sukuna]
beam_list = []
enemies = []
while running:
    clock.tick(fps)
    c = 0
    beam_wid_hor, beam_hei_hor = 15, 8
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            cursor.execute("DELETE FROM demon_slayer_scores;")
            mycon.commit()
            mycon.close()
            pygame.quit()
        if event.type == pygame.KEYDOWN and key == False:
            if event.key == pygame.K_d and len(beam_list) < max_beams:
                beam = pygame.Rect(character.get_rect().x + img_width//2, character.get_rect().y + img_height//2, beam_wid_hor,beam_hei_hor)
                beam_list.append(beam)
                c = 1
        if event.type == enemy_timer and key == False:
            enemy = random.choice(enemy_imgs)
            x = random.randrange(screen_width//2 + 100, screen_width - img_width)
            y = random.randrange(10, screen_height - img_height - 100)
            enemy_rect = pygame.Rect(x,y, img_width,img_height)
            enemies.append((enemy, enemy_rect))
        if event.type == scene_timer and key == False:
            scenes = [pygame.transform.scale(pygame.image.load("kny_bg.jpg"), (screen_width, screen_height)), pygame.transform.scale(pygame.image.load("kny_bg2.jpg"), (screen_width, screen_height)), pygame.transform.scale(pygame.image.load("kny_bg3.jpg"), (screen_width, screen_height)), pygame.transform.scale(pygame.image.load("landscape-anime-digital-art-fantasy-art-wallpaper-preview.jpg"), (screen_width, screen_height)), pygame.transform.scale(pygame.image.load("itachi.jpg"), (screen_width, screen_height))]
            bg_img = random.choice(scenes)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if retry_rect.collidepoint(event.pos):
                pygame.display.quit()
                mycon.close()
                os.system("python Demon_Slayer.py")
    key_pressed = pygame.key.get_pressed()
    Tanjiro_movements(key_pressed)
    draw(c); Tanjiro_hits(); enemy_movements()
    pygame.display.update()