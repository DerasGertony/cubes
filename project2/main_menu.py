import pygame
import sys
import os
import math
from pygame_widgets.mouse import Mouse, MouseState
from pygame_widgets.widget import WidgetBase
from button import Button
import pygame_widgets
from main import main


class Slider(WidgetBase):
    def __init__(self, win, x, y, width, height, **kwargs):
        super().__init__(win, x, y, width, height)
        self.selected = False
        self.min = kwargs.get('min', 0)
        self.max = kwargs.get('max', 30)
        self.step = kwargs.get('step', 1)
        self.colour = kwargs.get('colour', (150, 150, 150))
        self.handleColour = kwargs.get('handleColour', (100, 100, 100))
        self.borderThickness = kwargs.get('borderThickness', 3)
        self.borderColour = kwargs.get('borderColour', (0, 0, 0))
        self.value = self.round(kwargs.get('initial', (self.max + self.min) / 2))
        self.value = max(min(self.value, self.max), self.min)
        self.handleRadius = kwargs.get('handleRadius', int(self._height / 1.3))
            
    def listen(self, events):
        if not self._hidden and not self._disabled:
            mouseState = Mouse.getMouseState()
            x, y = Mouse.getMousePos()
            if self.contains(x, y):
                if mouseState == MouseState.CLICK:
                    self.selected = True

            if mouseState == MouseState.RELEASE:
                self.selected = False
            if self.selected:
                self.value = self.round((x - self._x) / self._width * self.max + self.min)
                self.value = max(min(self.value, self.max), self.min)

    def draw(self):
        if not self._hidden:
            pygame.draw.rect(self.win, self.colour, (self._x, self._y, self._width, self._height))
            circle = (int(self._x + (self.value - self.min) / (self.max - self.min) * (self._width-20)),
                          self._y, 20, self._height)
            pygame.draw.rect(self.win, self.handleColour, circle, self.handleRadius // 2)


    def contains(self, x, y):
        handleX = int(self._x + (self.value - self.min) / (self.max - self.min) * (self._width-20))
        handleY = self._y + self._height // 2
        if math.sqrt((handleX - x) ** 2 + (handleY - y) ** 2) <= self.handleRadius:
            return True
        return False

    def round(self, value):
        return self.step * round(value / self.step)

    def getValue(self):
        return self.value

    def setValue(self, value):
        self.value = value

class Start:
    def __init__(self):
        self.run = True
        self.but1 = Button(screen, 450, 400, 100, 40, text ='play', hoverColour=(150, 0, 0), pressedColour=(0, 200, 20), onClick = lambda: main())
        self.but2 = Button(screen, 450, 450, 100, 40, text = 'settings', onClick = lambda: settings())
    def start_screen(self):
        intro_text = ["MYNEKRUFT"]
        fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (width, height))
        screen.blit(fon, (0, 0))
        font = pygame.font.Font("mine.ttf", 50)
        text_coord = 30
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('gray'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 330
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        #play = Button('play')
        #settings = Button('settings')
        while self.run:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            pygame_widgets.update(events)
            pygame.display.flip()
            clock.tick(fps)

def settings():
    a.but1.hide()
    a.but2.hide()
    a.run = False
    set()

def fscreen():
    global res
    res[2] = 'True' if res[2] == 'False' else 'False'

def save(arg):
    global res
    with open('sttngs.py', 'wt') as f:
        f.write('\n'.join([arg[i] + ' = ' + res[i] for i in range(len(arg))]))
    for i in but:
        i.hide()
    a.but1.show()
    a.but2.show()  
    a.run = True
    a.start_screen()

def main_menu():
    global but
    for i in but:
        i.hide()
    a.but1.show()
    a.but2.show()  
    a.run = True
    a.start_screen()

def set():
    global res, but
    with open('sttngs.py') as f:
        g = f.read().split('\n')
        arg = [i.split(' = ')[0] for i in g]
        res = [i.split(' = ')[1] for i in g]
        base = res.copy()
        print(arg)
        print(res)
    size = width, height = 1000, 500
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    fps = 62
    if not but:
        but.append(Button(screen, 200, 300, 100, 50, text = arg[2] + ' ' + res[2], onClick = lambda: fscreen()))
        but.append(Slider(screen, 150, 200, 200, 25, initial = int(int(res[4])-90)))
        but.append(Button(screen, 200, 175, 100, 25, text = 'FOV: ' + res[4]))
        but.append(Button(screen, 450, 400, 100, 40, text = 'apply', onClick = lambda: save(arg)))
        but.append(Button(screen, 450, 450, 100, 40, text = 'back', onClick = lambda: main_menu()))
    else:
        for i in but:
            i.show()
        res = base.copy()
        but[1].setValue(int(int(res[4])-90))
    #but3 = Button(screen, 450, 400, 100, 40, text = 'back', onClick = lambda: main_menu())
    while not a.run:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        res[4] = str(but[1].getValue() + 90)
        but[2].set('text', 'FOV: ' + res[4])
        but[0].set('text', arg[2] + ' ' + res[2])
        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(fps)

if __name__ == '__main__':
    res = []
    but = []
    fps = 62
    pygame.init()
    size = width, height = 1000, 500
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    a = Start()
    a.start_screen()