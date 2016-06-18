# Elementary cellular automaton
# [add description here]

#from aut.binary.binaryAut import BAut
from aut.baseAut import BaseAut
import random

class ECAut(BaseAut):
    def __init__(self, rule, width, height, seed=-1):
        super().__init__(width, height)
        self.rule = rule
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d = ECAut.ruleDict(rule, 2)
        
        if seed != -1:
            random.seed(seed)
        num = random.randint(0, 2**width-1)
##        binStr = bin(num)[2:]
##        
##        # Add leading zeroes if necessary
##        binStr = '0' * (width - len(binStr)) + binStr
##        row = ECAut.binStrToList(binStr)
##        self.aut.append(row)

        row = ECAut.decToBaseNList(num, 2)
        ECAut.padList(row, width)        
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
            'Type: elementary cellular automaton',
            'Rule: {}'.format(self.rule),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])

##    def description(self):
##        '''rule, width, height, seed'''
##        return 'ECAut_{}_{}_{}_{}'.format(
##            self.rule, self.width, self.height, self.seed )

