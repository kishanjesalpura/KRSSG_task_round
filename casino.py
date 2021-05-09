import socket
import threading
import random
import concurrent.futures

HOST = "127.0.0.1"
PORT = 65432
TOT_PLAYERS = 3
DECK_SIZE = 52
ROUNDS = 4
CARDS_PER_PLAYER = 3


def card_provider(l):
    cards = []
    while len(cards) != l:
        new_card = random.randrange(1, DECK_SIZE+1)
        if new_card not in cards:
            cards.append(new_card)
    lst_to_return = []
    for x in range(TOT_PLAYERS):
        l = cards[x*CARDS_PER_PLAYER: (x+1)*CARDS_PER_PLAYER]
        lst_to_return.append(str(l)[1:-1])
    return lst_to_return

conn_list = []
addr_list = []
win_counts = {'A':0, 'B':0, 'C':0}
players = ['A', 'B', 'C']

def game_manager(connections, addresses):
    round_counter = 1
    while True:
        dist_deck = card_provider(CARDS_PER_PLAYER*TOT_PLAYERS)
        with concurrent.futures.ThreadPoolExecutor() as executor:
            p_moves = executor.map(client_manager, conn_list, dist_deck)
            max_val = 0
            idx = 0
            for val in p_moves:
                if val > max_val:
                    max_idx = [idx]
                    max_val = val
                elif val == max_val:
                    max_idx.append(idx)
                idx += 1
        if len(max_idx)==1:
            print("Player", players[max_idx[0]], "wins round", round_counter)
            win_counts[players[max_idx[0]]] += 1
        else:
            print("Tie betweeen players", end = ' ')
            for plyr in max_idx:
                print(players[plyr], end = ' ')
                win_counts[players[plyr]] += 1
            print("In round", )
        if round_counter % ROUNDS == 0:
            max_val=0
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
            for con in conn_list:
                con.sendall(msg.encode('utf-8'))
            c = input("Cycle completed!\nDo you want to continue?(y/n): ")
            if c.strip().lower() != 'y':
                break
            round_counter = 1
            for x in win_counts:
                win_counts[x] = 0
            continue
        round_counter+=1

def client_manager(connection, dist_deck):
    connection.sendall(str(dist_deck).encode('utf-8'))
    card = connection.recv(1024)
    return (int(card.decode('utf-8')))

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(TOT_PLAYERS)
    for _ in range(TOT_PLAYERS):
        conn, addr = s.accept()
        conn_list.append(conn)
        addr_list.append(addr)
        print("connected to:", addr)
    game_manager(conn_list, addr_list)
