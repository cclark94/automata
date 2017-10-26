from aut.baseAut import BaseAut
from PIL import Image
import random

# should put this somewhere more sensible
def getPixelGrid(image):
    '''Given a PIL Image, returns a list of lists, where each inner
    list is one row of the image'''
    w = image.width
    h = image.height
    d = list(image.getdata())
    return [d[w*i : w*(i+1)] for i in range(h)]


class BaAut(BaseAut):
    '''Background automaton'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1

    # width and height are taken from background image
    def __init__(self, rule, image, seed=None):
        if rule < BaAut.RULE_MIN or rule > BaAut.RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        # convert() changes pixels to 1-bit (black or white)
        im = Image.open(image).convert(mode='1')
        width = im.width
        height = im.height
        super().__init__(width, height)
        self.rule = rule
        self.image = image
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d = BaAut.ruleDict(rule, 2)
        self.prepareRandomSeed(seed)
        num = random.randint(0, 2**width-1)

        imgrid = getPixelGrid(im)

        row = BaAut.decToBaseNList(num, 2)
        BaAut.padList(row, width)
        # Pixel flipping on first row is not done; since pixels
        # randomly generated the result would not look different
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                result = d[config]
                # Flip result if corresponding pixel in image is black
                # i+1 because we skip the first row of the image
                if imgrid[i+1][j] == 0:
                    result = 1 - result
                temp.append(result)
            row = temp
            self.aut.append(row)



    def infoStr(self):
        return '\n'.join([
            'Type: background automaton',
            'Rule: {}'.format(self.rule),
            'Image: {}'.format(self.image),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])
