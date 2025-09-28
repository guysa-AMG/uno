

from player import Player
from modules import check_requirements
from card import Card
import sys
from time import sleep
import random as rdm
from utils import Button,Text,ColorPicker
MAX=6
check_requirements()
import pygame as gmi
STARTING_CARDS=-1
class Game:

    def __init__(self):
        
        #Initialize current Game instance and Give Game Controller desired number of NPC player"
       
        #self.uno_core = Uno(self.playersNum)
        #self.player :Player = self.uno_core.getMyPlayer()
        
        self.currentCard,self.deck=self.generate_deck()
        self.shuffle_deck()
        self.players=[]
        self.cpi=0
        self.winner=None
        self.NumPlayers=2
        self.pygame_init()
   
    def pygame_init(self):
        gmi.init()
      
        self.widgets=[]
        self.screen=gmi.display.set_mode((800,600),gmi.VIDEORESIZE|gmi.RESIZABLE)
        w,h=self.screen.get_size()
        

        self.startScreen()

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
                btn.draw(((x//2)-(btn.rect.width//2),y//2-(btn.rect.height//2)+(70*(num))),fnt_sz=20)
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
        self.my_cards=[card for card in self.startingCards() if not card.turn() ]
        self.players.append(Player(self.my_cards,1,npc=False))

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

    def refresh(self):
        self.screen.fill((255,255,255))

    def handle_btn(self,data:str):
        print(f"{data} clicked")
        if data.endswith("players"):
            self.NumPlayers=int(data.split(" ")[0])
    def recycleUsedCards(self):
        self.deck.extend(self.prevUsedCards)
        self.prevUsedCards=[]
        self.shuffle_deck()
    
    def pullCard(self):
       
        len_of_deck=len(self.deck)
        if len_of_deck <=1:
            self.recycleUsedCards()
        card=self.deck.pop()
        return card    

    def loop(self):
        kill=False
        while not kill and not self.checkIfWon():
            self.refresh()
            self.render()
                
            for event in gmi.event.get():
                if event.type ==gmi.QUIT:
                    kill=True
                if event.type == gmi.MOUSEBUTTONDOWN:
                    self.onclick(event.pos)

        if self.winner:
            self.outro()



    def outro(self):
        play=False
        w,h=self.screen.get_size()
        btn=Button(screen=self.screen,text="Play Again",pos=((w//2)-60,(h//2)-30),sz=(180,60))
        txt=Text(screen=self.screen,obj=self.winner.winning_message(),pos=((w//2),(h//2)),sz=60)
        close=Button(screen=self.screen,text="Close",pos=((w//2)+60,(h//2)-30),sz=(180,60))
        
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
                        self.__init__()
                    elif close.onClick(event.pos,print):
                        sys.exit(0)
            txt.draw(((x//2)-(txt.width//2),y//2-(txt.height//2)-50))
            btn.draw(((x//2)-180,y//2-(btn.rect.height//2)+50),fnt_sz=20)
            close.draw(((x//2)+60,y//2-(btn.rect.height//2)+50),fnt_sz=40)
           
            gmi.display.flip()
        if end:
            sys.exit(0)
        self.PlayerSelectScreen()

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

    
    def getfreqColour(self,cards):
        if len(cards)<3:
            return "R"
        lst={}
        for cardClass in cards:
            card=cardClass.card
            if "|" in card:
                clr,_=card.split("|")
                try:
                    lst[clr]+=1
                except:
                    lst[clr]=1
        
        maxv=max(list(lst.values()))
       
        for key in lst:
            if lst[key] == maxv:
                return key
        return None
        
    def nextPlayer(self):
       
        totalplayer=len(self.players)
        self.cpi+=1
        self.cpi%=totalplayer
        print(f"After:{self.players[self.cpi].name}")
        
    def action(self,card,npc=False):
        print("=================")
        print(f"Before:{self.players[self.cpi].name}")
        valid=True
        print(card.card)
        if card.card.startswith("*"):
            if npc:
                clr=self.getfreqColour(self.players[self.cpi].cards)
                self.currentCard.update(f"{clr}|{self.currentCard.value}")
     

            else:
                self.colorPicker()
           
            if card.card.endswith("x4"):
                self.pickup(self.cpi+1,4)
                
            return valid
        elif self.isValid(card):
            total=len(self.players)
            if card.card.endswith("R"):
                print("Reversing")
                current_player=self.players[self.cpi]
                self.players.reverse()
                self.cpi=self.players.index(current_player)
            elif card.card.endswith("S"):
                print("Skipping")
                self.cpi+=1
                self.cpi%=total
            elif card.card.endswith("x2"):
               self.pickup(self.cpi+1,2)
             
            self.currentCard=card
           
        else:
            valid=False
        return valid
            

    def get_human_index(self):
        for num,player in enumerate(self.players):
            if not player.npc:
                return num
            
    def onclick(self,pos):
        my_index=self.get_human_index()
        if self.cpi==my_index:
            for card in self.my_cards:
                if card.isClicked(pos):
                    if self.action(card):
                        self.my_cards.remove(card)
                        self.nextPlayer()
                     
                    
            if self.deck[-1].isClicked(pos):
                card=self.deck.pop()
                card.turn()
                self.my_cards.append(card)
                self.nextPlayer()
        else:
            print("!!! please wait your turn !!!")

    def pickup(self,index,cnt):
        total=len(self.players)
        index%=total
        for _ in range(cnt):

            self.players[index].cards.append(self.pullCard())
                
    def colorPicker(self):
        clr=ColorPicker(self.screen)
       
        self.currentCard.update(f"{clr}|{self.currentCard.value}")
     
    def robot_play(self):
        if self.players[self.cpi].npc:
            player=self.players[self.cpi]
            played=False
            index= self.players.index(player)
            for card in player.cards:
                if self.action(card,npc=True):
                    if self.players[self.cpi]==player:
                        self.players[self.cpi].cards.remove(card)
                    else:
                        self.players[index].cards.remove(card)

                  
                    played=True
                    break
            if not played:
                self.pickup(self.cpi,1)
                print(f"{self.players[self.cpi].name} picked up")

            sleep(1)
            
            self.nextPlayer()
            




    def render(self):
        #os.system("clear")
        font=gmi.font.SysFont("nonosans",50)
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
        self.robot_play()
        self.currentCard.draw(self.screen,(w//2-(self.currentCard.width//2),(h//2)-(self.currentCard.height//2)))
        
        gmi.display.flip()
      
     


    #self.prints ops details

    
    def printWinner(self):
        return self.uno_core.winner
    
    def checkIfWon(self):
        for player in self.players:
            if len(player.cards)==0:
                self.winner=player
                return True
            
        return False


   

if __name__=="__main__":
    try:
        Game()
    except SystemExit:
        gmi.quit()


