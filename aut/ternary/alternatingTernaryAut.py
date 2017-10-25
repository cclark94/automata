from aut.baseAut import BaseAut
import random

class ATAut(BaseAut):
    '''Alternating ternary automaton. Same idea as AAut in
    binary/alternatingAut.py, but three states are used rather than two.'''

    RULE_MIN = 0
    RULE_MAX = 3**(3**3)-1
    
    def __init__(self, rule1, rule2, width, height, seed=None):
        if width % 2 != 0:
            raise ValueError('AAut width must be even')
        if rule1 < ATAut.RULE_MIN or rule1 > ATAut.RULE_MAX:
            raise ValueError('rule1 outside of acceptable range')
        if rule2 < ATAut.RULE_MIN or rule1 > ATAut.RULE_MAX:
            raise ValueError('rule2 outside of acceptable range')  
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.seed = seed
        self.stateCount = 3
        self.aut = list()
        d1 = ATAut.ruleDict(rule1, 3)
        d2 = ATAut.ruleDict(rule2, 3)

        useD1 = True        
        self.prepareRandomSeed(seed)
        num = random.randint(0, 3**width-1)

        row = ATAut.decToBaseNList(num, 3)
        ATAut.padList(row, width)
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                if useD1: temp.append(d1[config])
                else: temp.append(d2[config])
                # Switch to other rule
                useD1 = not useD1
            row = temp
            self.aut.append(row)
            # Must flip an extra time after each row to make
            # checkerboard pattern
            useD1 = not useD1

    def infoStr(self):
        return '\n'.join([
            'Type: alternating ternary automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])
