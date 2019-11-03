from network import Network
from spaceship import SpaceShip
import pygame
from time import sleep
from game import Game

pygame.font.init()

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
    lost = False
    while run:
        clock.tick(500)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if game.finished():
            font = pygame.font.SysFont("timesnewroman", 100)
            if game.lost[n.id]:
                text = font.render("You lost!", 1, (255, 255, 255))

            else:
                text = font.render("You won!", 1, (255, 255, 255))

            x_text = WIDTH / 2 - text.get_width() / 2
            y_text = HEIGHT / 2 - text.get_height() / 2
            win.blit(text, (x_text, y_text))
            pygame.display.update()
            sleep(3)
            quit()

        elif game.isready():
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


            #Displays Hp
            font = pygame.font.SysFont("timesnewroman", 50)
            text = font.render(f"HP: {spaceship.hp}", 1, (255, 255, 255))
            x_text = WIDTH * 0.02
            y_text = HEIGHT * 0.02
            win.blit(text, (x_text, y_text))
            pygame.display.update()

            # Sends the spaceship to the server
            game = n.communicate(spaceship)

            if spaceship.hp <= 0:
                game = n.communicate("Lost")


        else:
            font = pygame.font.SysFont("timesnewroman", 100)
            text = font.render("Waiting for player...", 1, (255, 255, 255))
            x_text = WIDTH / 2 - text.get_width() / 2
            y_text = HEIGHT / 2 - text.get_height() / 2
            win.blit(text, (x_text, y_text))
            pygame.display.update()

            game = n.communicate("Waiting")


if __name__ == "__main__":
    main()
