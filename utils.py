import pygame as gme
from pygamepopup.menu_manager import MenuManager
from pygamepopup.components import Button as Btn,InfoBox
import pygamepopup
def text(screen,txt,sz,pos,color=(0,0,0)):
    font=gme.font.SysFont("Liberation Mono Bold.ttf",sz)
    surface = font.render(txt,True,color)
    w,h=font.size(txt)
    screen.blit(surface,gme.Rect(pos[0],pos[1],w,h))


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
        self.font=gme.font.SysFont("Liberation Mono Bold.ttf",self.sz)
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
        

    def draw(self,pos=None,fnt_sz=20):
        if pos is not None:
            self.rect.left,self.rect.top=(pos[0],pos[1])
        font=gme.font.SysFont("Liberation Mono Bold.ttf",fnt_sz)

        fw,fh=font.size(self.obj)

        gme.draw.rect(self.screen,self.bg,self.rect,0,3)
        text(self.screen,self.obj,fnt_sz,(self.rect.left+(self.rect.width//2-(fw//2)),self.rect.top+(self.rect.height//2-(fh//2))),self.fg)
    
    
    def onClick(self,pos,func):
        
        if self.rect.collidepoint(pos):
          
            func(self.obj.lower())
            return True
        return False

class ColorPicker:
    def __init__(self,screen):
        self.screen=screen
        x,y=screen.get_size()
        self.surface = gme.Surface((x//2,y//2))
        pygamepopup.init()
        self.menu =MenuManager(screen)
        self.draw()
    

    def draw(self):
        myDialog=InfoBox("Pick a Color",
               [ [
                    Btn(callback=self.handler,title="green",),
                    Btn(callback=self.handler,title="green",)
                ]]
                )
        self.menu.open_menu(myDialog)

    def handler(self,**kwargs):
        self.menu.close_active_menu()
        

        
        x,y=self.screen.get_size()
        w,h=self.surface.get_size()
        gme.draw.rect(self.surface,(255,0,0),gme.Rect(0,0,w//2,h//2))
        gme.draw.rect(self.surface,(255,255,0),gme.Rect(w//2,0,w//2,h//2))
        gme.draw.rect(self.surface,(0,255,0),gme.Rect(0,h//2,w//2,h//2))
        gme.draw.rect(self.surface,(0,0,255),gme.Rect(w//2,h//2,w//2,h//2))
        self.screen.blit(self.surface,gme.Rect(x//2,y//2,700,700))





