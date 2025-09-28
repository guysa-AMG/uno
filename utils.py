import pygame as gme
from pygame import Rect

import sys
def text(screen,txt,sz,pos,color=(0,0,0)):
    font=gme.font.SysFont("notosans",sz,True)
    surface = font.render(txt,True,color)
    w,h=font.size(txt)
    screen.blit(surface,gme.Rect(pos[0]-(w//2),pos[1]-(h//2),w,h))


class Widget:
    def __init__(self,screen,obj,pos,sz,fg,bg):
        self.fg=fg
        self.bg=bg
        self.screen=screen
        self.obj=obj
        self.pos=pos
        self.sz=sz
        if type(sz) is not int:
            self.rect=gme.Rect(pos[0],pos[1],sz[0],sz[1])

    def draw(self):
        pass
    def onClick(self,pos):
        pass

class Text(Widget):
    def __init__(self, screen, obj, pos, sz,fg=(0,0,0),bg=(255,255,255)):
        super().__init__(screen, obj, pos, sz,fg,bg)
        self.font=gme.font.SysFont("notosans",self.sz,True)
        self.width,self.height=self.font.size(self.obj)
        self.rect=gme.Rect(pos[0],pos[1],self.width,self.height)



    def draw(self,pos=None):
        surface = self.font.render(self.obj,True,self.fg,self.bg)
        
        if pos is not None:
            self.rect.left,self.rect.top=(pos[0],pos[1])

        self.screen.blit(surface,self.rect)

class Button(Widget):
    def __init__(self,screen,text,pos,sz,fg=(255,255,255),bg=(0,0,0)):
        super().__init__(screen,text,pos,sz,fg,bg)
        

    def draw(self,pos=None,fnt_sz=16):
        if pos is not None:
            self.rect.left,self.rect.top=(pos[0],pos[1])
        font=gme.font.SysFont("notosans",fnt_sz,True)

        fw,fh=font.size(self.obj)

        gme.draw.rect(self.screen,self.bg,self.rect,0,3)
        gme.draw.rect(self.screen,(255,255,255),self.rect,2)
        
        text(self.screen,self.obj,fnt_sz,(self.rect.left+(self.rect.width//2),self.rect.top+(self.rect.height//2)),self.fg)
    
    
    def onClick(self,pos,func):
        
        if self.rect.collidepoint(pos):
          
            func(self.obj.lower())
            return True
        return False

class ColorPicker:
    def __init__(self,screen):
        self.screen=screen
        self.x,self.y=self.screen.get_size()
        
        gme.font.init()
        font=gme.font.SysFont("liberationmono",30)
        self.text = font.render("Pick a Colour",True,(0,0,0))
        w,h=font.size("Pick a Colour")
        self.font_rect=gme.Rect(self.x//2,20,w,h)
        self.btns=[]
        self.selected=False
        
        self.colour="Nothing"
        self.draw()

    def draw(self):
       
        while not self.selected:

            self.x,self.y=self.screen.get_size()
            self.screen.fill((255,255,255))
            gme.draw.rect(self.screen,(255,255,255),gme.Rect(0,0,self.x,self.y))
            
            self.draw_Colours()
            text(self.screen,"Pick a Color",40,(self.x//2,20),(255,255,255))
           
            gme.display.flip()
            for event in gme.event.get():
                if event.type==gme.QUIT:
                    sys.exit(0)
                if event.type == gme.MOUSEBUTTONDOWN:
                    for btn in self.btns:
                        if btn.onClick(event.pos,self.handler):
                            self.selected=True
                            break
 

    def handler(self,data):
        self.colour=data
        
    
    def __str__(self):
        return self.colour[0].upper()

    def draw_Colours(self):
        
        w,h=self.screen.get_size()
        colors=[
            {"title":"red","colour":(255,0,0),"pos":(0,0),"size":(w/2,h/2)},
            {"title":"yellow","colour":(255,255,0),"pos":(w/2,0),"size":(w/2,h/2)},
            {"title":"green","colour":(0,255,0),"pos":(0,(h/2)),"size":(w/2,h/2)},
            {"title":"blue","colour":(0,0,255),"pos":(w/2,(h/2)),"size":(w/2,h/2)},
            
            ]
        
        
        surface=self.screen
        bd=2
        for clr in colors:
            self.btns.append(Button(surface,clr["title"],clr["pos"],clr["size"],(255,255,255),clr["colour"]))
        for btn in self.btns:
            btn.draw(fnt_sz=40)
            
           
    
      





