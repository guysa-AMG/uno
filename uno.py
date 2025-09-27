
from Controller import Uno
from player import Player
from modules import check_requirements
from card import Card
import os
import sys
MAX=6
check_requirements()
import pygame as gmi

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
        self.pygame_init()

    def pygame_init(self):
        gmi.init()
        self.screen=gmi.display.set_mode((850,1000),gmi.VIDEORESIZE|gmi.RESIZABLE)
        w,h=self.screen.get_size()
        self.cards=[]
        self.opsCard=[]
        self.ops2Card=[]
        self.ops4Card=[]
        for i in range(7):
            self.cards.append(Card("s7",f"G|{i}",npc=False))
            self.opsCard.append(Card("player2","Y|5"))
            self.ops2Card.append(Card("player3","Y|5",True,(120,60)))
            self.ops4Card.append(Card("player4","Y|5",True,(120,60)))

        self.currentCard=Card("current","B|8",npc=False)

        
        

    def update(self):
        self.player=self.uno_core.getMyPlayer()

    def loop(self):
        kill=False
        while not kill:
            try:
                self.clear()
                for event in gmi.event.get():
                    if event.type ==gmi.QUIT:
                        kill=True
                    if event.type == gmi.MOUSEBUTTONDOWN:
                        self.onclick(event.pos)
                    if event.type == gmi.MOUSEMOTION:
                        self.onHover(event.pos)
            except KeyboardInterrupt:
                self.print("\t\n.... closing Game ....\t\nbye👋")
                sys.exit(0)
    def onclick(self,pos):
        for card in self.cards:
            card:Card
            if card.isClicked(pos):
                self.currentCard=card
                self.cards.remove(card)
    def onHover(self,pos):
        for card in self.cards:
            card.isHover(pos)
                
                

    def printTitle(self,data):
        print(self.bg_red(data))

         

    def clear(self):
        os.system("clear")
        font=gmi.font.SysFont("Liberation Mono Bold.ttf",50)
        font_surface = font.render("  UNO  ",True,(255,255,255),(255,0,0))
        
        w,h=self.screen.get_size()
        self.screen.fill((255,255,255),gmi.Rect(0,0,w,h))
       
        self.screen.blit(font_surface,(w//2,10),gmi.Rect(0,0,w,50))

        [c.draw(self.screen,(((w/2)-(len(self.cards)*20))+(i*40),h-150)) for i,c in enumerate(self.cards)]
        [c.draw(self.screen,(((w/2)-(len(self.opsCard)*20))+(i*40),-50)) for i,c in enumerate(self.opsCard)]
        [c.draw(self.screen,(-80,((h//2)-((len(self.ops2Card)*20))+(i*40)))) for i,c in enumerate(self.ops2Card) ]
        [c.draw(self.screen,(w-100,((h//2)-((len(self.ops4Card)*20))+(i*40)))) for i,c in enumerate(self.ops4Card) ]
        
        self.currentCard.draw(self.screen,(w//2-(self.currentCard.width//2),(h//2)-(self.currentCard.height//2)))
        gmi.display.flip()
      
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