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

comicSans = pg.font.SysFont("Comic Sans MS", 18)

display_info = pg.display.Info()
WIDTH, HEIGHT = 800, 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

icon = pg.image.load("SolPy.png")
pg.display.set_caption("SolPy")
pg.display.set_icon(icon)

text = ""
lineNumber = 0
with open("script.txt", "r") as f:
    text = f.read()
    lineNumber = text.count("\n")

deleting = False
moveDir = 0
editIndex = len(text)

mainWindow = pg.Rect(20, 50, WIDTH - 40, HEIGHT - 70)
consoleRect = pg.Rect(40, HEIGHT - 210, WIDTH - 80, 170)

def run(text):
    print("Running code...")
    memory.clear()
    lines = text.split("\n")
    inter.currentScript = lines
    inter.currentLine = 0
    for line in lines:
        inter.runLine(line)
        inter.currentLine += 1

def toggleFullscreen():
    if pg.display.get_window_size() == (WIDTH, HEIGHT):
        pg.display.set_mode((display_info.current_w, display_info.current_h), pg.FULLSCREEN)
        mainWindow.width = display_info.current_w - 40
        mainWindow.height = display_info.current_h - 70
        consoleRect.width = display_info.current_w - 80
        consoleRect.y = display_info.current_h - 210
    else:
        pg.display.set_mode((WIDTH, HEIGHT))
        mainWindow.width = WIDTH - 40
        mainWindow.height = HEIGHT - 70
        consoleRect.width = WIDTH - 80
        consoleRect.y = HEIGHT - 210

def save():
    print("Saving script...")
    with open("script.txt", "w") as f:
        f.write(text)

def clear():
    global text, editIndex, lineNumber
    text = ""
    editIndex = 0
    lineNumber = 0

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

buttonsList.append(Button(20, 10, 100, 30, "Run (F9)", lambda: run(text)))
buttonsList.append(Button(130, 10, 150, 30, "Fullscreen (F11)", lambda: toggleFullscreen()))
buttonsList.append(Button(290, 10, 100, 30, "Save (F2)", lambda: save()))
buttonsList.append(Button(400, 10, 100, 30, "Clear (F3)", lambda: clear()))
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
                moveDir = -1
            elif event.key == pg.K_RIGHT:
                moveDir = 1
            elif event.key == pg.K_F9:
                run(text)
            elif event.key == pg.K_F11:
                toggleFullscreen()
            elif event.key == pg.K_F2:
                save()
            elif event.key == pg.K_F3:
                clear()
            elif event.unicode:
                text = text[:editIndex] + event.unicode + text[editIndex:]
                editIndex += 1
                
        elif event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                deleting = False
            elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                moveDir = 0

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttonsList:
                    button.checkClick(event.pos)

    if framecount % 6 == 0 and deleting:
        text = text[:editIndex-1] + text[editIndex:]
        editIndex = max(0, editIndex - 1)
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
    screen.blit(console_text, (50, HEIGHT - 200))

    for button in buttonsList:
        button.draw()

    pg.display.flip()
    clock.tick(60)

pg.quit()