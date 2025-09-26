
from Controller import Uno
from player import Player
from modules import check_requirements
import os
import sys
MAX=6
check_requirements()
import pygame

class Game:

    def __init__(self):

        #Initialize current Game instance and Give Game Controller desired number of NPC player"
        self.print(f"how many players? min=2 max={MAX}")
        try:
            self.playersNum = int(input("players[2]:"))
            if self.playersNum >MAX or self.playersNum<2:
                self.print("invalid num of players ")
                self.print("players setting as 2")
                self.playersNum = 2

        except ValueError:
            self.playersNum=2
        self.uno_core = Uno(self.playersNum)
        self.player :Player = self.uno_core.getMyPlayer()
    def update(self):
        self.player=self.uno_core.getMyPlayer()

    def loop(self):

        while not self.uno_core.isComplete():
            try:
                self.clear()
                self.printPlayersCards()
                self.printCurrentCard()
                res=self.prompt()
                self.uno_core.sendCard(res)
            except KeyboardInterrupt:
                self.print("\t\n.... closing Game ....\t\nbye👋")
                sys.exit(0)
    def printTitle(self,data):
        print(self.bg_red(data))

         

    def clear(self):
        os.system("clear")
        self.print("\n"*2)
        self.printTitle('''
\t============================||
\t||   4   0    6   6    9979    ||
\t||   0   4    69  6   9    9   ||
\t||   4   5    6 6 9   5    9   ||
\t||    4444    4  66    9939    ||
\t============================||''')
        self.print("\n"*2)

    #self.prints ops details
    def printPlayersCards(self):
        players=self.uno_core.getUpdate()
        for player in players:
            if player.npc:
                self.print(f'{player.name} has played {self.coloured(player.CurrentCard)} and has {player.card_count()} cards')

    def print(self,data):
        print(f"\t{data}")
        
    def giveCard(self,index):
        card=self.player.cards[index]
        return card
        
    def printCurrentCard(self):
        self.print(f'''
                        Current Card    
                                                         
                        |{self.coloured(self.uno_core.CurrentCard())}|
                                                                  
                            ''')

    
    def printWinner(self):
        return self.uno_core.winner
    
    def checkIfWon(self):
        self.uno_core.checkStatus(self.uno_core.getHumanPlayerIndex())

    def prompt(self):
      
        
        self.print("\tPlay your card:")

        self.render_cards()
        loop=True
        while loop:
            try:
                inpt=input(f"\tpick[1-{len(self.player.cards)+1}]: ")
                if inpt.strip(" ").lower() =="exit":
                    raise KeyboardInterrupt
                num=int(inpt)
                
                if num>=1 and num<=(len(self.player.cards)+1):
                    ##below is for when they pick the last option which is Draw from deck
                    if (len(self.player.cards)+1)==num:
                        loop=False
                        return num-1
                    
                    if self.uno_core.isValid(self.player.cards[num-1]):
                        loop=False
                        return num-1
                    else:
                        self.print(self.red("card incompatible\t\t\ndraw if you don't have !!!"))
                else:
                    self.print(self.red(f"please pick a number between[1-{len(self.player.cards)+1}]"))
            
            except ValueError:
                self.print(self.red(f"please pick a number !!!"))
            
    #player Options
    def render_cards(self):
        for index,card in enumerate(self.player.cards):
            self.print(f"{index+1} {self.coloured(card)}")
        self.print(f"{len(self.player.cards)+1} draw (from stack)")

    # call the colour functions in relative to the given card colour
    def coloured(self,cards):
        if cards == None:
            return cards
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
    def bg_red(self,data):
        return f"\033[41m{data}\033[00m"

if __name__=="__main__":
    Game().loop()