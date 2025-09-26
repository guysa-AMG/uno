import pygame
class Card:
    def __init__(self,name,card):
        self.name = name
        self.colorCode(card)
       
    def colorCode(self,card):
        sep="|"
        if sep in card:
            color,value=card.split("|")

            if color=="B":
                self.color=(0,0,255)
            elif color=="G":
                self.color=(0,255,0)
            elif color=="R":
                self.color=(255,0,0)
            elif color=="Y":
                self.color=(255,255,0)
            self.value=value
        else:
            self.color=(0,0,0)
            self.value=card
        

    def draw(self,screen,d):
        pygame.draw.rect(screen,self.color,pygame.Rect(d[0],d[1],30,60),2,3)

    
