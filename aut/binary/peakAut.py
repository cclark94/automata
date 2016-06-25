# The probability of rule1 varies from left to right. It starts at
# probStart, climbs to 1, and then descends back to probStart
# (upside-down V shape). 

# Formula: -abs( (1-probStart)*(2x-1) ) + 1, 0 <= x <= 1

from aut.baseAut import BaseAut
import random

class PAut(BaseAut):
    def __init__(self, rule1, rule2, probStart, width, height, seed=-1):
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.probStart = probStart
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d1 = PAut.ruleDict(rule1, 2)
        d2 = PAut.ruleDict(rule2, 2)
        
        if seed != -1:
            random.seed(seed)
        num = random.randint(0, 2**width-1) 

        row = PAut.decToBaseNList(num, 2)
        PAut.padList(row, width)        
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                proportionAcross = j/width
                rule1prob = -1 * abs(
                    (1-probStart) * (2*proportionAcross-1) ) + 1
                choice = random.random()
                if choice <= rule1prob: temp.append(d1[config])
                else: temp.append(d2[config])
            row = temp
            self.aut.append(row)


    def infoStr(self):
        return '\n'.join([
            'Type: peak automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Starting probability: {}'.format(self.probStart),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])
