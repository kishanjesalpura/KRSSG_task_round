import socket

HOST = "127.0.0.1"
PORT = 65432

ROUNDS = 4

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    counter = 0
    while True:
        data = s.recv(2048)
        data = data.decode('utf-8')
        if len(data)==0:
            break
        if counter==ROUNDS:
            print(data)
            counter=0
        else:
            cards = list(data.split(', '))
            cards = [int(x) for x in cards]
            temp = []
            for x in cards:
                if x%13 == 0:
                    temp.append(13)
                else:
                    temp.append(x%13)
            print("cards recieved are: ", temp)
            max_card = max(temp)
            s.sendall(str(max_card).encode('utf-8'))
            counter+=1
        
        