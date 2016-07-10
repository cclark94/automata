from aut.baseAut import BaseAut
import random

class SBlAut(BaseAut):
    '''Shifting blended automaton. Similar concept to BlAut class in
    blendedAutomaton.py. But the probability of rule1 changes as you move
    from the top to the bottom of the screen. At the top of the screen the
    probability is probStart, but it gradually transitions to probEnd.'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    
    def __init__(self, rule1, rule2, probStart, probEnd, width, height,
                 seed=None):
        if rule1 < SBlAut.RULE_MIN or rule1 > SBlAut.RULE_MAX:
            raise ValueError('rule1 outside of acceptable range')
        if rule2 < SBlAut.RULE_MIN or rule1 > SBlAut.RULE_MAX:
            raise ValueError('rule2 outside of acceptable range')
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
        self.prepareRandomSeed(seed)
        num = random.randint(0, 2**width-1)

        row = SBlAut.decToBaseNList(num, 2)
        SBlAut.padList(row, width)        
        self.aut.append(row)
        
        # Probability starts at probStart but gradually transitions
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
