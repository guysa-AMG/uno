
class Player:
    def __init__(self,startingCards:list,index=0,npc=True):
        self.npc =npc
        self.name=f"Player {index}"
        self.cards=startingCards
        self.CurrentCard=None
       
    def card_count(self):
        return len(self.cards)
    

