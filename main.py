# import the pygame module, so you can use it
import pygame
import sys
import utils
import objects
import random

# global variables
block_size = 35
grid = [[0 for x in range(10)] for y in range(20)]
screen = pygame.display.set_mode((block_size * len(grid[0]),
                                  block_size * len(grid)))
pieces = []
# define a main function

def main():
    # initialize the pygame module
    pygame.init()
    # load and set the logo
    pygame.display.set_caption("PYGAME TEMPLATE")
    utils.fill_grid(grid)
    # create clock
    clock = pygame.time.Clock()
    # define a variable to control the main loop
    running = True
    # initialize stuff
    background = pygame.Surface(screen.get_size())  # Create empty pygame surface
    background.fill((255,255,255))     # Fill the background white color (red,green,blue)
    background = background.convert()  # Convert Surface to make blitting faster
    timer = 0
    previous = random.randrange(0,7)
    pieces.append(objects.Piece(previous))
    speeding = False
    dup_count = 0
    ran = 0
    num_filled = 0
    score = 0
    # main loop
    while running:
        milliseconds = clock.tick(15) # controls FPS
        timer += milliseconds / 1000.0
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            if (event.type == pygame.KEYDOWN and (event.key == pygame.K_s
                    or event.key == pygame.K_DOWN)):
                speeding = True
            if (event.type == pygame.KEYUP and (event.key == pygame.K_s
                    or event.key == pygame.K_DOWN)):
                speeding = False
            utils.input(event, pieces[-1], pieces)
        # draw stuff here
        speed = 0.75 if not speeding else 0.1
        if (speed - timer <= 0):
            pieces[-1].fall(pieces);
            if pieces[-1].has_settled:
                if utils.check_lost(grid, pieces):
                    score = 0
                num_filled = utils.update_grid(grid, pieces)
                score += num_filled * 50 if num_filled < 4 else num_filled * 100
                previous = ran
                ran = random.randrange(0, 7)
                if ran == previous:
                    dup_count += 1
                if dup_count == 2:
                    dup_count = 0
                    while ran == previous:
                        ran = random.randrange(0, 7)
                pieces.append(objects.Piece(ran))
            timer = 0
        screen.blit(background, (0, 0))
        utils.draw_grid(screen, grid)
        for piece in pieces:
            piece.draw(screen)
        pygame.display.flip()
        pygame.display.set_caption("FPS: {0:.2f} | SCORE: {1}".format(clock.get_fps(), score))
    pygame.quit()
    sys.exit()


# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
