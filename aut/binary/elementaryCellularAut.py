# Elementary cellular automaton
# [add description here]

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
