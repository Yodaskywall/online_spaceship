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

games = {
    0: Game(0)
}

clock = pygame.time.Clock()


def main_loop(gameId):
    while True:
        clock.tick(60)
        try:
            for bullet in games[gameId].bullets:
                bullet.update("server")
                if not -30 <= bullet.y <= 900:
                    games[gameId].bullets.remove(bullet)
        except Exception as e:
            print(e)


def threaded_client(conn, clientId, gameId):
    games[gameId].connected[clientId] = True
    game = games[gameId]
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
            games[gameId].spaceships[data.id] = data

        elif data == "Waiting":
            pass

        elif data == "Lost":
            games[gameId].lost[clientId] = True
            reply = games[gameId]
            pickle_send(conn, reply)
            print(f"Connection with {clientId} terminated.")
            conn.close()
            connected = False
            break


        else:
            bullet = data
            bullet.x = (1200 - bullet.x - 10)
            bullet.y = (900 - bullet.y - 30)
            games[gameId].bullets.append(bullet)

        to_remove = []

        for bullet in game.bullets:
            sp = bullet.check_hit(game, clientId)
            if sp is not None:
                games[gameId].spaceships[clientId] = sp
                to_remove.append(bullet)

        for bullet in to_remove:
            games[gameId].bullets.remove(bullet)

        reply = games[gameId]
        pickle_send(conn, reply)

        connected = not game.finished()
        if not connected:
            conn.close()
            print(f"Connection with {clientId} terminated.")



gameId = 0
clientId = 0


while True:
    conn, address = s.accept()
    print(f"Connected to {address}.")

    start_new_thread(threaded_client, (conn, clientId, gameId))
    print(f"{clientId} connected to server {gameId}")
    if clientId == 0:
        start_new_thread(main_loop, (gameId,))

    clientId += 1

    if clientId == 2:
        clientId = 0
        gameId += 1
        games[gameId] = Game(gameId)


