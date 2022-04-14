import math

import pygame
import numpy as np
import time

from threading import Thread, Event
from typing import Tuple

MAX_VALUE = 128
HIGHEST_INCREASE = 32
RADIUS_FACTOR = 2

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
        self.center = (math.floor(center[0] / 3), math.floor(center[1] / 3))
        self.center_x = math.floor(center[1] / 3)
        self.center_y = math.floor(center[0] / 3)
        self.current_radius = 1
        self.active = True

        self.max_radius = max(math.sqrt(self.center[0] ** 2 + self.center[1] ** 2),
                              math.sqrt((300 - self.center[0]) ** 2 + self.center[1] ** 2),
                              math.sqrt(self.center[0] ** 2 + (300 - self.center[1]) ** 2),
                              math.sqrt((300 - self.center[0]) ** 2 + (300 - self.center[1]) ** 2)
                              )/RADIUS_FACTOR

    def __repr__(self):
        return f'Center: {self.center}. Radius: {self.current_radius}. Active: {self.active}'


circles: [Circle] = []
x = np.arange(0, 300)
y = np.arange(0, 300)


def draw_circle(circle: Circle, internal_array):
    for i in range(8):
        radius = circle.current_radius - i
        if radius <= 0:
            break
        mask = np.power((x[np.newaxis, :] - circle.center_x), 2) + np.power((
                    y[:, np.newaxis] - circle.center_y), 2) < np.power((radius * RADIUS_FACTOR), 2)
        internal_array[mask] += (HIGHEST_INCREASE - (4 * i))
    circle.current_radius += 1


def calculate():
    previous_circle_string = str(circles)
    while not event_var.is_set():
        # If the circles array has not changed since previous iteration, wait and continue
        if str(circles) == previous_circle_string:
            time.sleep(0.5)
            continue

        previous_circle_string = str(circles)
        print(previous_circle_string)
        internal_array = np.zeros((300, 300), dtype=np.int8)
        for circle in circles:
            # If a circle has completed its animation, get rid of it
            if circle.current_radius >= circle.max_radius:
                circles.remove(circle)
                continue

            draw_circle(circle, internal_array)

        # Update Display
        surface = pygame.surfarray.make_surface(gray(internal_array))
        display.blit(surface, (0, 0))
        pygame.display.update()


def startup():
    pygame.init()
    display = pygame.display.set_mode((900, 900))
    array = np.zeros((300, 300), dtype=np.int8)
    return display, array


display, array = startup()
running = True
is_updating = False
calculator_thread = Thread(target=calculate)
calculator_thread.start()
surface = pygame.surfarray.make_surface(gray(array))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            event_var.set()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            circles.append(Circle((mouse_pos[0], mouse_pos[1])))
pygame.quit()
