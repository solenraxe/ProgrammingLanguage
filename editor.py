import pygame as pg
import os
import interpreter as inter
import memory

scriptExists = os.path.exists("script.txt")
if not scriptExists:
    with open("script.txt", "w") as f:
        f.write("print Hello, World!")

pg.init()
pg.font.init()

comicSans = pg.font.SysFont("Comic Sans MS", 20)

WIDTH, HEIGHT = 800, 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

icon = pg.image.load("SolPy.png")
pg.display.set_caption("SolPy")
pg.display.set_icon(icon)

text = ""
with open("script.txt", "r") as f:
    text = f.read()
lineNumber = 0

deleting = False
editIndex = len(text)

def run(text):
    print("Running code...")
    memory.clear()
    lines = text.split("\n")
    inter.currentScript = lines
    inter.currentLine = 0
    for line in lines:
        inter.runLine(line)
        inter.currentLine += 1

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
                text = text[:editIndex] + "\n" + text[editIndex:]
                lineNumber += 1
                editIndex += 1
            elif event.key == pg.K_TAB:
                text = text[:editIndex] + "- " + text[editIndex:]
                editIndex += 2
            elif event.key == pg.K_LEFT:
                editIndex = max(0, editIndex - 1)
            elif event.key == pg.K_RIGHT:
                editIndex = min(len(text), editIndex + 1)
            elif event.key == pg.K_LCTRL:
                run(text)
            elif event.unicode:
                text = text[:editIndex] + event.unicode + text[editIndex:]
                editIndex += 1
                
        elif event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                deleting = False

    if framecount % 6 == 0 and deleting:
        text = text[:editIndex-1] + text[editIndex:]
        editIndex = max(0, editIndex - 1)

    screen.fill((0, 0, 0))
    text_to_render = text[:editIndex] + "|" + text[editIndex:] if framecount % 60 < 35 else text
    rendered_text = comicSans.render(text_to_render, True, (255, 255, 255))
    screen.blit(rendered_text, (50, 20))

    for i in range(lineNumber+1):
        number_text = comicSans.render(str(i+1) + ".", True, (255, 255, 255))
        screen.blit(number_text, (20, 20 + i * 28))

    console_text = comicSans.render(memory.getVar("console"), True, (255, 255, 255))
    screen.blit(console_text, (50, HEIGHT - 180))

    pg.display.flip()
    clock.tick(60)

pg.quit()

with open("script.txt", "w") as f:
    f.write(text)