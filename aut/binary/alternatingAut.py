from aut.baseAut import BaseAut
import random

class AAut(BaseAut):
    '''Alternating automaton.  Cells alternate between two rules,
    following a checkerboard pattern:

     ABABABABABABABAB
     BABABABABABABABA
     ABABABABABABABAB
     BABABABABABABABA
     etc.

     In order to make this pattern, the width must be even.'''
    
    def __init__(self, rule1, rule2, width, height, seed=None):
        # Width must be even
        assert width % 2 == 0
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d1 = AAut.ruleDict(rule1, 2)
        d2 = AAut.ruleDict(rule2, 2)
        
        useD1 = True
        self.prepareRandomSeed(seed)

        num = random.randint(0, 2**width-1)
        row = AAut.decToBaseNList(num, 2)
        AAut.padList(row, width)        
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
            'Type: alternating automaton',
            'Rule 1: {}'.format(self.rule1),
            'Rule 2: {}'.format(self.rule2),
            'Width: {}'.format(self.width),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])        
