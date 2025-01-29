import pygame
import sys
import math
import random
import time

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Counterspell')
running = True
black = (0,0,0)
white = (255,255,255)
clock = pygame.time.Clock()
pixel_font = pygame.font.Font("Grand9K Pixel.ttf", 15)
heart = pygame.image.load("heart.png").convert_alpha()
heart_big = pygame.image.load("heart_big.png").convert_alpha()

floor = pygame.image.load("floor.png").convert()
scroll = 0
character = pygame.image.load("character.png").convert_alpha()
enemy_normal = pygame.image.load("enemy_normal.png").convert_alpha()
enemy_angered = pygame.image.load("enemy_angered.png").convert_alpha()
bg = pygame.image.load("background.png").convert()
boss_bg = pygame.image.load("background_volcano.png").convert()
plat_img = pygame.image.load("platform.png").convert()
volcano_blurred = pygame.image.load("volcano_blurred.png").convert()
bgscroll = 0
tiles = math.ceil(800/bg.get_width()) + 1 
bgpos = [(0,0)]
plat_level = 6
plat_num = 0
total_offset = 0
enemy_spawn = 0
hp = 100

punch = pygame.transform.scale(pygame.image.load("punch.png").convert(), (64,64))
fireball = pygame.transform.scale(pygame.image.load("fireball.png").convert(), (64,64))
arrow = pygame.transform.scale(pygame.image.load("arrow.png").convert(), (64,64))
punch_w = pygame.transform.scale(pygame.image.load("punch_w.png").convert_alpha(), (64,64))
fireball_w = pygame.transform.scale(pygame.image.load("fireball_w.png").convert_alpha(), (64,64))
arrow_w = pygame.transform.scale(pygame.image.load("arrow_w.png").convert_alpha(), (64,64))

punch_r = fireball_r = arrow_r = False

pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

class Platform(pygame.sprite.Sprite):
    def __init__(self, left, top, width, height, img=None):
        super().__init__()
        if img == None:
            self.image = pygame.Surface([width, height])
            self.image.fill(white)
        else:
            self.image = img
        self.rect = self.image.get_rect()
        self.rect.x = left
        self.rect.y = top
        self.start_left = left

platforms = pygame.sprite.Group()

class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        super().__init__()
        self.image = character
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.left = 25
        self.rect.top = 636
        self.jumping = False
        self.velocity = 0
        self.jumpcount = 0
        self.base = 636
        self.fall = False
        self.fallcount = 0
        self.lives = 3

class Enemy(pygame.sprite.Sprite):
    def __init__(self, left, width, height):
        super().__init__()
        self.image = enemy_normal
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.start = left
        self.rect.left = left
        self.rect.top = 636
        self.angered = False
        self.range = 100
        self.direction = -1

player = pygame.sprite.GroupSingle(Player(64,64))
enemies = pygame.sprite.Group()
boss_group = pygame.sprite.Group()

def spawn_enemy():
    global enemy_spawn
    enemy_spawn += 1
    enemies.add(Enemy(1000,64,64))

spawn_enemy()

def game_over():
    screen.fill(black)
    text = pixel_font.render("You have defeated yourself....",True,white)
    text_rect = text.get_rect()
    text_rect.center = (400,400)
    screen.blit(text,text_rect)
    pygame.display.update()
    time.sleep(5)
    running = False
    pygame.quit()
    sys.exit()
    exit()
    quit()


def update():
    global punch_r
    global fireball_r
    global arrow_r
    screen.fill(black)
    if player.sprite.lives > 0:
        for i in bgpos:
            screen.blit(bg,i)
        platforms.draw(screen)
        screen.blit(floor, pygame.Rect(0,700,800,100))
        player.draw(screen)
        enemies.draw(screen)
        screen.blit(pixel_font.render(str((round(hp))),False,(255,0,0)), pygame.Rect((player.sprite.rect.left+25,player.sprite.rect.top-10),pixel_font.size(str(round(hp)))))
        screen.blit(heart,pygame.Rect(player.sprite.rect.left+8,player.sprite.rect.top-5,16,16))
        for enemy in enemies:
            if enemy.rect.left >=0 and enemy.rect.left <= 800:
                screen.blit(pixel_font.render(str(round(hp)),False,(255,0,0)), pygame.Rect((enemy.rect.left+25,enemy.rect.top-10),pixel_font.size(str(round(hp)))))
                screen.blit(heart,pygame.Rect(enemy.rect.left+8,enemy.rect.top-5,16,16))
        for i in range(player.sprite.lives):
            screen.blit(heart_big,pygame.Rect(10+(65*i),0,64,64))
    else:
        screen.blit(boss_bg,(0,0))
        player.draw(screen)
        boss_group.draw(screen)
        screen.blit(punch,(70,220))
        screen.blit(fireball,(70,300))
        screen.blit(arrow,(70,380))
        if punch_r:
            for i in range(400):
                screen.fill(black)
                screen.blit(boss_bg,(0,0))
                player.draw(screen)
                boss_group.draw(screen)
                screen.blit(punch,(70,220))
                screen.blit(fireball,(70,300))
                screen.blit(arrow,(70,380))
                screen.blit(punch_w,(200+i,100))
                pygame.display.update()
                time.sleep(0.01)
            punch_r = False
            game_over()
        elif fireball_r:
            for i in range(400):
                screen.fill(black)
                screen.blit(boss_bg,(0,0))
                player.draw(screen)
                boss_group.draw(screen)
                screen.blit(punch,(70,220))
                screen.blit(fireball,(70,300))
                screen.blit(arrow,(70,380))
                screen.blit(fireball_w,(200+i,100))
                pygame.display.update()
                time.sleep(0.01)
            fireball_r = False
            game_over()
        elif arrow_r:
            for i in range(400):
                screen.fill(black)
                screen.blit(boss_bg,(0,0))
                player.draw(screen)
                boss_group.draw(screen)
                screen.blit(punch,(70,220))
                screen.blit(fireball,(70,300))
                screen.blit(arrow,(70,380))
                screen.blit(arrow_w,(200+i,100))
                pygame.display.update()
                time.sleep(0.01)
            arrow_r = False
            game_over()


def scroll_bg(amount):
    global scroll
    global total_offset
    scroll = min(0, scroll-amount)
    total_offset = min(0, total_offset-amount)
    if abs(total_offset) > 800*enemy_spawn:
        spawn_enemy()
    for platform in platforms:
        platform.rect.left = min(platform.rect.left - amount, platform.start_left)
    for enemy in enemies:
        enemy.rect.left = min(enemy.rect.left - amount, enemy.start)

    global bgpos
    if abs(scroll) > bg.get_width():
        scroll = 0
    i=-1
    bgpos = []
    if amount < 0:
        while(i<tiles):
            bgpos += [(bg.get_width()*-i + scroll, 0)]
            i+=1
    else:
        while(i<tiles):
            bgpos += [(bg.get_width()*i + scroll, 0)]
            i+=1
    if not player.sprite.jumping and not player.sprite.fall:
        player.sprite.fall = True
        jump(15)
    update()

def jump(count=0):
    if not player.sprite.fall:
        player.sprite.jumping = True
    else:
        player.sprite.fallcount += 1
    player.sprite.velocity = -10
    player.sprite.jumpcount = count
    if count == 0 or count == 15:
        player.sprite.base = 636

def gen_plat():
    global scroll
    global plat_level
    global plat_num
    plat = Platform(((plat_num+1)*200)-50+scroll,
                    plat_level*100,
                    50,30,plat_img)
    platforms.add(plat)
    r = random.randint(0,2)
    if r == 0:
        plat_level = min(plat_level+1,6)
    elif r == 1:
        plat_level = max(plat_level-1,1)
    plat_num += 1
    

for plat_num in range(10):
    gen_plat()

def die():
    global punch_r
    global fireball_r
    global arrow_r
    for i in range(400):
        screen.fill(black)
        new_bg = pygame.transform.scale(volcano_blurred,(800+(i*2),800+(i*2)))
        screen.blit(new_bg,(-i,-i))
        pygame.display.update()
        time.sleep(0.01)
    screen.fill(black)
    screen.blit(boss_bg,(0,0))
    player.sprite.image = pygame.transform.scale(character,(200,200))
    player.sprite.rect.left = 0
    player.sprite.rect.top = 0
    boss = Enemy(0,64,64)
    boss.rect.left = 600
    boss.rect.top = 0
    boss.image = pygame.transform.scale(enemy_angered,(200,200))
    boss_group.add(boss)
    
update()

while running:
    clock.tick(50)

    for enemy in enemies:
        if abs(enemy.rect.left-player.sprite.rect.left) <= enemy.range*2:
            enemy.angered = True
            enemy.image = enemy_angered
            if pygame.sprite.collide_rect(player.sprite,enemy):
                hp -= 0.5
                if hp <= 0:
                    hp = 100
                    player.sprite.lives -= 1
                    if player.sprite.lives == 0:
                        die()
        else:
            enemy.angered = False
            enemy.image = enemy_normal
        
        if enemy.angered:
            if enemy.rect.left-player.sprite.rect.left > 0:
                enemy.direction = -1
            elif enemy.rect.left-player.sprite.rect.left < 0:
                enemy.direction = 1

            enemy.rect.left += (4*enemy.direction)
              
            
        else:
            if not(enemy.rect.left < 0 or enemy.rect.left > 800):
                enemy.rect.left += (2*enemy.direction)
                if enemy.rect.left <= enemy.start+scroll-(enemy.range/2):
                    enemy.direction = 1
                elif enemy.rect.left >= enemy.start+scroll+(enemy.range/2):
                    enemy.direction = -1

    if player.sprite.jumping or player.sprite.fall:
        if player.sprite.jumpcount < 15:
            player.sprite.rect.top += player.sprite.velocity
            player.sprite.jumpcount += 1
            if pygame.sprite.spritecollideany(player.sprite,platforms):
                player.sprite.jumpcount = 16
        elif player.sprite.rect.top < player.sprite.base:
            player.sprite.rect.top -= player.sprite.velocity
            collision = False
            for platform in platforms:
                if platform.rect.collidepoint(player.sprite.rect.midbottom):
                    collision = platform.rect.top - 64
            if collision:
                player.sprite.base = collision
                player.sprite.rect.top = collision
                player.sprite.jumping = False
                player.sprite.fall = False
                player.sprite.fallcount = 0
        else:
            player.sprite.jumping = False
            player.sprite.fall = False
            player.sprite.fallcount = 0

    keys=pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        scroll_bg(-6)
    if keys[pygame.K_RIGHT]:
        scroll_bg(6)
        gen_plat()
    if keys[pygame.K_SPACE]:
        if (player.sprite.rect.top == player.sprite.base or player.sprite.fall) and not player.sprite.jumping and player.sprite.fallcount <=2:
            jump()

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
            exit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.Rect(70,220,64,64).collidepoint(event.pos):
                punch_r = True
            elif pygame.Rect(70,300,64,64).collidepoint(event.pos):
                fireball_r = True
            elif pygame.Rect(70,380,64,64).collidepoint(event.pos):
                arrow_r = True

    update()
    pygame.display.update()