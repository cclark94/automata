from aut.baseAut import BaseAut
import random

class ECAut(BaseAut):
    '''Elementary cellular automaton. This is the most basic kind of automaton
    available. The rule-numbering convention is based on Wolfram codes. You
    can read more about elementary cellular automata at
    https://en.wikipedia.org/wiki/Elementary_cellular_automaton.'''
    
    def __init__(self, rule, width, height, seed=None):
        super().__init__(width, height)
        self.rule = rule
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d = ECAut.ruleDict(rule, 2)
        self.prepareRandomSeed(seed)
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
