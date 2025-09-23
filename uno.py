import socket as sk
import threading
from player import Player

from time import sleep

import random as rdm
import socket as sk
import os

SLPTME=0.5
class Uno:
    def __init__(self,num_players):
        
        self.deck=self.generate_deck()
        self.shuffle_deck()
        self.players=self.initPlayers(num_players)
        self.running=True
        self.CurrentCard=self.pullCard()

    def initPlayers(self,cnt:int):
        players =[Player(startingCards=self.startingCards(),index=index) for index in range(2,cnt+1)]
        players.append(Player(startingCards=self.startingCards(),npc=False))
        return players

    def pullCard(self):
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
            data.append({"name":player.name,"cards":cardCount})
        return data
        
    def startingCards(self):
        startings= self.deck[-8:]
        self.deck = self.deck[:-8]
        return startings

    def shuffle_deck(self):
        rdm.shuffle(self.deck)

    def generate_deck(self):
        colours = ["R","G","B","Y"]
        wildcards = ["SKIP","REV","PICKUPx2"]
        deck = [f"{x}|{i}" for x in colours for i in range (1,10) for _ in range(2)]
        deck.extend([f"{x}|0" for x in colours ])
        deck.extend([f"{x}|{y}" for y in wildcards for x in colours for _ in range(2)])
        deck.extend(["CHANGE" for i in range(4)])
        deck.extend(["CHANGEx4" for i in range(4)])
        return deck
    
    def getHumanPlayerIndex(self):
        for index in range(len(self.players)):
            if not self.players[index].npc:
                return index
    
    def isValid(self,card):
        ret=False
        sep="|"

        if sep in card:
            cardColour,cardValue=card.split(sep)
            if sep in self.CurrentCard:
                CurrentCardColour,CurrentCardValue=self.CurrentCard.split(sep)
                if CurrentCardColour == cardColour or CurrentCardValue == cardValue:
                    ret=True
        if card.startswith("CHANGE"):
            ret=True
        return ret
            


        

    def react(self,playerIndex):
        sleep(SLPTME)
        totalPlayers=len(self.players)

        if self.CurrentCard.endswith("REV"):
            self.players.reverse()
            playerIndex=self.getHumanPlayerIndex()+1

        elif self.CurrentCard.endswith("SKIP"):
            playerIndex=self.getHumanPlayerIndex()+2

        playerIndex%=totalPlayers

        for index in range(len(self.players[playerIndex].cards)):
            if self.isValid(self.players[playerIndex].cards[index]):
                self.CurrentCard=self.players[playerIndex].cards[index]
                self.removePlayerCard(index,playerIndex)
                return
        self.pickupCard(playerIndex)

    def sendCard(self,cardIndex):
        playerIndex = self.getHumanPlayerIndex()
        cards=self.players[self.getHumanPlayerIndex()].cards
        if len(cards)==cardIndex:
            self.pickupCard(playerIndex)
        else:
            self.CurrentCard=self.players[self.getHumanPlayerIndex()].cards[cardIndex]
            self.removePlayerCard(cardIndex,playerIndex)
            if self.CurrentCard=="CHANGE":
                self.changeColourWildCard()
            elif self.CurrentCard == "CHANGEx4":
                self.changeColourWildCard()
                for _ in range(4):
                    self.pickupCard(playerIndex+1)
                    

        
        self.react(playerIndex+1)
    def changeColourWildCard(self):
        colours=["Red","Green","Blue","Yellow"]
        [print(f"{inx+1} {clr}\n") for inx,clr in enumerate(colours)]
        error=True
        while error:
            try:
                res=int(input("pick Color [1-4]"))
                if res>=1 and res<=4:
                    error=False
                    self.CurrentCard=colours[res-1][0]+"|Any"
            except ValueError:
                pass
    def pickupCard(self,playerIndex):
        self.players[playerIndex].cards.append(self.pullCard())

    def removePlayerCard(self,cardIndex,playerIndex):
        newDeck=self.players[playerIndex].cards[:cardIndex]
        newDeck.extend(self.players[playerIndex].cards[cardIndex+1:])
        self.players[playerIndex].cards=newDeck
        
if __name__ == "__main__":
    print(Uno(4).generate_deck())