
from Controller import Uno
from player import Player
import os
import sys
class Game:
    def __init__(self):
        #Initialize current Game instance and Give Game Controller desired number of NPC player"
        print("how many players? min=2 max=4")
        try:
            self.playersNum = int(input("players[2]:"))
            if self.playersNum >4 or self.playersNum<2:
                print("invalid num of players ")
                print("players setting as 2")
                self.playersNum = 2

        except ValueError:
            self.playersNum=2
        self.uno_core = Uno(self.playersNum)
        self.player :Player = self.uno_core.getMyPlayer()
    def update(self):
        self.player=self.uno_core.getMyPlayer()

    def loop(self):

        while self.uno_core.running:
            try:
                self.clear()
                self.printPlayersCards()
                self.printCurrentCard()
                res=self.prompt()
                self.uno_core.sendCard(res)
            except KeyboardInterrupt:
                print("\n.... closing Game ....\nbye👋")
                sys.exit(0)
    def clear(self):
        #os.system("clear")
        print("\n"*2)
        #print('''
       #       ============================||
       #     ||   4   0    6   6    9979    ||
        #    ||   0   4    69  6   9    9   ||
       #     ||   4   5    6 6 9   5    9   ||
       #     ||    4444    4  66    9939    ||
        #      ============================||
        #    ''')
        print("\n"*2)

    #prints ops details
    def printPlayersCards(self):
        players=self.uno_core.getUpdate()
        for player in players:
            if player["name"]!="Player 0":
                print(f'{player["name"]} has {player["cardsCount"]} cards\n{player["cards"]}')

    def giveCard(self,index):
        card=self.player.cards[index]
        return card
        
    def printCurrentCard(self):
        print(self.coloured(self.uno_core.CurrentCard))

    

    def prompt(self):
        print("Play your card:")
        self.render_cards()
        loop=True
        while loop:
            try:
                num=int(input(f"pick[1-{len(self.player.cards)+1}]: "))
                
                if num>=1 and num<=(len(self.player.cards)+1):
                    if self.uno_core.isValid(self.player.cards[num-1]):
                        loop=False
                        return num-1
                    else:
                        print(self.red("card incompatibl\ndraw if you don't have !!!"))
                else:
                    print(self.red(f"please pick a number between[1-{len(self.player.cards)+1}]"))
            
            except ValueError:
                print(self.red(f"please pick a number !!!"))
            
    #player Options
    def render_cards(self):
        for index,card in enumerate(self.player.cards):
            print(f"{index+1} {self.coloured(card)}")
        print(f"{len(self.player.cards)+1} draw (from stack)")

 
    # call the colour functions in relative to the given card colour
    def coloured(self,cards):
        try:
            clr,card=cards.split("|")
        except ValueError:
            clr=None;
            card=cards

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
    # red colour coder     
    def red(self,data):
        return f"\033[91m {data} \033[00m"
    # green colour coder 
    def green(self,data):
        return f"\033[92m {data} \033[00m"
    # yellow colour coder 
    def yellow(self,data):
        return f"\033[93m {data} \033[00m"

    # blue colour coder 
    def blue(self,data):
        return f"\033[94m {data} \033[00m"


if __name__=="__main__":
    Game().loop()