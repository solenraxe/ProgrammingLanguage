import pygame as pg
import os
from tkinter import filedialog as fd
import pyperclip
import interpreter as inter
import memory

scriptExists = os.path.exists("script.txt")
if not scriptExists:
    with open("script.txt", "w") as f:
        f.write("print Hello, World!")

pg.init()
pg.font.init()

comicSans = pg.font.SysFont("Comic Sans MS", 18)

displayInfo = pg.display.Info()
WIDTH, HEIGHT = 800, 600

screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()

icon = pg.image.load("SolPy.png")
pg.display.set_caption("SolPy Editor")
pg.display.set_icon(icon)

previous = []
text = ""
lineNumber = 0
with open("script.txt", "r") as f:
    text = f.read()
    lineNumber = text.count("\n")

previous.append(text)

deleting = 0
moveDir = 0
editIndex = len(text)

LINE_HEIGHT = 26
TEXT_X = 75
TEXT_Y = 60
LINE_NUM_X = 50

scrollOffset = 0

mainWindow = pg.Rect(20, 50, WIDTH - 40, HEIGHT - 70)
consoleRect = pg.Rect(40, HEIGHT - 210, WIDTH - 80, 170)
consoleTextPos = [50, HEIGHT - 200]

def run(text):
    print("Running code...")
    memory.clear()
    memory.setVar("console", "Console :")
    lines = text.split("\n")
    inter.currentScript = lines
    inter.currentLine = 0
    for i, line in enumerate(lines):
        inter.runLine(line, i)
        inter.currentLine = i

def toggleFullscreen():
    if pg.display.get_window_size() == (WIDTH, HEIGHT):
        pg.display.set_mode((displayInfo.current_w, displayInfo.current_h), pg.FULLSCREEN)
        mainWindow.width = displayInfo.current_w - 40
        mainWindow.height = displayInfo.current_h - 70
        consoleRect.width = displayInfo.current_w - 80
        consoleRect.y = displayInfo.current_h - 210
        consoleTextPos[1] = displayInfo.current_h - 200
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
    global text, editIndex, lineNumber, scrollOffset
    text = ""
    editIndex = 0
    lineNumber = 0
    scrollOffset = 0
    memory.setVar("console", "Console :")

def loadFile():
    global text, lineNumber, editIndex, scrollOffset
    filetypes = (
        ('text files', '*.txt'),
        ('All files', '*.*')
    )
    file = fd.askopenfile(filetypes=filetypes)

    if file:
        text = file.read()
        lineNumber = text.count("\n")
        editIndex = len(text)
        scrollOffset = 0

def getVisibleLineCount():
    return max(1, (mainWindow.height - (TEXT_Y - mainWindow.y) - consoleRect.height - 20) // LINE_HEIGHT)

def getCursorLineCol(text, editIndex):
    before = text[:editIndex]
    line = before.count("\n")
    lastNewline = before.rfind("\n")
    col = editIndex - (lastNewline + 1)
    return line, col

def clampScroll():
    global scrollOffset
    lines = text.split("\n")
    visible = getVisibleLineCount()
    maxScroll = max(0, len(lines) - visible)
    if scrollOffset > maxScroll:
        scrollOffset = maxScroll
    if scrollOffset < 0:
        scrollOffset = 0

def ensureCursorVisible():
    global scrollOffset
    cursorLine, _ = getCursorLineCol(text, editIndex)
    visible = getVisibleLineCount()
    if cursorLine < scrollOffset:
        scrollOffset = cursorLine
    elif cursorLine > scrollOffset + visible - 1:
        scrollOffset = cursorLine - visible + 1
    clampScroll()

class Button():
    def __init__(self, x, y, width, height, text, onClick):
        self.rect = pg.Rect(x, y, width, height)
        self.text = text
        self.onClick = onClick

    def draw(self):
        pg.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=5)
        textSurface = comicSans.render(self.text, True, (255, 255, 255))
        textRect = textSurface.get_rect(center=self.rect.center)
        screen.blit(textSurface, textRect)

    def checkClick(self, pos):
        if self.rect.collidepoint(pos):
            self.onClick()

buttonsList = []

buttonsList.append(Button(20, 10, 100, 30, "Save (F2)", lambda: save()))
buttonsList.append(Button(130, 10, 100, 30, "Load (F8)", lambda: loadFile()))
buttonsList.append(Button(240, 10, 100, 30, "Clear (F3)", lambda: clear()))
buttonsList.append(Button(350, 10, 100, 30, "Run (F9)", lambda: run(text)))
buttonsList.append(Button(460, 10, 150, 30, "Fullscreen (F11)", lambda: toggleFullscreen()))

ctrlPressed = False
frameCount = 0
running = True
while running:
    frameCount += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                ctrlPressed = True
            elif event.key == pg.K_BACKSPACE:
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
                cursorLine, cursorCol = getCursorLineCol(text, editIndex)
                if cursorLine > 0:
                    lines = text.split("\n")
                    targetCol = min(cursorCol, len(lines[cursorLine - 1]))
                    newIndex = sum(len(l) + 1 for l in lines[:cursorLine - 1]) + targetCol
                    editIndex = newIndex
            elif event.key == pg.K_DOWN:
                cursorLine, cursorCol = getCursorLineCol(text, editIndex)
                lines = text.split("\n")
                if cursorLine < len(lines) - 1:
                    targetCol = min(cursorCol, len(lines[cursorLine + 1]))
                    newIndex = sum(len(l) + 1 for l in lines[:cursorLine + 1]) + targetCol
                    editIndex = newIndex
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
            elif (event.unicode and not ctrlPressed) or event.unicode == "#":
                text = text[:editIndex] + event.unicode + text[editIndex:]
                editIndex += 1
                lineNumber = text.count("\n")
            elif event.key == pg.K_z:
                if not ctrlPressed or len(previous) < 1: continue
                text = previous[-1]
                if editIndex > len(text): editIndex = len(text)
                previous.pop()
                lineNumber = text.count("\n")
            elif event.key == pg.K_v:
                if not ctrlPressed: continue
                clipBoard = pyperclip.paste()
                text = text[:editIndex] + clipBoard + text[editIndex:]
                editIndex += len(clipBoard)
                lineNumber = text.count("\n")
            elif event.key == pg.K_s:
                if not ctrlPressed: continue
                save()

            ensureCursorVisible()

        elif event.type == pg.KEYUP:
            if event.key == pg.K_BACKSPACE:
                deleting = 0
            elif event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                moveDir = 0
            elif event.key == pg.K_LCTRL or event.key == pg.K_RCTRL:
                ctrlPressed = False

        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                for button in buttonsList:
                    button.checkClick(event.pos)
                
                if mainWindow.collidepoint(event.pos):
                    cursorLine = min((event.pos[1] - 50)//LINE_HEIGHT + scrollOffset, lineNumber)
                    lines = text.split("\n")
                    lineWidth, _ = comicSans.size(lines[cursorLine])
                    if lineWidth != 0:
                        cursorCol = min(round((event.pos[0] - TEXT_X)/lineWidth*len(lines[cursorLine])), len(lines[cursorLine]))
                    else:
                        cursorCol = 0
                    newIndex = sum(len(l) + 1 for l in lines[:cursorLine]) + cursorCol
                    editIndex = newIndex

        elif event.type == pg.MOUSEWHEEL:
            if mainWindow.collidepoint(pg.mouse.get_pos()):
                scrollOffset -= event.y
                clampScroll()

    if deleting > 0: deleting += 1
    if frameCount % 6 == 0 and deleting > 0:
        repeat = 1
        if deleting > 24: repeat = round(deleting/24)
        text = text[:editIndex-repeat] + text[editIndex:]
        editIndex = max(0, editIndex - repeat)
        lineNumber = text.count("\n")
        ensureCursorVisible()
    if frameCount % 8 == 0 and moveDir != 0:
        editIndex = max(0, min(len(text), editIndex + moveDir))
        ensureCursorVisible()

    if frameCount % 60 == 0 and len(previous) >= 1:
        if previous[-1] != text:
            previous.append(text)
            if len(previous) > 600:
                previous = previous[-600:]

    screen.fill((0, 0, 0))

    pg.draw.rect(screen, (255, 255, 255), mainWindow, 2, border_radius=5)

    cursorLine, cursorCol = getCursorLineCol(text, editIndex)
    lines = text.split("\n")
    blinkOn = frameCount % 60 < 35

    visible = getVisibleLineCount()
    clampScroll()

    oldClip = screen.get_clip()
    clipRect = pg.Rect(mainWindow.x + 2, mainWindow.y + 2, mainWindow.width - 4, mainWindow.height - 4)
    screen.set_clip(clipRect)

    for i in range(scrollOffset, min(len(lines), scrollOffset + visible + 1)):
        lineText = lines[i]
        if i == cursorLine:
            if blinkOn:
                lineText = lineText[:cursorCol] + "|" + lineText[cursorCol:]
            else:
                lineText = lineText[:cursorCol] + " " + lineText[cursorCol:]

        y = TEXT_Y + (i - scrollOffset) * LINE_HEIGHT
        rendered_text = comicSans.render(lineText, True, (255, 255, 255))
        screen.blit(rendered_text, (TEXT_X, y))

    screen.set_clip(oldClip)

    lineNumClip = pg.Rect(mainWindow.x + 2, mainWindow.y + 2, mainWindow.width - 4, mainWindow.height - 4)
    screen.set_clip(lineNumClip)
    for i in range(scrollOffset, min(len(lines), scrollOffset + visible + 1)):
        y = TEXT_Y + (i - scrollOffset) * LINE_HEIGHT
        number_text = comicSans.render(str(i+1) + ".", True, (255, 255, 255))
        screen.blit(number_text, (LINE_NUM_X, y))
    screen.set_clip(oldClip)

    pg.draw.rect(screen, (255, 255, 255), consoleRect, 2, border_radius=5)
    consoleText = comicSans.render(memory.getVar("console"), True, (255, 255, 255))
    screen.blit(consoleText, consoleTextPos)

    for button in buttonsList:
        button.draw()

    pg.display.flip()
    clock.tick(60)

pg.quit()