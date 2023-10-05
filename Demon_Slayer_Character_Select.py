import pygame
import mysql.connector as sqltor

mycon = sqltor.connect(host = "localhost", user = "root", passwd = "sairam", database = "test")
if mycon.is_connected():
    print("You have successfully connected to the database")
cursor = mycon.cursor()

pygame.init()
screen_width, screen_height = (900, 300)
fps = 40
img_width, img_height = (70, 80)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Kimetsu No Yaiba")
bg_img = pygame.transform.scale(pygame.image.load("kny_bg.jpg"), (screen_width, screen_height))
blue = (0, 0, 255); red = (255, 0, 0); green = (0, 255, 0)
running = True

name1 = "Tanjiro Kamado"
tanjiro_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("tanjiro.png"), (img_width + 40, img_height + 40)), 0)
tanjiro_rect = pygame.Rect(img_width, screen_height//2, img_width,img_height)
tanjiro_rect.x = 100; tanjiro_rect.y = screen_height//2 - 50
tanjiro_attack = pygame.transform.scale(pygame.image.load("beam.png"), (img_width, img_height))
tanjiro_attack_form = pygame.transform.scale(pygame.image.load("tanjiro_attack_form.png"), (img_width + 50, img_height + 50))

name2 = "Zenitsu Agatsuma"
zenitsu_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("zenitsu_img.png"), (img_width + 50, img_height + 50)), 0)
zenitsu_rect = pygame.Rect(img_width, screen_height//2, img_width,img_height)
zenitsu_rect.x = 300; zenitsu_rect.y = screen_height//2 - 50
zenitsu_attack = pygame.transform.scale(pygame.image.load("zenitsu_attack.png"), (img_width, img_height))
zenitsu_attack_form = pygame.transform.scale(pygame.image.load("zenitsu_attack_form.png"), (img_width + 50, img_height + 50))

name3 = "Inosuke Hashibira"
inosuke_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("inosuke.png"), (img_width + 50, img_height + 50)), 0)
inosuke_rect = pygame.Rect(img_width, screen_height//2, img_width,img_height)
inosuke_rect.x = 500; inosuke_rect.y = screen_height//2 - 50
inosuke_attack = pygame.transform.scale(pygame.image.load("beam.png"), (img_width, img_height))
inosuke_attack_form = pygame.transform.scale(pygame.image.load("inosuke_attack_form.png"), (img_width + 50, img_height + 50))

name4 = "Tomioka Giyuu"
tomioka_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("tomioka_img.png"), (img_width, img_height + 50)), 0)
tomioka_rect = pygame.Rect(img_width, screen_height//2, img_width,img_height)
tomioka_rect.x = 700; tomioka_rect.y = screen_height//2 - 50
tomioka_attack = pygame.transform.scale(pygame.image.load("blast.png"), (img_width, img_height))
tomioka_attack_form = pygame.transform.scale(pygame.image.load("tomioka_attack_form.png"), (img_width + 50, img_height + 50))

screen.blit(pygame.transform.scale(pygame.image.load("zenitsu.jpg"), (screen_width, screen_height)), (0,0))
screen.blit(tanjiro_img, (tanjiro_rect.x, tanjiro_rect.y))
screen.blit(zenitsu_img, (zenitsu_rect.x, zenitsu_rect.y))
screen.blit(inosuke_img, (inosuke_rect.x, inosuke_rect.y))
screen.blit(tomioka_img, (tomioka_rect.x, tomioka_rect.y))
pygame.display.update()

character = ""
def run_chr_select():
    global running
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tanjiro_rect.collidepoint(event.pos):
                    character = (name1, tanjiro_img, tanjiro_rect, tanjiro_attack, tanjiro_attack_form)
                    running = False
                    return character
                if zenitsu_rect.collidepoint(event.pos):
                    character = (name2, zenitsu_img, zenitsu_rect, zenitsu_attack, zenitsu_attack_form)
                    running = False
                    return character
                if inosuke_rect.collidepoint(event.pos):
                    character = (name3, inosuke_img, inosuke_rect, inosuke_attack, inosuke_attack_form)
                    running = False
                    return character
                if tomioka_rect.collidepoint(event.pos):
                    character = (name4, tomioka_img, tomioka_rect, tomioka_attack, tomioka_attack_form)
                    running = False
                    return character