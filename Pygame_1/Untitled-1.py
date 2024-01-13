from pygame import *
from random import randint
 

mixer.init()
mixer.music.load('space.mp3')
mixer.music.play()
fire_sound = mixer.Sound('piy.mp3')
 

font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))
font2 = font.Font(None, 36)


img_back = "space_1.jpg"  # фон гри
img_hero = "2.png"  # герой
img_bullet = "bullet_1.png" # куля
img_enemy = "1.png"  # ворог
img_enemy2 = "astr_1.png"
 
score = 0  # збито кораблів
goal = 200 # стільки кораблів потрібно збити для перемоги
lost = 0  # пропущено кораблів
max_lost = 3 # програли, якщо пропустили стільки


class GameSprite(sprite.Sprite):    
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):        
        sprite.Sprite.__init__(self)       
        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = player_speed 
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
     
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(GameSprite):   
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed   
        if keys[K_UP] and self.rect.y > 5:
            self.rect.x -= self.speed
        if keys[K_DOWN] and self.rect.y < win_width - 80:
            self.rect.x += self.speed   
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):    
    def update(self):
        self.rect.y += self.speed
        global lost        
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):    
    def update(self):
        self.rect.y += self.speed        
        if self.rect.y < 0:
            self.kill()
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height)) 
ship = Player(img_hero, 5, win_height - 100, 80, 100, 10) 
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(
        80, win_width - 80), -40, 80, 50, randint(1, 5))
    monsters.add(monster) 

for i in range(1, 3):
    monster = Enemy(img_enemy2, randint(
        60, win_width - 60), -20, 80, 50, randint(1, 10))
    monsters.add(monster) 
bullets = sprite.Group()
finish = False
run = True   
while run:   
    for e in event.get():
        if e.type == QUIT:
            run = False       
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                ship.fire()   
    if not finish:       
        window.blit(background, (0, 0))
        text = font2.render("Рахунок: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        monsters.update()
        bullets.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True 
            window.blit(lose, (200, 200))    
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))
        display.update()
    time.delay(50)