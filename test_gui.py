import pygame as gm
from utils import Button,Text
from pygamepopup.menu_manager import MenuManager
from pygamepopup.components import Button as Btn,InfoBox
import pygamepopup as pygmp




def handle_btn(data):
    print(f"{data} clicked")
    
suma,sumb=gm.init()
pygmp.init()
screen=gm.display.set_mode((400,300),gm.RESIZABLE)
mm=MenuManager(screen)
w,h=screen.get_size()

gm.display.set_caption("UNO game")
btn=Button(screen=screen,text="Start",pos=((w//2)-30,(h//2)-30),sz=(60,30))
txt=Text(screen=screen,obj="Welcome To Uno!",pos=((w//2),(h//2)),sz=50)
bol=True

dialog = InfoBox("Select",
                 [
                     [
                         Btn(callback=handle_btn,title="Hi There")
                     ]
                 ])
mm.open_menu(dialog)
while bol:
    for event in gm.event.get():
        if event.type == gm.QUIT:
            bol=False
        elif event.type ==gm.MOUSEBUTTONDOWN:
            btn.onClick(event.pos,handle_btn)
    screen.fill((255,255,255))
    w,h=screen.get_size()
    btn.draw()
    txt.draw((w//2,h//2))
  
    gm.display.flip()
    
gm.quit()
