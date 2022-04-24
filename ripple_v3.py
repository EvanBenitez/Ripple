import math

import pygame
import numpy as np
import time

from threading import Thread, Event
from typing import Tuple

MAX_VALUE = 128
HIGHEST_INCREASE = 32
RADIUS_FACTOR = 3
MAX_CALC_SIZE = 300
MAX_DISPLAY_SIZE = 900
WAVE_ELEMENTS = 20
WAVE_MAX = 10

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
    ret = 255 - ret
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
                              )

    def __repr__(self):
        return f'Center: {self.center}. Radius: {self.current_radius}. Active: {self.active}'


circles: [Circle] = []
x = np.arange(0, MAX_CALC_SIZE)
y = np.arange(0, MAX_CALC_SIZE)


def circle(centerX, centerY, radius, color_shift, array):

    center = (centerX, centerY)
    x = 0
    y = radius
    h = 1 - radius

    if radius == 0: # If the circle has just been formed
        array[center[0], center[1]] += color_shift

    while x <= y:
        # Need to check for out of bounds
        if 0 <= x + center[0] < MAX_CALC_SIZE and 0 < y + center[1] < MAX_CALC_SIZE:
            array[x + center[0], y + center[1]] += color_shift

        # And not x = 0 to avoid doubling cardinal directions
        if 0 <= -x + center[0] < MAX_CALC_SIZE and 0 <= y + center[1] < MAX_CALC_SIZE and x != 0:
            array[-x + center[0], y + center[1]] += color_shift

        if 0 <= x + center[0] < MAX_CALC_SIZE and 0 <= -y + center[1] < MAX_CALC_SIZE:
            array[x + center[0], -y + center[1]] += color_shift

        # And not x = 0 to avoid doubling cardinal directions
        if 0 <= -x + center[0] < MAX_CALC_SIZE and 0 <= -y + center[1] < MAX_CALC_SIZE and x != 0:
            array[-x + center[0], -y + center[1]] += color_shift

        # reverse x and y
        if 0 <= y + center[0] < MAX_CALC_SIZE and 0 <= x + center[1] < MAX_CALC_SIZE and x != y:
            array[y + center[0], x + center[1]] += color_shift

        if 0 <= -y + center[0] < MAX_CALC_SIZE and 0 <= x + center[1] < MAX_CALC_SIZE and x != y:
            array[-y + center[0], x + center[1]] += color_shift

        # And not x = 0 to avoid doubling cardinal directions
        if 0 <= y + center[0] < MAX_CALC_SIZE and 0 <= -x + center[1] < MAX_CALC_SIZE and x != 0 and x != y:
            array[y + center[0], -x + center[1]] += color_shift

        # And not x = 0 to avoid doubling cardinal directions
        if 0 <= -y + center[0] < MAX_CALC_SIZE and 0 <= -x + center[1] < MAX_CALC_SIZE and x != 0 and x != y:
            array[-y + center[0], -x + center[1]] += color_shift

        x += 1
        if h < 0:
            h += 2 * x + 3
        else:
            h += 2 * (x - y) + 5
            y -= 1


def draw_circle(circle_object: Circle, internal_array):
    for i in range(WAVE_ELEMENTS):
        wave_r = circle_object.current_radius - i # Wave spacing is 1 here, always
        if wave_r >= 0:
            wave_height = math.sin(3 * math.pi * (i/WAVE_ELEMENTS))
            adjust = int(WAVE_MAX + 3*i)

            # if i >= WAVE_ELEMENTS * i/3 and i < WAVE_ELEMENTS * 2/3:
            #     adjust *= 2

            circle(circle_object.center_y, circle_object.center_x, wave_r, adjust, internal_array)
    circle_object.current_radius += 1


def calculate():
    previous_circle_string = str(circles)
    while not event_var.is_set():
        # If the circles array has not changed since previous iteration, wait and continue
        if str(circles) == previous_circle_string:
            time.sleep(0.5)
            continue

        previous_circle_string = str(circles)
        print(previous_circle_string)
        internal_array = np.zeros((MAX_CALC_SIZE, MAX_CALC_SIZE), dtype=np.int8)
        for circle in circles:
            # If a circle has completed its animation, get rid of it
            if circle.current_radius + WAVE_ELEMENTS >= circle.max_radius:
                circles.remove(circle)
                continue

            draw_circle(circle, internal_array)

        # Update Display
        surface = pygame.surfarray.make_surface(gray(internal_array))
        display.blit(surface, (0, 0))
        pygame.display.update()


def startup():
    pygame.init()
    display = pygame.display.set_mode((MAX_DISPLAY_SIZE, MAX_DISPLAY_SIZE))
    array = np.zeros((MAX_CALC_SIZE, MAX_CALC_SIZE), dtype=np.int8)
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
