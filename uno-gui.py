import pygame as game

game.init()

win = game.display.set_mode((950,800))

loop=True

while loop:

    for ev in game.event.get():
        if ev == game.QUIT:
            loop=False
    win.fill((255,255,255))
  
    game.display.update()

game.quit()