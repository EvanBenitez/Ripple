import pygame

# settings
FRAME_SIZE = (500, 500)
BACKGROUND_COLOR = (127, 127, 127)

# Boiler plate initilizaton
# Also returns an array of the pixes (Note): this is not stored in the conventional RGB or grayscale values
def startUp():
    pygame.init()
    pygame.display.set_caption("Ripple")
    display = pygame.display.set_mode(FRAME_SIZE)
    pixels = pygame.PixelArray(display)
    pixels[:,:] = (BACKGROUND_COLOR)
    pygame.display.flip()
    return pixels


def main():
    startUp()

    running = True
    while running:
        for event in pygame.event.get():
            # check for app exit
            if event.type == pygame.QUIT:
                running = False
                pygame.display.quit()
                pygame.quit()

if __name__ == "__main__":
    main()