import pygame

IMAGE_DIR = "images/"
DIM = (150, 135) # Dimensions of the spaceship sprite
BDIM = (10, 30)


class Bullet:
    def __init__(self, id, ship_x, ship_y):
        self.id = id
        self.x = ship_x + DIM[0] / 2 - BDIM[0] / 2
        self.y = ship_y - 20
        self.speed = 100

    def draw(self, win, clientId):
        if clientId == self.id:
            sprite = f"{IMAGE_DIR}/bullet.png"
        else:
            sprite = f"{IMAGE_DIR}/bullet2.png"

        loaded_sprite = pygame.image.load(sprite)
        win.blit(loaded_sprite, (self.x, self.y))

    def check_hit(self, game, clientId):
        spaceship = game.spaceships[clientId]
        if (self.y + BDIM[1] > spaceship.y + DIM[1] // 2 and spaceship.x - BDIM[0] <= self.x <= spaceship.x + DIM[0] and self.id != spaceship.id):
            aspaceship = game.spaceships[spaceship.id]
            aspaceship.hp -= 1
            return aspaceship

    def update(self, clientId):
        if clientId == self.id:
            self.y -= self.speed

        else:
            self.y += self.speed




class SpaceShip:
    def __init__(self, p, clientId):
        self.id = clientId
        self.width = DIM[0]
        self.height = DIM[1]
        self.speed = 3
        self.hp = 10
        self.cooldown = 500
        self.last = 0

        if p == 0:
            self.sprite = f"{IMAGE_DIR}/nave.png"
            self.x = round((1200 / 2) - (self.width / 2))
            self.y = round(900 * 0.98 - self.height)

        else:
            self.sprite = f"{IMAGE_DIR}/nave2.png"
            self.x = round((1200 / 2) - (self.width / 2))
            self.y = round(900 * 0.02)

        self.rect = (self.x, self.x + self.width, self.y, self.y + self.width)

    def draw(self, win):
        loaded_sprite = pygame.image.load(self.sprite)
        win.blit(loaded_sprite, (self.x, self.y))

    def move(self):
        keys = pygame.key.get_pressed()

        if self.rect[1] < 1200 and keys[pygame.K_RIGHT]:
            self.x += self.speed
            self.rect = (self.x, self.x + self.width, self.y, self.y + self.width)

        if self.rect[0] > 0 and keys[pygame.K_LEFT]:
            self.x -= self.speed
            self.rect = (self.x, self.x + self.width, self.y, self.y + self.width)

    def shoot(self, bullet_l, n):
        keys = pygame.key.get_pressed()

        now = pygame.time.get_ticks()
        diff = abs(now - self.last)

        if keys[pygame.K_SPACE] and diff >= self.cooldown:
            bullet_l.append(Bullet(self.id, self.x, self.y))
            self.last = now

            return n.communicate(Bullet(self.id, self.x, self.y))







