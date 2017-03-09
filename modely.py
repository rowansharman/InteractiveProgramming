import pygame, random, unicodeGen, math

allUnicodeChoices = unicodeGen.get_all_unicode()  # Run this once to generate the list

white = 255, 255, 255
green = 0, 255, 0

class Model:
    '''Model keeps track of the game state, including running time and
    score-related info'''

    def __init__(self, runTime=60, hits=0, misses=0, wrongKey=0, gameOver=False):
        '''keeps track of hits misses and game state and initializes the class.
        When undefined, hits and misses equal zero and gameover is false.
        '''
        self.hits = hits
        self.misses = misses
        self.wrongKey = wrongKey
        self.gameover = gameOver
        self.runTime = runTime

    def score(self):
        '''Keeps track of score'''
        total = self.hits + self.misses + self.wrongKey
        if(total == 0):
            return 0
        return (self.hits / total) * 100

    def updateScore(self, event, timeRunning):
        '''Updates score statistics by modifying values in the class model'''
        if event == 'h':
            self.hits += 1
        elif event == 'm':
            self.misses += 1
        else:
            self.wrongKey += 1
        if timeRunning/1000 >= self.runTime:  # Game over after runTime seconds
            self.gameover = True


class Letter:
    '''Letter objects include the letter to be typed, its location on the
    screen, size, and related information, and the random unicode string that
    follows it'''

    def __init__(self,
                 font='ARIALUNI.TTF', value=None, x=None, y=None, surf=None):
        # arguments not passed in are randomly generated
        self.font = font
        self.textFont = pygame.font.Font(self.font, 40)
        self.tailFont = pygame.font.Font(self.font, 40)

        charWidth = 40
        # by experimentation, the widest characters appear to be about 40
        # pixels in this font and size
        charHeight = self.textFont.size('X')[1]
        # all characters should be the same height

        if(value == None):
            self.value = random.randint(97, 122)
            # this is the range a-z in ascii
        else:
            self.value = value

        self.tail = []  # tail is the random unicode string
        # Add a random number of random characters to the tail:
        self.tailLength = random.randint(3, 12)
        for i in range(self.tailLength):
            self.tail.append(random.choice(allUnicodeChoices))

        self.surf = pygame.Surface((charWidth, charHeight*(self.tailLength+1)))
        # Create a new object for the character and tail to be on
        targetChar = self.textFont.render(chr(self.value), 1, white)
        # This is the character at the bottom that you're supposed to type
        self.surf.blit(targetChar, (0, (self.tailLength)*charHeight))
        for i in range(len(self.tail)):
            uni = self.tailFont.render(self.tail[i], 1, green)
            self.surf.blit(uni, (0, ((i)*charHeight)))

        self.height = self.surf.get_height()

        if y == None:
            self.y = 0 - (random.randint(0, 600) + self.height)
            # Place the surface off the screen
        else:
            self.y = y
        if(x == None):
            self.x = random.randint(0, 19)
        else:
            self.x = x

    def getEnd(self):
        # return the coordinates of the bottom end of the surface
        return self.y + self.height
