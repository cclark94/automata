from aut.baseAut import BaseAut
import random

class PAut(BaseAut):
    '''Peak automaton. The user specifies two rules and a starting probability,
    probStart. At the left edge of the image, the probability of rule1 is
    probStart, but it climbs up to 1 at the middle of the image and then
    descends back to probStart at the right edge (picture an upside-down V).

    Formula to calculate probability of rule1:
    -abs( (1-p)*(2x-1) ) + 1,
    where p is the starting probability of rule 1 (0 <= p <= 1) and x is the
    proportion across the screen (0 <= x <= 1).'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    
    def __init__(self, rule1, rule2, probStart, width, height, seed=None):
        if rule1 < AAut.RULE_MIN or rule1 > AAut.RULE_MAX:
            raise ValueError('rule1 outside of acceptable range')
        if rule2 < AAut.RULE_MIN or rule1 > AAut.RULE_MAX:
            raise ValueError('rule2 outside of acceptable range')    
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.probStart = probStart
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d1 = PAut.ruleDict(rule1, 2)
        d2 = PAut.ruleDict(rule2, 2)
        self.prepareRandomSeed(seed)
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
