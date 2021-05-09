import socket

HOST = "127.0.0.1"
PORT = 1025

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        cards = s.recv(2048)
        cards = cards.decode('utf-8')
        if len(cards)==0:
            break
        cards = eval(cards)
        print("cards recieved are: ", cards)
        max_card = 1
        for card in cards:
            if card%13==0:
                max_card = 13
                break
            elif card%13 > max_card:
                max_card = card%13
        s.sendall(str(max_card).encode('utf-8'))