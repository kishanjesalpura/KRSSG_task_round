import socket
from sys import exit

HOST = "127.0.0.1"
PORT = 65432
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    # Trying to  establish a connection with the server
    try:
        s.connect((HOST, PORT))
    except:
        print(f'No server on port {PORT}')
        print("Server not found")
        print("Please chaeck wether the server program is running or not.")
        print("Else try checking the port values in client and server")
        exit(1)

    # Gets the total numberof rounds and the player name from the server
    print(f"Connected to the server : ('{HOST}', {PORT})")
    player_data = s.recv(1024)
    player_data = player_data.decode('utf-8').split(',')
    ROUNDS = int(player_data[1])
    print("You are player", player_data[0])

    # This loop constantly waits from data from the server.
    # It breaks once it gets a zero bit from the server.
    # It eithre prints the data or processes the data If it is a list of cards.
    counter = 0
    while True:
        data = s.recv(2048)

        # break condition for the loop when zero byte received.
        if not data:
            break
        data = data.decode('utf-8')
        
        # prints the game's final result and then waits for user's consent.
        if counter>=ROUNDS:
            print(data)
            x = input()
            if x.strip().lower() == 'y':
                s.sendall('1'.encode('utf-8'))
            else:
                s.sendall('0'.encode('utf-8'))
            counter -= 1

        # When it receives the cards 
        # then it finds the maximum card and sends it to the server. 
        else:
            cards = list(data.split(', '))
            cards = [int(x) for x in cards]
            temp = []
            for x in cards:
                if x%13 == 0:
                    temp.append(13)
                else:
                    temp.append(x%13)
            max_card = max(temp)
            # prints the current operation.
            print(f"cards recieved are: {temp} ; card sent: {max_card}")
            s.sendall(str(max_card).encode('utf-8'))
            counter+=1

print("Game completed!")