#|Начало: 21.04.2021|
#Создай собственный Шутер!
#--------------------------------------
#Модули                               |
#--------------------------------------
from pygame import *
from random import randint
#--------------------------------------
#Класс                                |
#--------------------------------------
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.w = w
        self.h = h
        self.speed = speed
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
#--------------------------------------
#Подкласс для игрока                  |
#--------------------------------------
bullets = sprite.Group()
class Player(GameSprite):
    w = 60
    h = 60
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x <= 650:
            self.rect.x += self.speed
    def fire(self):
        speed = 3
        bullet = Bullets('bullet.png', self.rect.x, self.rect.y, speed, 10, 20)
        bullets.add(bullet)
#--------------------------------------
#Подкласс для врага                   |
#--------------------------------------
lost = 0                         #|Счётчик для пропущенных монстров|
class Enemy(GameSprite):
    def update(self):
        global lost
        w = 80
        h = 60
        if self.rect.y <= 500:
            self.rect.y += self.speed
        else:
            global lost        #|Чтобы переменная нигде не потерялась|
            lost += 1          #|Изменение переменной, при достижении монстра нижней границы|
            self.rect.y = 0
            self.rect.x = randint(10, 650)
#--------------------------------------
#Подкласс для пуль                    |
#--------------------------------------
class Bullets(GameSprite):
    def update(self):
        if self.rect.y <= 500:
            self.rect.y -= self.speed
        else:
            self.kill()
#--------------------------------------
#Подкласс для астероидов              |
#--------------------------------------
class Asteroids(GameSprite):
    def update(self):
        if self.rect.y <= 500:
            self.rect.y += self.speed
        else:
            self.rect.y = 0
            self.rect.x = randint(10, 650)
#--------------------------------------
#Группа астероидов                    |
#--------------------------------------
asteroids = sprite.Group()
for i in range (4):
    x = randint (10, 650)
    speed = randint(1, 2)
    asteroid = Asteroids('asteroid.png', x, 0, speed, 60, 60)
    asteroids.add(asteroid)
#--------------------------------------
#Группа монстров                      |
#--------------------------------------
monsters = sprite.Group()
for i in range (6):
    x = randint (10, 650)
    speed = randint(1, 3)
    monster = Enemy('ufo.png', x, 0, speed, 60, 60)
    monsters.add(monster)
#--------------------------------------
#Объекты                              |
#--------------------------------------
window = display.set_mode((700, 500))
display.set_caption('Шутер')

font.init()

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
player = Player('rocket.png', 10, 420, 10, 60, 80)

clock = time.Clock()
FPS = 60

Clip_bullets = 10
counter1 = 0

font = font.SysFont('Arial', 36)
win = font.render('YOU WIN!', True, (250, 250, 0))
lose = font.render('YOU LOSE!', True, (250, 250, 0))
counter_kills = font.render('Счёт: ' + str(counter1), True, (250, 250, 250))
counter_misses = font.render('Пропущено: ' + str(lost), True, (250, 250, 250))
score_clip = font.render('Патроны: ' + str(Clip_bullets), True, (250, 250, 250))
#--------------------------------------
#Игровой цикл                          |
#--------------------------------------
finish = False
game = True
while game:
    window.blit(background,(0,0))
    clock.tick(FPS)

    for e in event.get():
        if e.type == QUIT: #|Реакция на выход по крестику|
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_s:
                if Clip_bullets != 0:
                    player.fire()                                     #|Ограничение по патронам в обойме|
                    Clip_bullets = Clip_bullets = Clip_bullets - 1
            if e.key == K_r:
                Clip_bullets = 10               #|Перезарядка обоймы|

    if finish != True:
        
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        sprites_list4 = sprite.groupcollide(asteroids, bullets, False, True)
        for m in sprites_list:                   #|Счетчик убитых монстров|
            counter1 = counter1 + 1
            x = randint (10, 650)
            speed = randint(1, 3)                 #|Тут мы добавляем нового монстра взамен того, что только умер|
            monster = Enemy('ufo.png', x, 0, speed, 60, 60)
            monsters.add(monster)
    
        window.blit(counter_misses, (0, 40))                    #|Пишем еще раз для того, чтобы счётчик постоянно обновлялся|
        counter_misses = font.render('Пропущено: ' + str(lost), True, (250, 250, 250))

        window.blit(counter_kills, (0, 10))
        counter_kills = font.render('Счёт: ' + str(counter1), True, (250, 250, 250))

        window.blit(score_clip, (0, 70))
        score_clip = font.render('Патроны: ' + str(Clip_bullets), True, (250, 250, 250))

        
        player.reset()
        player.move()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        bullets.draw(window)
        asteroids.update()
        asteroids.draw(window)

        sprites_list2 = sprite.spritecollide(player, monsters, False)
        for m in sprites_list2:
            window.blit(lose, (300, 200))
            finish = True

        sprites_list3 = sprite.spritecollide(player, asteroids, False)
        for m in sprites_list3:
            window.blit(lose, (300, 200))
            finish = True

        if counter1 >= 10:
            window.blit(win, (300, 200))
            finish = True
                
        if lost >= 5:
            window.blit(lose, (300, 200))
            finish = True

        display.update()

#|Конец: 05.05.2021|
#\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\/\
#>:3
#|'._____________________________________.|