from aut.baseAut import BaseAut
import random, math

class CAut(BaseAut):
    '''Connected automaton. There are two separate automata sharing the screen,
    but their leftmost cells influence each other. The two automata are binary
    automata, but their leftmost cells have to follow a special kind of rule
    since these cells are influenced not just by their immediate neighbors but
    also by the leftmost cell of the other automaton.  It would be good to
    generalize this so that you can have more than two separate automata.'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    # The leftmost cells are influenced by three other cells
    LEFT_RULE_MIN = 0
    LEFT_RULE_MAX = 2**(2**4) - 1

    def __init__(self, rule1, rule2, leftRule, width1, width2, height,
                 seed=None, separatorWidth=10):
        if rule1 < CAut.RULE_MIN or rule1 > CAut.RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        if rule2 < CAut.RULE_MIN or rule2 > CAut.RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        if leftRule < CAut.LEFT_RULE_MIN or \
           leftRule > CAut.LEFT_RULE_MAX:
            raise ValueError('rule outside of acceptable range')
        width = width1 + separatorWidth + width2
        super().__init__(width, height)
        self.rule1 = rule1
        self.rule2 = rule2
        self.leftRule = leftRule
        self.width1 = width1
        self.width2 = width2
        self.seed = seed
        self.separatorWidth = separatorWidth
        # Only two states for the actual automata, but the separator will use
        # a third state
        self.stateCount = 3
        self.aut = list()
        d1 = CAut.ruleDict(rule1, 2)
        d2 = CAut.ruleDict(rule2, 2)
        # The next state of the leftmost cell is determined based on the two
        # middle cells and the immediate neighbors of the leftmost cell.
        # So there are four cells being considered, which is the last argument
        # to generalizedRuleDict()
        leftD = CAut.generalizedRuleDict(leftRule, 2, 4)
        self.prepareRandomSeed(seed)
        # I think it would also be okay to just generate one random number
        # covering the entire width
        num1 = random.randint(0, 2**width1-1)
        num2 = random.randint(0, 2**width2-1)

        # A row consists of the rows of the two automata put side by side,
        # with a separator in between. The separator uses a separate state from
        # the states used in the automata
        row1 = CAut.decToBaseNList(num1, 2)
        row2 = CAut.decToBaseNList(num2, 2)
        CAut.padList(row1, width1)
        CAut.padList(row2, width2)
        row = row1 + [2]*separatorWidth + row2
        self.aut.append(row)
        
        for i in range(height-1):
            temp = list()
            w1floor = math.floor(width1/2)
            w1ceil = math.ceil(width1/2)
            w2floor = math.floor(width2/2)
            w2ceil = math.ceil(width2/2)

            # Leftmost cell of first automaton
            # Order for cells being considered:
            # left neighbor, self, right neighbor, other leftmost
            # Wrap around for its left neighbor
            prev = row[width1-1]
            curr = row[0]
            nxt = row[1]
            # The other leftmost cell
            other = row[width1 + separatorWidth]
            config = (prev, curr, nxt, other)
            temp.append(leftD[config])

            # Remaining cells for first automaton
            for j in range(1, width1):
                prev = row[j - 1]
                curr = row[j]
                nxt = row[(j+1) % width1]
                config = (prev, curr, nxt)
                temp.append(d1[config])

            # Separator
            temp.extend([2]*separatorWidth)

            # Repeat for second automaton
            w = width1 + separatorWidth
            # Leftmost cell of second automaton
            # Wrap around for its left neighbor
            prev = row[width - 1]
            curr = row[w]
            nxt = row[w + 1]
            other = row[0]
            config = (prev, curr, nxt, other)
            temp.append(leftD[config])

            # Remaining cells for second automaton
            for j in range(1, width2):
                prev = row[w + j - 1]
                curr = row[w + j]
                nxt = row[w + (j+1) % width2]
                config = (prev, curr, nxt)
                temp.append(d2[config])

            row = temp
            self.aut.append(row)
            
            
##            # Left side of first automaton
##            for j in range(w1floor):
##                #prev = row[(j-1) % w1floor]
##                prev = row[(j-1) % width1]
##                curr = row[j]
##                nxt = row[j+1]
##                config = (prev, curr, nxt)
##                temp.append(d1[config])
##            # Middle column of first automaton
##            # Order for cells being considered:
##            # left neighbor, self, right neighbor, other middle
##            # The modulos are probably unnecessary
##            prev = row[(w1floor-1) % width1]
##            curr = row[w1floor]
##            nxt = row[(w1floor+1) % width1]
##            other = row[width1 + separatorWidth + w2floor]
##            config = (prev, curr, nxt, other)
##            temp.append(middleD[config])
##            # Right side of first automaton
##            for j in range(w1ceil, width1):
##                prev = row[j-1]
##                curr = row[j]
##                #nxt = row[(j+1-w1ceil) % w1floor + w1ceil]
##                nxt = row[(j+1) % width1]
##                config = (prev, curr, nxt)
##                temp.append(d1[config])
##            # Separator
##            temp.extend([2]*separatorWidth)
##            # repeat for the second automaton
##            w = width1 + separatorWidth
##            # Left side of second automaton
##            for j in range(w2floor):
##                #prev = row[w + ((j-1)%w2floor)]
##                prev = row[w + ((j-1)%width2)]
##                curr = row[w + j]
##                nxt = row[w + j + 1]
##                config = (prev, curr, nxt)
##                temp.append(d2[config])
##            # Middle column of second automaton
##            # Again, modulos are probably unnecessary
##            prev = row[w + (w2floor-1)%width2]
##            curr = row[w + w2floor]
##            nxt = row[w + (w2floor+1)%width2]
##            other = row[w1floor]
##            config = (prev, curr, nxt, other)
##            temp.append(middleD[config])
##            # Right side of second automaton
##            for j in range(w2ceil, width2):
##                prev = row[w + j - 1]
##                curr = row[w + j]
##                #nxt = row[w + ((j+1-w2ceil) % w2floor + w2ceil)]
##                nxt = row[w + ((j+1)%width2)]
##                config = (prev, curr, nxt)
##                temp.append(d2[config])
##            row = temp
##            self.aut.append(row)

    def infoStr(self):
        return '\n'.join([
            'Type: connected automaton',
            'Rule1: {}'.format(self.rule1),
            'Rule2: {}'.format(self.rule2),
            'Leftmost rule: {}'.format(self.leftRule),
            'Width1: {}'.format(self.width1),
            'Width2: {}'.format(self.width2),
            'Separator width: {}'.format(self.separatorWidth),
            'Height: {}'.format(self.height),
            'Seed: {}'.format(self.seed) ])        
        
        
