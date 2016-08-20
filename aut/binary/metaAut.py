from aut.baseAut import BaseAut
import random

class MAut(BaseAut):
    '''Meta automaton. The rules that get applied are based on the states of
    another automaton that has been created separately.'''

    RULE_MIN = 0
    RULE_MAX = 2**(2**3)-1
    
    def __init__(self, ruleAut, mapping, seed=None):
        # mapping is a dictionary that maps states in ruleAut to rules that
        # are applied. e.g., {0:25, 1:112, 2:56}
        for rule in mapping.values():
            if rule < MAut.RULE_MIN or rule > MAut.RULE_MAX:
                raise ValueError('rule outside of acceptable range')
        # Each state in ruleAut needs to appear as a key in mapping
        assert sorted(mapping.keys()) == list(range(0, ruleAut.stateCount))
        # The dimensions of the new automaton are the same as the dimensions of
        # the ruleAut
        width = ruleAut.width
        height = ruleAut.height
        super().__init__(width, height)
        self.mapping = mapping
        self.ruleAut = ruleAut
        # It would be good to generalize this to any statecount in the future
        self.stateCount = 2
        self.aut = list()

        # ruleDicts will map each state in ruleAut to the ruleDict for whatever
        # rule was specified in mapping
        ruleDicts = dict()
        for state in mapping:
            ruleDicts[state] = MAut.ruleDict(mapping[state], 2)

        self.prepareRandomSeed(seed)
        num = random.randint(0, 2**width-1)

        row = MAut.decToBaseNList(num, 2)
        MAut.padList(row, width)
        self.aut.append(row)

        for i in range(height-1):
            temp = list()
            for j in range(width):
                prev = row[(j-1) % width]
                curr = row[j]
                nxt = row[(j+1) % width]
                config = (prev, curr, nxt)
                # The rule that gets applied depends on the current cell
                # in ruleAut
                temp.append(ruleDicts[ruleAut.aut[i][j]][config])
            row = temp
            self.aut.append(row)

    def infoStr(self):
        return '\n'.join([
            'Type: meta automaton',
            'Mapping: {}'.format(self.mapping),
            'Seed: {}'.format(self.seed),
            'RuleAut:\n{}'.format(self.ruleAut) ])

        
