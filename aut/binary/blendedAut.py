# Note: this is like probabilisticBlendedAutomaton from the messy code

# User specifies the probability that the first rule will be used. Probability
# of second rule equals 1 - specified probability

from aut.baseAut import BaseAut
import random

class BlAut(BaseAut):
    def __init__(self, rule1, rule2, probability, width, height, seed=-1):
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.probability = probability
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d1 = BlAut.ruleDict(rule1, 2)
        d2 = BlAut.ruleDict(rule2, 2)
        
        if seed != -1:
            random.seed(seed)
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

