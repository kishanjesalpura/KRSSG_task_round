import socket

HOST = "127.0.0.1"
PORT = 65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        cards = s.recv(2048)
        cards = cards.decode('utf-8')
        cards = eval(cards)
        print("cards recieved are: ", cards)
        if 0 in cards:
            max_card = 0
        else:
            max_card = max(cards)
        s.sendall(str(max_card).encode('utf-8'))