import sys, pygame, time, random, unicodeGen
from modely import Model, Letter

speed = 3
runTime = 60  # seconds

pygame.init()

size = width, height = 1200, 600  # window size
black = 0, 0, 0
white = 255, 255, 255
grey = 50, 50, 50
red = 255, 0, 0

font = 'ARIALUNI.TTF'
textFont = pygame.font.Font(font, 40)
scoreFont = pygame.font.Font(font, 20)

screen = pygame.display.set_mode(size)  # make the window

mod = Model(runTime)  # make a game that will run for runTime seconds

letters = []
for i in range(10):  # Generate our random list of Letters
    letters.append(Letter())


def randExclude(exclude, start, stop):
    '''returns a random column in range of x-values excluding the values given
    to exclude. This prevents letters dropping into the same column and
    covering each other.
    '''
    r = None
    while r in exclude or r is None:
        r = random.randrange(start, stop)
    return r


def replaceLet(let, start, stop):
    '''Ensures that there are no letters in the same column. If there are,
    replace them.
    '''
    xVals = []
    for i in range(len(let)):
        if let[i].x in xVals:
            a = randExclude(xVals, start, stop)
            let[i].x = a
            xVals.append(a)
        else:
            xVals.append(let[i].x)
    return(let)


letters = replaceLet(letters, 0, 19)
# make sure that there are no overlapping letters in the original list


def xInLetters(l):
    '''returns a list of all the occupied columns'''
    xV = []
    for i in range(len(l)):
        xV.append(l[i].x)
    return xV


letterSize = textFont.size('X')
targetStart = 100
# Distance from the bottom of the screen to the top of the target

target = pygame.Surface((width, 70))

# curTime = time.clock() - startTime
clock = pygame.time.Clock()
startTime = pygame.time.get_ticks()
fps = 30

while not mod.gameover:  # This is the main loop
    clock.tick(fps)  # This determines how often the loop runs
    screen.fill(black)
    target.fill(grey)
    screen.blit(target, (0, height - targetStart))
    potentials = []

    for i in range(len(letters)):
        # Go through all the letters to update their positions and
        # determine whether they are on the screen and whether they are in the
        # target zone.
        thisLetter = letters[i]
        letters[i].y += speed
        screen.blit(thisLetter.surf, ((width/20)*thisLetter.x, thisLetter.y))

        if thisLetter.getEnd() >= 600:  # If letter off the screen, replace it
            xs = xInLetters(letters)
            letters[i] = Letter()
            letters[i].x = randExclude(xs, 0, 19)
            print('   X')
            timeRunning = pygame.time.get_ticks() - startTime
            mod.updateScore('m', timeRunning)

        if thisLetter.getEnd() > height - targetStart:
            # If bottom of letter has reached top of target box, add it to the
            # list of correct letters
            potentials.append(thisLetter.value)

    for event in pygame.event.get():  # When something happens
        if event.type == pygame.QUIT:  # Terminate the program if window closed
            sys.exit()
        if event.type == pygame.KEYDOWN:
            keyPressed = event.key
            if keyPressed in potentials:  # Hit!
                for i in range(len(letters)):
                    # scan through to find letter(s) that was pressed and is in
                    # target box, replace it, and update score
                    if (keyPressed == letters[i].value
                       and letters[i].getEnd() >= height - targetStart):
                        print('X')
                        timeRunning = pygame.time.get_ticks() - startTime
                        mod.updateScore('h', timeRunning)
                        xs = xInLetters(letters)
                        letters[i] = Letter()
                        letters[i].x = randExclude(xs, 0, 19)
            else:  # Pressed wrong key
                print('      X')
                timeRunning = pygame.time.get_ticks() - startTime
                mod.updateScore('w', timeRunning)

    # Add the scoreboard and update the dispay:
    scoreboard = scoreFont.render(
        ('Score: ' + str(round(mod.score(), 1))), 1, red)
    screen.blit(scoreboard, (width - 100, 10))
    pygame.display.flip()

while mod.gameover:
    clock.tick(fps)
    screen.fill(black)
    endFont = pygame.font.Font(font, 100)
    endText = endFont.render(('Score: ' + str(round(mod.score(), 1))), 1, red)
    endTextSize = endText.get_size()
    screen.blit(endText, (width/2 - endTextSize[0]/2,
                          height/2 - endTextSize[1]/2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
