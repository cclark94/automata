# Like probRangeBlendedAutomaton in the messy code

#from aut.binary.binaryAut import BAut
from aut.baseAut import BaseAut
import random

class SBlAut(BaseAut):
    def __init__(self, rule1, rule2, probStart, probEnd, width, height,
                 seed=-1):
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.probStart = probStart
        self.probEnd = probEnd
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        
        d1 = SBlAut.ruleDict(rule1, 2)
        d2 = SBlAut.ruleDict(rule2, 2)
        if not seed == -1:
            random.seed(seed)
        num = random.randint(0, 2**width-1)

##        binStr = bin(num)[2:]
##        # Add leading zeroes if necessary
##        binStr = '0' * (width - len(binStr)) + binStr
##        row = SBlAut.binStrToList(binStr)  
##        self.aut.append(row)

        row = SBlAut.decToBaseNList(num, 2)
        SBlAut.padList(row, width)        
        self.aut.append(row)
        
        # Probability starts at probStart but gradually increases
        # to probEnd
        probCurr = probStart
        probStep = (probEnd-probStart)/(height-1)
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                # Choose one of the two rules randomly
                rule = random.random()
                if rule <= probCurr: temp.append(d1[config])
                else: temp.append(d2[config])
            row = temp
            self.aut.append(row)
            probCurr += probStep

    def infoStr(self):
        return '\n'.join([
            'Type: shifting blended automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Starting probability of rule 1: {}'.format(self.probStart),
            'Ending probability of rule 1: {}'.format(self.probEnd),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])

##    def description(self):
##        '''rule1, rule2, probStart, probEnd, width, height, seed'''
##        return 'SBlAut_{}_{}_{}_{}_{}_{}_{}'.format(
##            self.rule1, self.rule2, self.probStart, self.probEnd,
##            self.width, self.height, self.seed )
        
