import socket
from sys import exit

HOST = '127.0.0.1'
PORT = 65431

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT))
    except:
        print(f'No server on port {PORT}')
        print("Server not found")
        print("Please chaeck wether the server program is running or not.")
        print("Else try checking the port values in client and server")
        exit(1)

    x = input("Enter the name of road(A, B, C, D) : ")
    s.sendall(x.encode('utf-8'))

    data = s.recv(1024).decode('utf-8')
    total_cycles = int(data)
    timestamp = 1        
    
    while True:
        if timestamp<=total_cycles:
            x=input('Enter the cars arriving(A1A2) : ')
            s.sendall(x.encode('utf-8'))
        signals = s.recv(2048)
        if not signals:
            break
        print("Timestamp", timestamp)
        print(signals.decode('utf-8'))
        timestamp += 1
