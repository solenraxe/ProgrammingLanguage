import pygame as pg
import os
from tkinter import filedialog as fd
import interpreter as inter
import memory

scriptExists = os.path.exists("script.txt")
if not scriptExists:
    with open("script.txt", "w") as f:
        f.write("print Hello, World!")

pg.init()
pg.font.init()

comicSans = pg.font.SysFont("Comic Sans MS", 18)

display_info = pg.display.Info()
WIDTH, HEIGHT = 800, 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

icon = pg.image.load("SolPy.png")
pg.display.set_caption("SolPy Editor")
pg.display.set_icon(icon)

text = ""
lineNumber = 0
with open("script.txt", "r") as f:
    text = f.read()
    lineNumber = text.count("\n")

deleting = 0
moveDir = 0
editIndex = len(text)

mainWindow = pg.Rect(20, 50, WIDTH - 40, HEIGHT - 70)
consoleRect = pg.Rect(40, HEIGHT - 210, WIDTH - 80, 170)
consoleTextPos = [50, HEIGHT - 200]

def run(text):
    print("Running code...")
    memory.clear()
    lines = text.split("\n")
    inter.currentScript = lines
    inter.currentLine = 0
    for i, line in enumerate(lines):
        inter.runLine(line, i)
        inter.currentLine = i

def toggleFullscreen():
    if pg.display.get_window_size() == (WIDTH, HEIGHT):
        pg.display.set_mode((display_info.current_w, display_info.current_h), pg.FULLSCREEN)
        mainWindow.width = display_info.current_w - 40
        mainWindow.height = display_info.current_h - 70
        consoleRect.width = display_info.current_w - 80
        consoleRect.y = display_info.current_h - 210
        consoleTextPos[1] = display_info.current_h - 200
    else:
        pg.display.set_mode((WIDTH, HEIGHT))
        mainWindow.width = WIDTH - 40
        mainWindow.height = HEIGHT - 70
        consoleRect.width = WIDTH - 80
        consoleRect.y = HEIGHT - 210
        consoleTextPos[1] = HEIGHT - 200

def save():
    print("Saving script...")
    with open("script.txt", "w") as f:
        f.write(text)

def clear():
    global text, editIndex, lineNumber
    text = ""
    editIndex = 0
    lineNumber = 0

def loadFile():
    global text, lineNumber, editIndex
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    file = fd.askopenfile(filetypes=filetypes)

    if file:
        text = file.read()
        lineNumber = text.count("\n")
        editIndex = len(text)

class Button():
    def __init__(self, x, y, width, height, text, onClick):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.onClick = onClick

    def draw(self):
        pg.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=5)
        text_surface = comicSans.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def checkClick(self, pos):
        if self.rect.collidepoint(pos):
            self.onClick()

buttonsList = []

buttonsList.append(Button(20, 10, 100, 30, "Save (F2)", lambda: save()))
buttonsList.append(Button(130, 10, 100, 30, "Load (F8)", lambda: loadFile()))
buttonsList.append(Button(240, 10, 100, 30, "Clear (F3)", lambda: clear()))
buttonsList.append(Button(350, 10, 100, 30, "Run (F9)", lambda: run(text)))
buttonsList.append(Button(460, 10, 150, 30, "Fullscreen (F11)", lambda: toggleFullscreen()))

framecount = 0
running = True
while running:
    framecount += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_BACKSPACE:
                deleting = 1
            elif event.key == pg.K_RETURN:
                text = text[:editIndex] + "\n" + text[editIndex:]
                lineNumber += 1
                editIndex += 1
            elif event.key == pg.K_TAB:
                text = text[:editIndex] + "- " + text[editIndex:]
                editIndex += 2
            elif event.key == pg.K_LEFT:
                moveDir = -1
            elif event.key == pg.K_RIGHT:
                moveDir = 1
            elif event.key == pg.K_UP:
                for i in range(editIndex-1, -1, -1):
                    if text[i] == "\n":
                        editIndex = i
                        break
            elif event.key == pg.K_DOWN:
                newIndex = text.find("\n", editIndex)
                if newIndex > -1:
                    editIndex = newIndex + 1
            elif event.key == pg.K_F9:
                run(text)
            elif event.key == pg.K_F11:
                toggleFullscreen()
            elif event.key == pg.K_F2:
                save()
            elif event.key == pg.K_F3:
                clear()
            elif event.key == pg.K_F8:
                loadFile()
            elif event.unicode:
                text = text[:editIndex] + event.unicode + text[editIndex:]
                editIndex += 1
                
        elif event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                deleting = 0
            elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                moveDir = 0

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttonsList:
                    button.checkClick(event.pos)

    if deleting > 0: deleting += 1
    if framecount % 6 == 0 and deleting > 0:
        repeat = 1
        if deleting > 24: repeat = round(deleting/24)
        text = text[:editIndex-repeat] + text[editIndex:]
        editIndex = max(0, editIndex - repeat)
        lineNumber = text.count("\n")
    if framecount % 6 == 0 and moveDir != 0:
        editIndex = max(0, min(len(text), editIndex + moveDir))

    screen.fill((0, 0, 0))

    pg.draw.rect(screen, (255, 255, 255), mainWindow, 2, border_radius=5)

    text_to_render = text[:editIndex] + "|" + text[editIndex:] if framecount % 60 < 35 else text
    rendered_text = comicSans.render(text_to_render, True, (255, 255, 255))
    screen.blit(rendered_text, (75, 60))

    for i in range(lineNumber+1):
        number_text = comicSans.render(str(i+1) + ".", True, (255, 255, 255))
        screen.blit(number_text, (50, 60 + i * 26))

    pg.draw.rect(screen, (255, 255, 255), consoleRect, 2, border_radius=5)
    console_text = comicSans.render(memory.getVar("console"), True, (255, 255, 255))
    screen.blit(console_text, consoleTextPos)

    for button in buttonsList:
        button.draw()

    pg.display.flip()
    clock.tick(60)

pg.quit()
