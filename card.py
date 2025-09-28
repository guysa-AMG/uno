import pygame
class Card:
    def __init__(self,name,card,visible=True,size=None):
        self.name = name
        self.card=card
        self.visible=visible
        pygame.font.init()
        self._font=pygame.font.SysFont(None,50)
        
        if visible:
            self.colorCode(card)
        else:
            self.color=(0,0,0)
            self.value="?"
        self.width=80
        self.height=150
        self.card_Surface = self._font.render(self.value,True,(0,0,0))
      
       

        if size is not None:
            self.width,self.height=size
        
    def turn(self):
        return
        if self.visible:
            self.color=(0,0,0)
            self.value="?"
            self.visible=False
        else:
            self.colorCode(self.card)
            self.visible=True

    def rotate(self,angle):
        self.width,self.height=self.height,self.width
        
    def update(self,card):
        self.card=card
        self.colorCode(card)

     
        
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
            self.card_Surface = self._font.render(self.value,True,(0,0,0))

        else:
            self.color=(0,0,0)
            self.value=card
        

    def draw(self,screen,updated):

        
        self.rect=pygame.Rect(updated[0],updated[1],self.width,self.height)
        
        cl,ct=(self.rect.left+(self.width//2),self.rect.top+(self.height//2))
        
        pygame.draw.rect(screen,self.color,self.rect,0,3)

        if not self.visible:
            pygame.draw.rect(screen,(255,255,255),self.rect,2,1)
        else:
            pygame.draw.rect(screen,(0,0,0),self.rect,2,1)

        pygame.draw.circle(screen,(255,255,255),(cl,ct),25)
        w,h=self._font.size(self.value)
        cl,ct=(cl-(w//2),ct-(h//2))
        screen.blit(self.card_Surface,pygame.Rect(cl,ct,10,10))
    def isClicked(self,pos):
        return self.rect.collidepoint(pos)
    def isHover(self,pos):
        if self.rect.collidepoint(pos):
            self.rect.top-=30
    


    
