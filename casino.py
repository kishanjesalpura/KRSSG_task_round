import socket
import threading
import random
import concurrent.futures

HOST = "127.0.0.1"
PORT = 65432
TOT_PLAYERS = 3
DECK_SIZE = 52
ROUNDS = 4


def card_provider(l):
    cards = []
    while len(cards) != l:
        new_card = random.randrange(1, DECK_SIZE+1)
        if new_card not in cards:
            cards.append(new_card)
    return cards

conn_list = []
addr_list = []

def game_manager(connections, addresses):
    winner_list = []
    counter = 1
    while True:
        dist_deck = card_provider

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(TOT_PLAYERS)
    for _ in range(TOT_PLAYERS):
        conn, addr = s.accept()
        conn_list.append(conn)
        addr_list.append(addr)
        print("connected to:", addr)
    game_manager(conn_list, addr_list)
    


def clientmanager(conn):
    with conn:
        print("connected to ", conn)
        counter = 0
        while True:
            counter += 1
            cards = card_provider()
            encoded_cards = cards.encode('utf-8')
            conn.sendall(encoded_cards)
            max_card = conn.recv(1024)
            print("The recieved card is", max_card.decode('utf-8'))
            if counter % 4 == 0:
                c = input("Cycle completed!\nDo you want to continue?(y/n): ")
                if c.lower() != 'y':
                    break
