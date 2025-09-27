import pygame
class Card:
    def __init__(self,name,card,npc=True,size=None):
        self.name = name
        self.npc=npc
        if not npc:
            self.colorCode(card)
        else:
            self.color=(0,0,0)
            self.value="?"
        self.width=60
        self.height=120
        font=pygame.font.SysFont("Liberation Mono Bold.ttf",50)
        self.card_Surface = font.render(self.value,True,(0,0,0))

        if size is not None:
            self.width,self.height=size
        
         
       
    def colorCode(self,card):
        sep="|"
        if sep in card:
            color,value=card.split("|")

            if color=="B":
                self.color=(0,0,200)
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
        

    def draw(self,screen,updated):

        

        self.rect=pygame.Rect(updated[0],updated[1],self.width,self.height)
        
        cl,ct=(self.rect.left+(self.width//2),self.rect.top+(self.height//2))
        
        pygame.draw.rect(screen,self.color,self.rect,0,3)

        if self.npc:
            pygame.draw.rect(screen,(255,255,255),self.rect,2,3)
        else:
            pygame.draw.rect(screen,(0,0,0),self.rect,2,3)

        pygame.draw.circle(screen,(255,255,255),(cl,ct),25)
       
        screen.blit(self.card_Surface,pygame.Rect(cl-10,ct-15,10,10))
    def isClicked(self,pos):
        return self.rect.collidepoint(pos)
    def isHover(self,pos):
        if self.rect.collidepoint(pos):
            self.rect.top-=30
    def rotate(self):
        pass


    
