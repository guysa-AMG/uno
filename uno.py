import random as rdm
import socket as sk
import os


class Uno:
    def __init__(self):
        
        self.sock = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
        self.connect()

    def parse(self,data):
        cards=data.split(" ")
        sorted={}
        for i,card in enumerate(cards):
            try:
                colour,unit = card.split("|")
                sorted[i]=self.coloured(unit,colour)
            except ValueError:
               
                sorted[i]=card
            
        print(sorted)

    def coloured(self,card,clr):
        if clr =="G":
            return self.green(card)
        elif clr == "B":
            return self.blue(card)
        elif clr == "R":
            return self.red(card)
        elif clr == "Y":
            return self.yellow(card)
        else:
            return card

    def connect(self):
        
        self.sock.connect((self.obtain_ip(),8889))
        while True:
            data = self.sock.recv(512)
            data=self.parse(data.decode())
            print(data)

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
    def red(self,data):
        return f"\033[91m{data}\033[00m"

    def green(self,data):
        return f"\033[92m{data}\033[00m"

    def yellow(self,data):
        return f"\033[93m{data}\033[00m"


    def blue(self,data):
        return f"\033[94m{data}\033[00m"
print(len(Uno().deck))

print(len(Uno().deck))




inst=sk.socket(sk.AF_INET,sk.SOCK_STREAM)

inst.bind((sk.gethostbyaddr(sk.gethostname())[2][0],PORT))

inst.listen()

print(f"listening to incoming connection on port {PORT}")
available_player=[]

def handle(addr:sk.socket):
    available_player.append(addr)
    
    for user in available_player:
        addr.send("200-Confirm".encode())



while True:
    addr,ret = inst.accept()
    
    handle(addr)

    
