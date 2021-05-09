import socket
import threading
import random

HOST = "127.0.0.1"
PORT = 1025


def card_provider():
    l = []
    while len(l) != 3:
        new_card = random.randrange(1, 53)
        if new_card not in l:
            l.append(new_card)
    return str(l)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
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
