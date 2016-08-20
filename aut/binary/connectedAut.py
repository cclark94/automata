from aut.baseAut import BaseAut
import random, math

class CAut(BaseAut):
    '''Connected automaton. There are two separate automata sharing the screen,
    but their middle cells influence each other. The two automata are binary
    automata, but their middle cells have two follow a special kind of rule
    since these cells only have one neighbor. (Later I might want to try making
    these cells have three neighbors: the normal two neighbors and then also
    the middle cell of the other automaton. And it would be good to generalize
    this so that you can have more than two separate automata.'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    # The middle cells just have one neighbor: the other middle cell
    MIDDLE_RULE_MIN = 0
    MIDDLE_RULE_MAX = 2**(2**2)

    def __init__(self, rule, middleRule, width1, width2, height, seed=None):
        if rule < CAut.RULE_MIN or rule > CAut.RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        if middleRule < CAut.MIDDLE_RULE_MIN or middleRule > CAut.MIDDLE_RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        # Widths should be odd so that there's a middle column for each
        # automaton
        assert width1 % 2 == 1
        assert width2 % 2 == 1
        width = width1 + width2
        super().__init__(width, height)
        self.rule = rule
        self.middleRule = middleRule
        self.width1 = width1
        self.width2 = width2
        self.seed = seed
        self.stateCount = 2
        self.aut = list()
        d = CAut.ruleDict(rule, 2)
        # The next state of the middle cell is determine based on the current
        # state of both middle cells. So there are only 2 cells being
        # considered, which is the last argument to generalizedRuleDict()
        middleD = CAut.generalizedRuleDict(middleRule, 2, 2)
        self.prepareRandomSeed(seed)
        # I think it would also be okay to just generate one random number
        # covering the entire width
        num1 = random.randint(0, 2**width1-1)
        num2 = random.randint(0, 2**width2-1)

        # A row consists of the rows of the two automata put side by side
        row = CAut.decToBaseNList(num1, 2) + CAut.decToBaseNList(num2, 2)
        CAut.padList(row, width)
        self.aut.append(row)
        for i in range(height-1):
            temp = list()
            w1floor = math.floor(width1/2)
            w1ceil = math.ceil(width1/2)
            w2floor = math.floor(width2/2)
            w2ceil = math.ceil(width2/2)
            # Left side of first automaton
            for j in range(w1floor):
                prev = row[(j-1) % w1floor]
                curr = row[j]
                nxt = row[j+1]
                config = (prev, curr, nxt)
                temp.append(d[config])
            # Middle column of first automaton
            curr = row[w1floor]
            other = row[width1 + w2floor]
            config = (curr, other)
            temp.append(middleD[config])
            # Right side of first automaton
            for j in range(w1ceil, width1):
                prev = row[j-1]
                curr = row[j]
                nxt = row[(j+1-w1ceil) % w1floor + w1ceil]
                config = (prev, curr, nxt)
                temp.append(d[config])
            # repeat for the second automaton
            # Left side of second automaton
            for j in range(w2floor):
                prev = row[width1 + ((j-1)%w2floor)]
                curr = row[width1 + j]
                nxt = row[width1 + j + 1]
                config = (prev, curr, nxt)
                temp.append(d[config])
            # Middle column of second automaton
            curr = row[width1 + w2floor]
            other = row[w1floor]
            config = (curr, other)
            temp.append(middleD[config])
            # Right side of second automaton
            for j in range(w2ceil, width2):
                prev = row[width1 + j - 1]
                curr = row[width1 + j]
                nxt = row[width1 + ((j+1-w2ceil) % w2floor + w2ceil)]
                config = (prev, curr, nxt)
                temp.append(d[config])
            row = temp
            self.aut.append(row)

    def infoStr(self):
        return '\n'.join([
            'Type: connected automaton',
            'Rule: {}'.format(self.rule),
            'Middle rule: {}'.format(self.middleRule),
            'Width1: {}'.format(self.width1),
            'Width2: {}'.format(self.width2),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])        
        
        
