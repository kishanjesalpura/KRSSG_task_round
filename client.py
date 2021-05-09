import socket

HOST = "127.0.0.1"
PORT = 65432

ROUNDS = 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(2048)
        data = data.decode('utf-8')
        if len(data)==0:
            break

        if ',' in data:
            cards = list(data.split(', '))
            cards = [int(x) for x in cards]
            temp = []
            for x in cards:
                if x%13 == 0:
                    temp.append(13)
                else:
                    temp.append(x%13)
            print("cards recieved are: ", temp)
            max_card = 0
            for card in cards:
                if card%13==0:
                    max_card = 13
                    break
                elif card%13 > max_card:
                    max_card = card%13
            s.sendall(str(max_card).encode('utf-8'))
        else:
            print(data)
