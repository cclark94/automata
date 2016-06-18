#from aut.ternary.ternaryAut import TAut
from aut.baseAut import BaseAut
import random

class ETAut(BaseAut):
    def __init__(self, rule, width, height, seed=-1):
        super().__init__(width, height)
        self.rule = rule
        self.seed = seed
        self.stateCount = 3
        self.aut = list()

        d = ETAut.ruleDict(rule, 3)
        if seed != -1:
            random.seed(seed)
        num = random.randint(0, 3**width-1)
##        ternStr = ETAut.decToTernStr(num)
##        # Add leading zeroes if necessary
##        ternStr = '0' * (width - len(ternStr)) + ternStr
##        row = ETAut.ternStrToList(ternStr)

        row = ETAut.decToBaseNList(num, 3)
        ETAut.padList(row, width)
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                temp.append(d[config])
            row = temp
            self.aut.append(row)

    def infoStr(self):
        return '\n'.join([
            'Type: elementary ternary automaton',
            'Rule: {}'.format(self.rule),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])

##    def description(self):
##        '''rule, width, height, seed'''
##        return 'ETAut_{}_{}_{}_{}'.format(
##            self.rule, self.width, self.height, self.seed )
            
    
