from aut.baseAut import BaseAut
import random

class BlAut(BaseAut):
    '''Blended automaton. The user specifies two rules and the probability of
    the first rule being used; the probability of the second rule is
    1-probability. At each cell a random value is generated to determine which
    rule is applied.'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    
    def __init__(self, rule1, rule2, probability, width, height, seed=None):
        if rule1 < AAut.RULE_MIN or rule1 > AAut.RULE_MAX:
            raise ValueError('rule1 outside of acceptable range')
        if rule2 < AAut.RULE_MIN or rule1 > AAut.RULE_MAX:
            raise ValueError('rule2 outside of acceptable range')   
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.probability = probability
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d1 = BlAut.ruleDict(rule1, 2)
        d2 = BlAut.ruleDict(rule2, 2)
        self.prepareRandomSeed(seed)
        num = random.randint(0, 2**width-1)

        row = BlAut.decToBaseNList(num, 2)
        BlAut.padList(row, width)        
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                # Choose one of the two rules randomly
                rule = random.random()
                if rule <= probability: temp.append(d1[config])
                else: temp.append(d2[config])
            row = temp
            self.aut.append(row)


    def infoStr(self):
        return '\n'.join([
            'Type: blended automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Probability: {}'.format(self.probability),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])

