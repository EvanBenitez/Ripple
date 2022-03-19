import math
import pygame
import time

# settings
maxX = 500
maxY = 500
FRAME_SIZE = (maxX, maxY)
BACKGROUND_COLOR = (127, 127, 127)

# Boiler plate initilizaton
# Also returns an array of the pixes (Note): this is not stored in the conventional RGB or grayscale values
def startUp():
    pygame.init()
    pygame.display.set_caption("Ripple")
    display = pygame.display.set_mode(FRAME_SIZE)
    pixels = pygame.PixelArray(display)
    pixels[:,:] = BACKGROUND_COLOR
    pygame.display.flip()
    return pixels

# draws a circle
# currently in prototype phase
def circle(centerX, centerY, radius, colorShift, array):

    # adjust colorshift into pygame format it esesentually acts as a base 255 number system from the RGB
    colorShift = colorShift[0] * 256**2 + colorShift[1] * 256 + colorShift[2]
    center = (centerX, centerY)
    x = 0
    y = radius
    h = 1 - radius

    if radius == 0: # for radius 0
        array[center[0], center[1]] += colorShift

    while x <= y:
        # need to check for out of bounds
        if 0 <= x + center[0] < maxX and 0 < y + center[1] < maxY:
            array[x + center[0], y + center[1]] += colorShift

        if 0 <= -x + center[0] < maxX and 0 <= y + center[1] < maxY and x != 0: # and not x = 0 to avoid doubling cardnal directions
            array[-x + center[0], y + center[1]] += colorShift

        if 0 <= x + center[0] < maxX and 0 <= -y + center[1] < maxY:
            array[x + center[0], -y + center[1]] += colorShift

        if 0 <= -x + center[0] < maxX and 0 <= -y + center[1] < maxY and x != 0: # and not x = 0 to avoid doubling cardnal directions
            array[-x + center[0], -y + center[1]] += colorShift

        # reverse x and y
        if 0 <= y + center[0] < maxX and 0 <= x + center[1] < maxY and x != y:
            array[y + center[0], x + center[1]] += colorShift
        
        if 0 <= -y + center[0] < maxX and 0 <= x + center[1] < maxY and x != y:
            array[-y + center[0], x + center[1]] += colorShift

        if 0 <= y + center[0] < maxX and 0 <= -x + center[1] < maxY and x != 0 and x != y: # and not x = 0 to avoid doubling cardnal directions
            array[y + center[0], -x + center[1]] += colorShift

        if 0 <= -y + center[0] < maxX and 0 <= -x + center[1] < maxY and x != 0 and x != y: # and not x = 0 to avoid doubling cardnal directions
            array[-y + center[0], -x + center[1]] += colorShift

        x += 1
        if h < 0:
            h += 2 * x + 3
        else:
            h += 2 * (x - y) + 5
            y -= 1
    pygame.display.flip()

def ripple(mouse_pos, pixels):
    WAVE_ELEMENTS = 21 # number of wave heights
    SPACING = 2 # space between wave elements
    WAVE_MAX = 10 # constant for wave height
    r = 0
    max_radius = max(math.sqrt(mouse_pos[0]**2 + mouse_pos[1]**2), 
                        math.sqrt((maxX - mouse_pos[0])**2 + mouse_pos[1]**2), 
                        math.sqrt(mouse_pos[0]**2 + (maxY - mouse_pos[1])**2), 
                        math.sqrt( (maxX - mouse_pos[0])**2 + (maxY - mouse_pos[1])**2) 
                    )
    
    # while r < max_radius + SPACING * WAVE_ELEMENTS:
    #     for i in range(WAVE_ELEMENTS):
    #         wave_r = r - SPACING * i
    #         if wave_r >= 0:
    #             wave_height = math.cos(2 * math.pi * (i / WAVE_ELEMENTS))
                
    #             adjust = int(WAVE_MAX * wave_height)
    #             circle(mouse_pos[0], mouse_pos[1], wave_r, (adjust,adjust,adjust), pixels)
    #     r += 1
    #     time.sleep(0.01)

    # more accurate wave, however introduces very slight color distortions
    while r < max_radius + SPACING * WAVE_ELEMENTS:
        for i in range(WAVE_ELEMENTS):
            wave_r = r - SPACING * i
            if wave_r >= 0:
                wave_height = math.sin(3 * math.pi * (i / WAVE_ELEMENTS))
                if i >= WAVE_ELEMENTS * 1 / 3 and i < WAVE_ELEMENTS * 2 / 3:
                    wave_height *= 2

                adjust = int(WAVE_MAX * wave_height)
                circle(mouse_pos[0], mouse_pos[1], wave_r, (adjust,adjust,adjust), pixels)
        r += 1
        # time.sleep(0.01)


def main():
    pixels = startUp()

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
                # circle(mouse_pos[0], mouse_pos[1], 30, (100,100,100), pixels)
                ripple(mouse_pos, pixels)
                # x = threading.Thread(target=ripple, args=(mouse_pos, pixels,), daemon=True)
                # x.start()

if __name__ == "__main__":
    main()