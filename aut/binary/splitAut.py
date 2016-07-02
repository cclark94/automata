from aut.baseAut import BaseAut
import random

class SAut(BaseAut):
    '''Split automaton. The image is divided into two rectangular sections,
    one where rule1 is applied and another where rule2 is applied. User
    specifies the overall width and the with of rule1; the width of rule2
    will be (overall width - width of rule1).'''
    
    def __init__(self, rule1, rule2, width, width1, height, seed=None):
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.width1 = width1
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        
        d1 = SAut.ruleDict(rule1, 2)
        d2 = SAut.ruleDict(rule2, 2)
        width2 = width - width1
        self.prepareRandomSeed(seed)
        num = random.randint(0, 2**width-1)
        binStr = bin(num)[2:]

        row = SAut.decToBaseNList(num, 2)
        SAut.padList(row, width)        
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            for j in range(width1):
                prev = row[(j-1)%width]
                curr = row[j]
                nxt = row[(j+1)%width]
                config = (prev, curr, nxt)
                temp.append(d1[config])
                
            for k in range(width1, width):
                prev = row[(k-1)%width]
                curr = row[k]
                nxt = row[(k+1)%width]
                config = (prev, curr, nxt)
                temp.append(d2[config])
                
            row = temp
            self.aut.append(row)


    def infoStr(self):
        return '\n'.join([
            'Type: split automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Total width: {}'.format(self.width),
            'Width of rule 1: {}'.format(self.width1),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])
