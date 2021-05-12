# This is a special client that connects to the server first 
# and sends the number clients and number of rounds to the server

import socket
from sys import exit

HOST = "127.0.0.1"
PORT = 12346

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
    # connects to the server
    try:
        client.connect((HOST, PORT))
    except:
        exit(1)

    # Taking inputs for the server
    no_of_players = int(input("Enter the number of players : "))
    no_of_rounds = int(input("Enter the number of rounds : "))
    
    # pings the user again if the input given is not possible
    while no_of_rounds%no_of_players == 0:
        no_of_rounds = int(input("Number or rounds divisible by total players\nPls try again : "))
    data = str(no_of_players)+" , "+str(no_of_rounds)
    client.sendall(data.encode('utf-8'))