import pygame as pg

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

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                text = text[:-1]
            elif event.key == pg.K_RETURN:
                text += "\n"
                lineNumber += 1
            elif event.key == pg.K_TAB:
                text += "    "
            else:
                text += event.unicode

    screen.fill((0, 0, 0))
    rendered_text = comicSans.render(text + "|", True, (255, 255, 255))
    screen.blit(rendered_text, (50, 20))

    for i in range(lineNumber+1):
        number_text = comicSans.render(str(i+1) + ".", True, (255, 255, 255))
        screen.blit(number_text, (20, 20 + i * 28))

    pg.display.flip()
    clock.tick(60)