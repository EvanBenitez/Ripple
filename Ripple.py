import pygame

# settings
maxX = 500
maxY = 500
FRAME_SIZE = (maxX, maxY)
BACKGROUND_COLOR = (0, 0, 0)

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
    while x < y:
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
        if 0 <= y + center[0] < maxX and 0 <= x+ center[1] < maxY:
            array[y + center[0], x + center[1]] += colorShift
        
        if 0 <= -y + center[0] < maxX and 0 <= x+ center[1] < maxY:
            array[-y + center[0], x + center[1]] += colorShift

        if 0 <= y + center[0] < maxX and 0 <= -x+ center[1] < maxY and x != 0: # and not x = 0 to avoid doubling cardnal directions
            array[y + center[0], -x + center[1]] += colorShift

        if 0 <= -y + center[0] < maxX and 0 <= -x+ center[1] < maxY and x != 0: # and not x = 0 to avoid doubling cardnal directions
            array[-y + center[0], -x + center[1]] += colorShift

        x += 1
        if h < 0:
            h += 2 * x + 3
        else:
            h += 2 * (x - y) + 5
            y -= 1
    pygame.display.flip()



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

            # create ripple... eventually
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                circle(mouse_pos[0], mouse_pos[1], 30, (100,100,100), pixels)

if __name__ == "__main__":
    main()