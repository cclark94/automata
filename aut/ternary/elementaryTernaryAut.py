from aut.baseAut import BaseAut
import random

class ETAut(BaseAut):
    '''Elementary ternary automaton. Same idea as ECAut in
    binary/elementaryCellularAut.py, except that three states are used
    rather than two. This significantly increases the number of possible
    rules (from 2**(2**3) to 3**(3**3)).'''

    RULE_MIN = 0
    RULE_MAX = 3**(3**3)-1
    
    def __init__(self, rule, width, height, seed=None):
        if rule < ETAut.RULE_MIN or rule > ETAut.RULE_MAX:
            raise ValueError('rule1 outside of acceptable range')
        super().__init__(width, height)
        self.rule = rule
        self.seed = seed
        self.stateCount = 3
        self.aut = list()

        d = ETAut.ruleDict(rule, 3)
        self.prepareRandomSeed(seed)
        num = random.randint(0, 3**width-1)

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
    
