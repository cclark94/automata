# Split automaton
# [add description here. note: like mixed automaton]

#from aut.binary.binaryAut import BAut
from aut.baseAut import BaseAut
import random

class SAut(BaseAut):
    def __init__(self, rule1, rule2, width, width1, height, seed=-1):
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.width1 = width1
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        
        d1 = SAut.ruleDict(rule1, 2)
        d2 = SAut.ruleDict(rule2, 2)
        width2 = width - width1
        if not seed == -1:
            random.seed(seed)
        num = random.randint(0, 2**width-1)
        binStr = bin(num)[2:]
        
##        # Add leading zeroes if necessary
##        binStr = '0' * (width - len(binStr)) + binStr
##        row = SAut.binStrToList(binStr)  
##        self.aut.append(row)

        row = SAut.decToBaseNList(num, 2)
        SAut.padList(row, width)        
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width1):
                prev = row[(j-1)%width]
                curr = row[j]
                nxt = row[(j+1)%width]
                config = (prev, curr, nxt)
                temp.append(d1[config])
                
            for k in range(width1, width):
                prev = row[(k-1)%width]
                curr = row[k]
                nxt = row[(k+1)%width]
                config = (prev, curr, nxt)
                temp.append(d2[config])
                
            row = temp
            self.aut.append(row)


    def infoStr(self):
        return '\n'.join([
            'Type: split automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Total width: {}'.format(self.width),
            'Width of rule 1: {}'.format(self.width1),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])



##    def description(self):
##        '''rule 1, rule 2, total width, width for rule 1, height, seed'''
##        return 'SAut_{}_{}_{}_{}_{}_{}'.format(
##            self.rule1, self.rule2, self.width, self.width1,
##            self.height, self.seed )
