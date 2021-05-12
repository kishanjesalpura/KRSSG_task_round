import socket
import threading
import random
from concurrent.futures import ThreadPoolExecutor
from sys import exit

# Some global variables used in the program

# host IPv4 address and port number
HOST = "127.0.0.1"
PORT = 12346

# Game related variables.
# I have used these variables to make the program convenient to change.
TOT_PLAYERS = 3
DECK_SIZE = 52
rounds = 4
CARDS_PER_PLAYER = 3

# These variables store the players game and connection data
conn_list = []
addr_list = []
win_counts = {}
players = []

# Makes a list of random cards.
# The second part converts cards list strings(each string corresponds to one players cards)
# The list of strings is the return value.
def card_provider():

    cards = []
    while len(cards) != TOT_PLAYERS*CARDS_PER_PLAYER:
        new_card = random.randrange(1, DECK_SIZE+1)
        if new_card not in cards:
            cards.append(new_card)
    playerwise_seperated = []

    for x in range(TOT_PLAYERS):
        l = str(cards[x*CARDS_PER_PLAYER: (x+1)*CARDS_PER_PLAYER])
        playerwise_seperated.append(l[1:-1])
    return playerwise_seperated


# Function keeps the track of the total number of rounds 
# calls other fuctions and in short manages the game.
def game_manager():
    round_counter = 1

    while round_counter!=0:
        cards_for_players = card_provider()
        
        #ThreadPoolExecutor is fuction used to execute fuction in threads.
        # Here map  fuction takes the lists and gives their corresponding elements to the fuction
        # And runs that in different threads.
        with ThreadPoolExecutor() as executor:
            p_moves = executor.map(client_manager, conn_list, cards_for_players)
        
        max_card_val = 0
        idx = 0
        #finding the round winner(s) from all the returned cards
        for player_max_card in p_moves:
            if player_max_card > max_card_val:
                max_idx_lst = [idx]
                max_card_val = player_max_card
            elif player_max_card == max_card_val:
                max_idx_lst.append(idx)
            idx += 1

        # Printing message on server terminal
        if len(max_idx_lst)==1:
            print("Player", players[max_idx_lst[0]], "wins round", round_counter)
            win_counts[players[max_idx_lst[0]]] += 1
        else:
            print("Tie betweeen players", end = ' ')
            for idx in max_idx_lst:
                print(players[idx], end = ' ')
                win_counts[players[idx]] += 1
            print("In round", round_counter)

        if round_counter >= rounds:
            # To ask player's consent after all rounds are finished
            round_counter = printing_winners(round_counter)
        else:
            round_counter+=1


# Sending cards to the connection object given and recieving the response
def client_manager(player_conn, cards_to_send):
    player_conn.sendall(str(cards_to_send).encode('utf-8'))
    card = player_conn.recv(1024).decode('utf-8')
    return (int(card))


def printing_winners(round_counter):
    max_val=0
    # Finding all the winners of the game and storing them in a list
    for player in win_counts:
        if win_counts[player] > max_val:
            winnrs = [player]
            max_val = win_counts[player]
        elif win_counts[player] == max_val:
            winnrs.append(player)

    if len(winnrs)==1:
        msg = f"Player {winnrs[0]} wins the game"
    else:
        msg = "Tie betweeen players"
        for plyr in winnrs:
            msg+=" "+plyr
    print(msg)
    msg+="\nCycle completed!\nDo you want to continue?(y/n): "

    # Running thrreads to send the game winner message and asking wether they want to continue or not.
    with ThreadPoolExecutor() as executor:
        p_moves = executor.map(print_and_ask, conn_list, [msg]*TOT_PLAYERS)
    for x in p_moves:
        if not x:
            return 0
    return round_counter+1


# Fuction used for threading in the above function
def print_and_ask(conn, msg):
    conn.sendall(msg.encode('utf-8'))
    response = conn.recv(1024)
    response = int(response.decode('utf-8'))
    if response: 
        return(1)
    

# main programme
if __name__ == "__main__":

    # Starting script to take number of players,
    # and the number of rounds from the user
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except:
            print(f"unable to bind to port {PORT}")
            print("Please try again after some time")
            exit(1)

        s.listen(1)
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024)
            data = data.decode('utf-8').split(' , ')
            TOT_PLAYERS = int(data[0])
            rounds = int(data[1])


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind((HOST, PORT))
        except:
            print(f"unable to bind to port {PORT}")
            print("Please try again after some time")
            exit(1)

        # Connecting to all the players,
        # and sending them their data and totol number of round.
        s.listen(TOT_PLAYERS)
        for a in range(TOT_PLAYERS):
            conn, addr = s.accept()
            conn_list.append(conn)
            addr_list.append(addr)
            print("connected to:", addr)

            win_counts[str(a+1)] = 0
            players.append(str(a+1))
            player_data = str(a+1)+','+str(rounds)
            conn.sendall(player_data.encode('utf-8'))

        game_manager()

    print("Game successfully completed.!")