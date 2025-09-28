
class Player:
    def __init__(self,startingCards:list,index=0,npc=True):
        self.npc =npc
        self.name=f"Player {index}"
        self.cards=startingCards
        self.CurrentCard=None
       
    def card_count(self):
        return len(self.cards)
    def __repr__(self):
        return f"name {self.name} Cards:{len(self.cards)} npc :{self.npc}"
    def winning_message(self):
        message=""
        if self.npc:
            message=f"!!! {self.name} Has Won !!!"
        else:
            message="!!! You Have Won !!"
        return message


