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
    return cards

conn_list = []
addr_list = []

def game_manager(connections, addresses):
    winner_list = []
    counter = 1
    max_idx = []
    while True:
        dist_deck = card_provider(CARDS_PER_PLAYER*TOT_PLAYERS)
        dist_deck = [dist_deck[x*CARDS_PER_PLAYER:(x+1)*CARDS_PER_PLAYER] for x in range(TOT_PLAYERS)]
        with concurrent.futures.ThreadPoolExecutor() as executor:
            p_moves = executor.map(client_manager, conn_list, dist_deck)
            max_val = 1
            idx = 0
            for val in p_moves:
                print (val)
                if val > max_val:
                    max_idx = [chr(idx+ord('A'))]
                    max_val = val
                elif val == max_val:
                    max_idx.append(chr(idx+ord('A')))
                idx += 1
        if len(max_idx)==1:
            print("Player", max_idx[0], "wins round", counter)
        else:
            print("Tie betweeen players", end = ' ')
            for plyr in max_idx:
                print(plyr, end = ' ')
            print("In round 1")
        counter+=1
        winner_list.append(max_idx)
        if counter % ROUNDS == 0:
            win_lst = [0,0,0,0]
            winnrs = []
            max_val=0
            for rd_wnnrs in winner_list:
                for wnnrs in rd_wnnrs:
                    win_lst[int(ord(wnnrs)-ord('A'))] += 1
            for idx in range(TOT_PLAYERS):
                if win_lst[idx] > max_val:
                    winnrs = [chr(idx+ord('A'))]
                elif win_lst[idx] == max_val:
                    winnrs.append(chr(idx+ord('A')))


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
