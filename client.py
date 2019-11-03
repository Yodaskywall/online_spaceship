import pygame
from network import Network
from spaceship import SpaceShip
import pygame
from game import Game


WIDTH = 1200
HEIGHT = 900


def main():

    # Conncets to the server
    n = Network()
    print("Connected to the server.")
    bullets = []

    game = n.connect()

    # Configures the window
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("SpaceShip Game")

    # Creates the spaceships at the beginning
    if n.id == 0:
        e_id = 1
        spaceship = SpaceShip(0, 0)
        enemy_spaceship = SpaceShip(1, 1)

    else:
        e_id = 0
        spaceship = SpaceShip(0, 1)
        enemy_spaceship = SpaceShip(1, 0)

    clock = pygame.time.Clock()

    # Starts the game loop
    run = True
    while run:
        clock.tick(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # Updates the spaceship
        if game.spaceships[n.id] is not None:
            spaceship = game.spaceships[n.id]
        if game.spaceships[e_id] is not None:
            enemy_spaceship.x = (WIDTH - game.spaceships[e_id].x - enemy_spaceship.width)
            enemy_spaceship.hp = game.spaceships[e_id].hp

        #Updates the bullets

        bullets = game.bullets
        for bullet in bullets:
            if bullet.id == n.id:
                bullet.x = (1200 - bullet.x - 10)
                bullet.y = (900 - bullet.y - 30)

        # Checks for moves
        spaceship.move()
        spaceship.shoot(bullets, n)

        # Draws things
        win.fill((0, 0, 0))
        spaceship.draw(win)
        for bullet in bullets:
            bullet.draw(win, n.id)
        enemy_spaceship.draw(win)
        pygame.display.update()

        # Sends the spaceship to the server
        game = n.communicate(spaceship)

        print(spaceship.hp)
        if spaceship.hp <= 0:
            quit()


if __name__ == "__main__":
    main()
