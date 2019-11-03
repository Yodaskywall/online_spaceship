import socket
from _thread import start_new_thread
from network import pickle_receive, pickle_send
from spaceship import SpaceShip
from game import Game
import pygame

HEADERSIZE = 10

server = "192.168.1.108"
port = 25565

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))

except socket.error as e:
    print(e)

s.listen()
print("Waiting for a connection, Server Started.")

game = Game()

clock = pygame.time.Clock()


def main_loop():
    while True:
        clock.tick(60)
        try:
            for bullet in game.bullets:
                bullet.update("server")
                if not -30 <= bullet.y <= 900:
                    game.bullets.remove(bullet)
        except Exception as e:
            print(e)


def threaded_client(conn, clientId):
    pickle_send(conn, [clientId, game])

    connected = True

    while connected:
        data = pickle_receive(conn)

        if isinstance(data, SpaceShip):
            try:
                if data.x != game.spaceships[data.id].x:
                    pass
            except:
                pass
            game.spaceships[data.id] = data

        else:
            bullet = data
            bullet.x = (1200 - bullet.x - 10)
            bullet.y = (900 - bullet.y - 30)
            game.bullets.append(bullet)

        to_remove = []

        for bullet in game.bullets:
            a = bullet.check_hit(game, clientId)
            if a is not None:
                game.spaceships[clientId] = a
                to_remove.append(bullet)

        for bullet in to_remove:
            game.bullets.remove(bullet)



        reply = game
        pickle_send(conn, reply)




serverId = 0
clientId = 0





while True:
    conn, address = s.accept()
    print(f"Connected to {address}.")

    start_new_thread(threaded_client, (conn, clientId))
    print(clientId)
    if clientId == 0:
        start_new_thread(main_loop, ())

    clientId += 1

    if clientId == 2:
        clientId = 0


