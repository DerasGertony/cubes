import pygame

import math

import pygame_widgets
from pygame_widgets.widget import WidgetBase
from pygame_widgets.mouse import Mouse, MouseState
from pygame_widgets.button import Button
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
def fscreen():
    global res
    res[3] = 'True' if res[3] == 'False' else 'False'
def save():
    pass
def main_menu():
    global but
    for i in but:
        i.hide()
    return 'bruh'

def set():
    global res, but
    with open('sttngs.py') as f:
        g = f.read().split('\n')[:-1]
        arg = [i.split(' = ')[0] for i in g]
        res = [i.split(' = ')[1] for i in g]
        print(arg)
        print(res)
    
    pygame.init()
    size = width, height = 1000, 500
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(pygame.image.load('fon.jpg'), (width, height))
    fps = 60
    but.append(Button(screen, 200, 300, 100, 50, text = arg[3] + ' ' + res[3], onClick = lambda: fscreen()))
    but.append(Slider(screen, 150, 200, 200, 25, initial = int(int(res[5])-90)))
    but.append(Button(screen, 200, 175, 100, 25, text = 'FOV: ' + res[5]))
    but.append(Button(screen, 450, 400, 100, 40, text = 'apply', onClick = lambda: save()))
    but.append(Button(screen, 450, 450, 100, 40, text = 'back', onClick = lambda: main_menu()))
    but[0].set('text', 'bruh')
    #but3 = Button(screen, 450, 400, 100, 40, text = 'back', onClick = lambda: main_menu())
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        screen.blit(fon, (0,0))
        res[5] = str(but[1].getValue() + 90)
        print(arg[3] + ' ' + res[3], res[5])
        pygame_widgets.update(events)
        pygame.display.flip()
        clock.tick(fps)
res = []
but = []