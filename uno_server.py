import socket as sk
import threading

PORT=8889


import random as rdm
import socket as sk
import os


class Uno_server:
    def __init__(self):
        self.colours = ["R","G","B","Y"]
        self.wildcards = ["SKIP","REV","PICKUPx2"]
        self.sock = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        
        self.deck = [f"{x}|{i}" for x in self.colours for i in range (1,10) for _ in range(2)]
        self.deck.extend([f"{x}|0" for x in self.colours ])
        self.deck.extend([f"{x}|{y}" for y in self.wildcards for x in self.colours for _ in range(2)])
        self.deck.extend(["CHANGE" for i in range(4)])
        self.deck.extend(["CHANGE|x4" for i in range(4)])
        self.shuffle_deck()
        self.players=[]

        self.start()
    def startingCards(self):
        startings= self.deck[-8:]
        self.deck = self.deck[:-8]
        return startings

    def handle(self,addr:sk.socket):
        self.players.append(addr)
        addr.send("Hi, welcome to Uno".encode())
        addr.send(f"your cards \n {', '.join(self.startingCards())}".encode())
        print(len(self.deck))


    def start(self):
        self.sock.bind((self.obtain_ip(),PORT))

        while True:
            self.sock.listen()
            addr,_ = self.sock.accept()
            self.handle(addr)

    def run(self):
        pass
        

    def obtain_ip(self):
       #value =input("ipaddr:")
       #return value
       return sk.gethostbyname(sk.gethostname())
    
    def shuffle_deck(self):
        rdm.shuffle(self.deck)

    def generate_deck(self):
        pass
    def red(data):
        return f"\033[91m{data}\033[00m"

    def green(data):
        return f"\033[92m{data}\033[00m"

    def yellow(data):
        return f"\033[93m{data}\033[00m"


    def blue(data):
        return f"\033[94m{data}\033[00m"


if __name__ == "__main__":
    Uno_server()