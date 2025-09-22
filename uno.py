import random as rdm
import socket as sk


class Uno:
    def __init__(self):
        self.colours = ["R","G","B","Y"]
        self.wildcards = ["SKIP","REV","PICKUPx2"]
        self.sock = sk.socket(sk.AF_INET6,sk.SOCK_STREAM)
        
        self.deck = [f"{x}|{i}" for x in self.colours for i in range (1,10) for _ in range(2)]
        self.deck.extend([f"{x}|0" for x in self.colours ])
        self.deck.extend([f"{x}|{y}" for y in self.wildcards for x in self.colours for _ in range(2)])
        self.deck.extend(["CHANGE" for i in range(4)])
        self.deck.extend(["CHANGE|x4" for i in range(4)])
        self.shuffle_deck()

        self.connect()

    def connect(self):
        self.sock.bind((self.obtain_ip(),7777))
        self.sock.listen()

        while True:
            client=self.sock.accept()
    def run(self):
        pass
        

    def obtain_ip(self):
        return sk.gethostbyaddr(sk.gethostname())[2][0]
    
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
print(len(Uno().deck))

