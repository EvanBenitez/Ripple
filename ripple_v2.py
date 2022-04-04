import math

import pygame
import numpy as np
import time

from threading import Thread, Event
from typing import Tuple

MAX_VALUE = 128

event_var = Event()


def scale_up(im):
    # Use this instead of np.kron(). This method is about 2.5x faster to scale up the array
    return im.repeat(3, axis=0).repeat(3, axis=1)


# Converts numpy array to a grayscale value
def gray(im):
    im = 255 * (im / MAX_VALUE)
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 2] = ret[:, :, 1] = ret[:, :, 0] = im
    return scale_up(ret)


class Circle:
    def __init__(self, center: Tuple[int, int]):
        self.center = (math.floor(center[0]/3), math.floor(center[1]/3))
        self.radius = 0
        self.active = True


circles: [Circle] = []


def calculate():
    while not event_var.is_set():
        for circle in circles:
            center = circle.center
            array[center[0]][center[1]] = 100


def startup():
    pygame.init()
    display = pygame.display.set_mode((900, 900))
    array = np.zeros((300, 300), dtype=np.int8)
    return display, array


display, array = startup()
calculator_thread = Thread(target=calculate)
calculator_thread.start()
surface = pygame.surfarray.make_surface(gray(array))
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            event_var.set()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            circles.append(Circle((mouse_pos[0], mouse_pos[1])))
    display.blit(surface, (0, 0))
    surface = pygame.surfarray.make_surface(gray(array))
    pygame.display.update()
pygame.quit()
