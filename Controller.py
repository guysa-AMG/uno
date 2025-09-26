import socket as sk
import threading
from player import Player

from time import sleep

import random as rdm
import os
STARTING_CARDS=-7
SLPTME=0.5
class Uno:
    def __init__(self,num_players):
        
        starting,self.deck=self.generate_deck()
        self.shuffle_deck()
        self.players=self.initPlayers(num_players)
        self._CurrentCard=starting
        self.totalPlayers=len(self.players)
        self.winner=None
        self.prevUsedCards=[]
        self._isComplete=False
        
    #ensure before rewriting the current card it should reused when deck completes
    def RecycleCard(self):
        self.prevUsedCards.append(self._CurrentCard)
    def print(self,data):
        print(f"\t{data}")
        
    def isComplete(self):
        if self._isComplete:
            winner :Player=self.winner
            if winner.npc:
                self.print(f"{winner.name} has played {self.coloured(winner.CurrentCard)}")
                self.print(f"\t🎉 {winner.name} Has Won 🎉\n")
            else:
                self.print(f"\t🎉 You Have Won 🎉\n")
        return self._isComplete
       
    def recycleUsedCards(self):
        self.deck.extend(self.prevUsedCards)
        self.prevUsedCards=[]
        self.shuffle_deck()

    def initPlayers(self,cnt:int):
        players =[Player(startingCards=self.startingCards(),index=index) for index in range(2,cnt+1)]
        players.append(Player(startingCards=self.startingCards(),npc=False))
        return players

    def pullCard(self):
       
        len_of_deck=len(self.deck)
        if len_of_deck <=1:
            self.recycleUsedCards()
        card=self.deck.pop()
        return card
    
    def getMyPlayer(self):
        for player in self.players:
            if not player.npc:
                return player
   
    def getUpdate(self):
        data=[]
        for player in self.players:
            cardCount=len(player.cards)
            if player.npc:
                data.append(player)
        return data
        
    def startingCards(self):
        startings= self.deck[STARTING_CARDS:]
        self.deck = self.deck[:STARTING_CARDS]
        return startings
    def test(self):
        pass
    def shuffle_deck(self):
        
        rdm.shuffle(self.deck)

    def generate_deck(self):
        colours = ["R","G","B","Y"]
        wildcards = ["SKIP","REV","PICKUPx2"]
        deck = [f"{x}|{i}" for x in colours for i in range (1,10) for _ in range(2)]
        deck.extend([f"{x}|0" for x in colours ])
        rdm.shuffle(deck)
        startingDeck=deck.pop()
        deck.extend([f"{x}|{y}" for y in wildcards for x in colours for _ in range(2)])
        deck.extend(["CHANGE" for i in range(4)])
        deck.extend(["CHANGEx4" for i in range(4)])
        return startingDeck,deck
    def CurrentCard(self):
        return self._CurrentCard
    def getHumanPlayerIndex(self):
        for index in range(len(self.players)):
            if not self.players[index].npc:
                return index
    
    def isValid(self,card):
        ret=False
        sep="|"

        if sep in card:
            cardColour,cardValue=card.split(sep)
            if sep in self._CurrentCard:
                CurrentCardColour,CurrentCardValue=self._CurrentCard.split(sep)
                if CurrentCardColour == cardColour or CurrentCardValue == cardValue:
                    ret=True
        elif card.startswith("CHANGE"):
            return True
        
        return ret
            

    def getfreqColour(self,cards):
        lst={}
        for card in cards:
            if "|" in card:
                clr,_=card.split("|")
                try:
                    lst[clr]+=1
                except:
                    lst[clr]=1
        self.print(lst)
        maxv=max(list(lst.values()))
        self.print(maxv)
        for key in lst:
            if lst[key] == maxv:
                return key
        return None
    
    def setCurrent(self,card,uid):
        self.RecycleCard()
        self.players[uid].CurrentCard=card
        self._CurrentCard=card

    def checkStatus(self,PlayerIndex):
        if len(self.players[PlayerIndex].cards)==0 and self.winner == None:
            self.winner=self.players[PlayerIndex]
            self._isComplete=True
            return True
        else:
            return False
    
    #npc move executor the function plays valid moves in context to the current
    def npc_play(self,playerIndex):
        for index in range(len(self.players[playerIndex].cards)):
            
            if self.isValid(self.players[playerIndex].cards[index]):
                if self.players[playerIndex].cards[index].startswith("CHANGE"):
                    colour=self.getfreqColour(self.players[playerIndex].cards)
       
                    self.setCurrent(colour+"|Wild CARD",playerIndex)
                    if self.players[playerIndex].cards[index].endswith("x4"):
                        self.pickupCard((playerIndex+1),4)
                elif self.players[playerIndex].cards[index].endswith("PICKUPx2"):
                    self.pickupCard(playerIndex+1,2)

                else:
                    self.setCurrent(self.players[playerIndex].cards[index],playerIndex)

                self.removePlayerCard(index,playerIndex)
                self.checkStatus(playerIndex)
                return
        self.pickupCard(playerIndex)
     
    #changes the current game state    
    def react(self,playerIndex):
        sleep(SLPTME)
        
        if self._CurrentCard.endswith("REV"):
            self.players.reverse()
            playerIndex=self.getHumanPlayerIndex()+1

        elif self._CurrentCard.endswith("SKIP"):
            playerIndex=self.getHumanPlayerIndex()+2

        playerIndex%=self.totalPlayers

        self.npc_play(playerIndex=playerIndex)

        hidx = self.getHumanPlayerIndex()
        if (current_index:=((playerIndex+1)%self.totalPlayers)) != hidx:
            self.react(current_index)
        
    #reads the humans given value and calls the game state to be updated
    def sendCard(self,cardIndex):
        playerIndex = self.getHumanPlayerIndex()
        cards=self.players[self.getHumanPlayerIndex()].cards
        if len(cards)==cardIndex:
            self.pickupCard(playerIndex)
        else:
            
            self.setCurrent(self.players[self.getHumanPlayerIndex()].cards[cardIndex],self.getHumanPlayerIndex())
            self.removePlayerCard(cardIndex,playerIndex)
            if self._CurrentCard=="CHANGE":
                self.changeColourWildCard(playerIndex)
            elif self._CurrentCard == "CHANGEx4":
                self.changeColourWildCard(playerIndex)
                self.pickupCard(playerIndex+1,4)
            if self.checkStatus(playerIndex):
                return     

        self.react(playerIndex+1)
    
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

    def changeColourWildCard(self,uid):
        colours=["Red","Green","Blue","Yellow"]
        [self.print(f"{inx+1} {clr}\n") for inx,clr in enumerate(colours)]
        error=True
        while error:
            try:
                res=int(input("\tpick Color [1-4]"))
                if res>=1 and res<=4:
                    error=False
                    self.setCurrent(colours[res-1][0]+"|WILD CARD",uid)
            except ValueError:
                pass
    #draws and num amount of cards for Player at PlayerIndex
    def pickupCard(self,playerIndex,num=1)        :
        playerIndex%=self.totalPlayers
        self.print(f"{self.players[playerIndex].name} has picked {num} cards")
              
        playerIndex%=self.totalPlayers
        for _ in range(num):
            self.players[playerIndex].cards.append(self.pullCard())
    #remove given card from player stack
    def removePlayerCard(self,cardIndex,playerIndex):
        newDeck=self.players[playerIndex].cards[:cardIndex]
        newDeck.extend(self.players[playerIndex].cards[cardIndex+1:])
        self.players[playerIndex].cards=newDeck
        
if __name__ == "__main__":
    print(Uno(4).getfreqColour(['Y|1', 'G|4', 'CHANGE','B|2', 'R|1', 'Y|2', 'G|3', 'G|4', 'Y|PICKUPx2']))