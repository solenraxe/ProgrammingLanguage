import pygame as pg
import interpreter as inter

pg.init()
pg.font.init()

comicSans = pg.font.SysFont("Comic Sans MS", 20)

WIDTH, HEIGHT = 800, 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

#pg.display.set_caption("Language")
#pg.display.set_icon()

text = ""
lineNumber = 0

deleting = False

def run():
    global text
    lines = text.split("\n")
    for line in lines:
        inter.runLine(line)

framecount = 0
running = True
while running:
    framecount += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                deleting = True
            elif event.key == pg.K_RETURN:
                text += "\n"
                lineNumber += 1
            elif event.key == pg.K_TAB:
                text += "    "
            else:
                text += event.unicode
        elif event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                deleting = False

    if framecount % 4 == 0 and deleting:
        text = text[:-1]

    screen.fill((0, 0, 0))
    text_to_render = text+"|" if framecount % 60 < 30 else text
    rendered_text = comicSans.render(text_to_render, True, (255, 255, 255))
    screen.blit(rendered_text, (50, 20))

    for i in range(lineNumber+1):
        number_text = comicSans.render(str(i+1) + ".", True, (255, 255, 255))
        screen.blit(number_text, (20, 20 + i * 28))

    pg.display.flip()
    clock.tick(60)