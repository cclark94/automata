from aut.baseAut import BaseAut
import random

class FAut(BaseAut):
    '''Flip automaton. Randomly flips bits after they have been generated
    according to a user-specified probability'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    
    def __init__(self, rule, probability, width, height, seed=None):
        if rule < FAut.RULE_MIN or rule > FAut.RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        super().__init__(width, height)
        self.rule = rule
        self.probability = probability
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d = FAut.ruleDict(rule, 2)
        self.prepareRandomSeed(seed)
        num = random.randint(0, 2**width-1)

        row = FAut.decToBaseNList(num, 2)
        FAut.padList(row, width)        
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                result = d[config]
                # Generate random value r and flip result if r is
                # below probability
                # General (not just binary) way this could be done:
                # result = (result + 1) % self.stateCount
                r = random.random()
                if r < probability:
                    result = 1 - result
                temp.append(result)
            row = temp
            self.aut.append(row)

    def infoStr(self):
        return '\n'.join([
            'Type: flip automaton',
            'Rule: {}'.format(self.rule),
            'Probability: {}'.format(self.probability),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])
