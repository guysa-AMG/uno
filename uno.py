
from Controller import Uno
from player import Player
from modules import check_requirements
from card import Card
import os
import sys
import random as rdm
from utils import Button,Text,ColorPicker
MAX=6
check_requirements()
import pygame as gmi
STARTING_CARDS=-7
class Game:

    def __init__(self):
        
        #Initialize current Game instance and Give Game Controller desired number of NPC player"
       
        #self.uno_core = Uno(self.playersNum)
        #self.player :Player = self.uno_core.getMyPlayer()
        
        self.currentCard,self.deck=self.generate_deck()
        self.shuffle_deck()
        self.players=[]
        self.NumPlayers=2
        self.pygame_init()
   
    def pygame_init(self):
        gmi.init()
      
        self.widgets=[]
        self.screen=gmi.display.set_mode((850,1000),gmi.VIDEORESIZE|gmi.RESIZABLE)
        w,h=self.screen.get_size()
      
        self.PlayerSelectScreen()

    def startingCards(self):
        
        startings= self.deck[STARTING_CARDS:]
        self.deck = self.deck[:STARTING_CARDS]
        
        return startings  
     
    def startScreen(self):
        play=False
        w,h=self.screen.get_size()
        btn=Button(screen=self.screen,text="Start",pos=((w//2)-30,(h//2)-30),sz=(180,60))
        txt=Text(screen=self.screen,obj="Welcome To Uno!",pos=((w//2),(h//2)),sz=50)
        end=False
        while not play:
            self.refresh()
            x,y=self.screen.get_size()
            for event in gmi.event.get():
                if event.type is gmi.QUIT:
                    play=True
                    end=True
                elif event.type == gmi.MOUSEBUTTONDOWN:
                    if btn.onClick(event.pos,print):
                        play=True
            txt.draw(((x//2)-(txt.width//2),y//2-(txt.height//2)-50))
            btn.draw(((x//2)-(btn.rect.width//2),y//2-(btn.rect.height//2)+50),fnt_sz=40)
            gmi.display.flip()
        if end:
            sys.exit(0)
        self.PlayerSelectScreen()
    
    def PlayerSelectScreen(self):
        play=False
        w,h=self.screen.get_size()
        txt=Text(screen=self.screen,obj="Select Players",pos=((w//2),(h//2)),sz=50)
        input=[Button(screen=self.screen,text=f"{num} Players",pos=((w//2)-30,(h//2)-30),sz=(180,60)) for num in range(2,5)]
        end=False
        while not play:
            self.refresh()
            x,y=self.screen.get_size()
            for event in gmi.event.get():
                if event.type is gmi.QUIT:
                    play=True
                    end=True
                elif event.type == gmi.MOUSEBUTTONDOWN:
                    for btn in input:
                        if btn.onClick(event.pos,self.handle_btn):
                            play=True
            txt.draw(((x//2)-(txt.width//2),y//2-(txt.height//2)-70))
            for num,btn in enumerate(input):
                btn.draw(((x//2)-(btn.rect.width//2),y//2-(btn.rect.height//2)+(70*(num))),fnt_sz=40)
            gmi.display.flip()
        
        if end:
            sys.exit(0)
        self.createNpcs(self.NumPlayers)
        self.loop()
  
    def shuffle_deck(self):
        rdm.shuffle(self.deck)

    def generate_deck(self):
        colours = ["R","G","B","Y"]
        wildcards = ["R","S","x2"]
        deck = [Card(str(i),f"{x}|{i}") for x in colours for i in range (1,10) for _ in range(2)]
        deck.extend([Card("0",f"{x}|0") for x in colours ])
        rdm.shuffle(deck)
        startingDeck=deck.pop()
        deck.extend([Card(y,f"{x}|{y}") for y in wildcards for x in colours for _ in range(2)])
        deck.extend([Card("*","*") for i in range(4)])
        deck.extend([Card("*x4","*x4") for i in range(4)])
        startingDeck.turn()
        return startingDeck,deck
    
    def createNpcs(self,count):
        for index in range(2,count+1):
            if index <3:
                p_deck=self.startingCards()
            else:
                p_deck=[]
                for crd in self.startingCards():
                    crd.rotate(angle=-90 if index==3 else 90)
                    p_deck.append(crd)
            
            pl=Player(p_deck,index)
            
            self.players.append(pl)
        self.my_cards=[card for card in self.startingCards() if not card.turn() ]

        self.players.append(Player(self.my_cards,1,npc=False))

    def refresh(self):
       
        self.screen.fill((255,255,255))
 
    def eventRunner(self,val):
        for event in gmi.event.get():
            if event.type == gmi.QUIT:
                val=False
                
            elif event.type ==gmi.MOUSEBUTTONDOWN:
                for widget in self.widgets:
                    widget.onClick(event.pos,self.handle_btn)

    def handle_btn(self,data:str):
        print(f"{data} clicked")
        if data.endswith("players"):
            self.NumPlayers=int(data.split(" ")[0])
            

   
    def loop(self):
        kill=False
        while not kill:
            
            self.refresh()
            self.render()
                
            for event in gmi.event.get():
                if event.type ==gmi.QUIT:
                    kill=True
                if event.type == gmi.MOUSEBUTTONDOWN:
                    self.onclick(event.pos)
    def isValid(self,c:Card):
        sep = "|"        
        if sep in c.card:
            new_Color,newValue=c.card.split(sep)
            currentColour,currentValue=self.currentCard.card.split(sep)
            if currentColour == new_Color or currentValue == newValue:
                return True
        
        elif c.card.startswith("*"):
            return True
        return False

           

    def onclick(self,pos):
        for card in self.my_cards:
            card:Card
            if card.isClicked(pos):
                if card.card.startswith("*"):
                    self.colorPicker()
                    return
                elif self.isValid(card):
                    self.currentCard=card
                    self.my_cards.remove(card)
                
        if self.deck[-1].isClicked(pos):
            card=self.deck.pop()
            card.turn()
            self.my_cards.append(card)

                
                
    def colorPicker(self):
        ColorPicker(self.screen)


    def render(self):
        #os.system("clear")
        font=gmi.font.SysFont("Liberation Mono Bold.ttf",50)
        font_surface = font.render("  UNO  ",True,(255,255,255),(255,0,0))
        
        w,h=self.screen.get_size()
        self.screen.fill((255,255,255),gmi.Rect(0,0,w,h))
       
        self.screen.blit(font_surface,(w//2,10),gmi.Rect(0,0,w,50))
        [card.draw(self.screen,((w//2)-(150),(h//2)-(70))) for card in self.deck]

        for player in self.players:
            player :Player
            
            if player.name == "Player 1":
                [c.draw(self.screen,(((w//2)-(len(player.cards)*30))+(i*60),h-150)) for i,c in enumerate(player.cards)]
            elif player.name == "Player 2":
                [c.draw(self.screen,(((w//2)-(len(player.cards)*30))+(i*60),-50)) for i,c in enumerate(player.cards)]
            elif player.name == "Player 3":
                
                [c.draw(self.screen,(-50,((h//2)-((len(player.cards)*30))+(i*60)))) for i,c in enumerate(player.cards) ]
            elif player.name == "Player 4":
                [c.draw(self.screen,(w-100,((h//2)-((len(player.cards)*30))+(i*60)))) for i,c in enumerate(player.cards) ]
        
        self.currentCard.draw(self.screen,(w//2-(self.currentCard.width//2),(h//2)-(self.currentCard.height//2)))
        gmi.display.flip()
      
     


    #self.prints ops details

    
    def printWinner(self):
        return self.uno_core.winner
    
    def checkIfWon(self):
        self.uno_core.checkStatus(self.uno_core.getHumanPlayerIndex())

   

if __name__=="__main__":
    try:
        Game()
    except SystemExit:
        gmi.quit()



class Original:

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
        

