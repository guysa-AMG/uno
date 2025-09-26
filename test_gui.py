import pygame as gm


suma,sumb=gm.init()

screen=gm.display.set_mode((400,300),gm.RESIZABLE)


gm.display.set_caption("UNO game")

bol=True
while bol:
    for event in gm.event.get():
        if event.type == gm.QUIT:
            bol=False
    screen.fill((255,255,255))
    gm.display.flip()
    
gm.quit()
