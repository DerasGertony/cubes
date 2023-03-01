from typing import Callable
import pygame

from pygame_widgets.widget import WidgetBase
from generation import generation


class ProgressBar(WidgetBase):
    def draw(win, x, y, width, height, progress):
        """ Display to surface """
        percent = min(max(progress, 0), 1)
        pygame.draw.rect(win, (100, 100, 100),
                             (x, y, int(width * percent), height))
        pygame.draw.rect(win, (10, 10, 10),
                             (x, y, int(width * percent), height), 1)
        pygame.draw.rect(win, (50, 50, 50),
                             (x + int(width * percent), y,
                              int(width * (1 - percent)), height))
