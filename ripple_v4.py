import math
import pygame
import pygame.surfarray as surfarray
import threading
import time
import sys

# settings
mode = int(sys.argv[1])
maxX = 300
maxY = 300
FRAME_SIZE = (maxX, maxY)
BACKGROUND_COLOR = (127, 127, 127)


# Boiler plate initialization
# Also returns an array of the pixes (Note): this is not stored in the conventional RGB or grayscale values
def startUp():
    pygame.init()
    pygame.display.set_caption("Ripple")
    display = pygame.display.set_mode(FRAME_SIZE)
    pixels = pygame.PixelArray(display)
    pixels[:, :] = BACKGROUND_COLOR
    pygame.display.flip()
    return pixels.surface, surfarray.array2d(pixels.surface)


# draws a circle
# currently in prototype phase
def circle(centerX, centerY, radius, colorShift, array):
    # adjust colorshift into pygame format it essentially acts as a base 255 number system from the RGB
    colorShift = colorShift[0] * 256 ** 2 + colorShift[1] * 256 + colorShift[2]
    center = (centerX, centerY)
    x = 0
    y = radius
    h = 1 - radius

    if radius == 0:  # for radius 0
        array[center[0], center[1]] += colorShift

    while x <= y:
        # need to check for out of bounds
        if 0 <= x + center[0] < maxX and 0 < y + center[1] < maxY:
            array[x + center[0], y + center[1]] += colorShift

        if 0 <= -x + center[0] < maxX and 0 <= y + center[
            1] < maxY and x != 0:  # and not x = 0 to avoid doubling cardinal directions
            array[-x + center[0], y + center[1]] += colorShift

        if 0 <= x + center[0] < maxX and 0 <= -y + center[1] < maxY:
            array[x + center[0], -y + center[1]] += colorShift

        if 0 <= -x + center[0] < maxX and 0 <= -y + center[
            1] < maxY and x != 0:  # and not x = 0 to avoid doubling cardinal directions
            array[-x + center[0], -y + center[1]] += colorShift

        # reverse x and y
        if 0 <= y + center[0] < maxX and 0 <= x + center[1] < maxY and x != y:
            array[y + center[0], x + center[1]] += colorShift

        if 0 <= -y + center[0] < maxX and 0 <= x + center[1] < maxY and x != y:
            array[-y + center[0], x + center[1]] += colorShift

        if 0 <= y + center[0] < maxX and 0 <= -x + center[
            1] < maxY and x != 0 and x != y:  # and not x = 0 to avoid doubling cardinal directions
            array[y + center[0], -x + center[1]] += colorShift

        if 0 <= -y + center[0] < maxX and 0 <= -x + center[
            1] < maxY and x != 0 and x != y:  # and not x = 0 to avoid doubling cardinal directions
            array[-y + center[0], -x + center[1]] += colorShift

        x += 1
        if h < 0:
            h += 2 * x + 3
        else:
            h += 2 * (x - y) + 5
            y -= 1


def ripple(mouse_pos, sur, array):
    WAVE_ELEMENTS = 21  # number of wave heights
    SPACING = 2  # space between wave elements
    WAVE_MAX = 10  # constant for wave height
    r = 0
    max_radius = max(math.sqrt(mouse_pos[0] ** 2 + mouse_pos[1] ** 2),
                     math.sqrt((maxX - mouse_pos[0]) ** 2 + mouse_pos[1] ** 2),
                     math.sqrt(mouse_pos[0] ** 2 + (maxY - mouse_pos[1]) ** 2),
                     math.sqrt((maxX - mouse_pos[0]) ** 2 + (maxY - mouse_pos[1]) ** 2)
                     )

    t = time.time()
    while r < max_radius + SPACING * WAVE_ELEMENTS:
        for i in range(WAVE_ELEMENTS):
            wave_r = r - SPACING * i
            if wave_r >= 0:
                wave_height = math.sin(3 * math.pi * (i / WAVE_ELEMENTS))
                adjust = int(WAVE_MAX * wave_height)

                if i >= WAVE_ELEMENTS * 1 / 3 and i < WAVE_ELEMENTS * 2 / 3:
                    adjust *= 2

                circle(mouse_pos[0], mouse_pos[1], wave_r, (adjust, adjust, adjust), array)
        r += 1
        surfarray.blit_array(sur, array)
        pygame.display.flip()
    print(time.time() - t)


def main():
    pixels, array = startUp()

    running = True
    while running:
        for event in pygame.event.get():
            # check for app exit
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()

            # create ripple
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if mode == 1:
                    x = threading.Thread(target=ripple, args=(mouse_pos, pixels, array), daemon=True)
                    x.start()
                else:
                    ripple(mouse_pos, pixels, array)


if __name__ == "__main__":
    main()
