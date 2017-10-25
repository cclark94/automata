from PIL import Image
import random, string, sys

class BaseAut:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Stores the list of filters that have been applied
        # to the automaton
        self.filters = list()


    def __str__(self):
        s = self.infoStr()
        if self.filters:
            s += '\n\nFilters:'
        for i in range(len(self.filters)):
            s += '\n{}. {}'.format(i+1, self.filters[i])
        return s


    def prepareRandomSeed(self, seed):
        '''There are three possibilities:
        1. The user specifies a seed as a positive integer. The automaton will
        be generated using this random seed.
        2. The user doesn't specify the seed. In this case, a seed will be
        chosen at random; if the the user saves the automaton, the random seed
        will be specified in the log file. So an automaton generated this way
        could be regenerated exactly.
        3. The user specifies -1 as the seed. This is like case (2), except that
        the seed won't be recorded and won't appear on the log file. It won't
        be possible to exactly duplicate the automaton using the log file, since
        the seed will be unknown.'''
        if seed:
            if seed == -1:
                self.seed = "<hidden>"
            else:
                random.seed(seed)
                self.seed = seed
        else:
            seed = random.randint(0, sys.maxsize)
            random.seed(seed)
            self.seed = seed


    def infoStr(self):
        raise NotImplementedError()


    def addFilter(self, filterName):
        self.filters.append(filterName)


    def save(self, filename=None, magnification=1, colors=None):
        '''Creates a png image of the automaton and a log telling
        all of essential info about the automaton and image (i.e., everything
        you would need to reconstruct them).'''
        if filename == None:
            filename = BaseAut.__generateFileName(self)
        if colors == None:
            colors = BaseAut.__getDefaultColors(self)
            
        self.saveImage(filename, magnification, colors)

        # Save info about automaton in a log
        f = open(filename + '.log', 'w')
        f.write(self.__str__())
        f.write('\n\nMagnification: {}'.format(magnification))
        for i in range(len(colors)):
            f.write('\nColor for state {}: {}'.format(i, colors[i]))        
        f.close()        
            

    def saveImage(self, filename=None, magnification=1, colors=None):
        if filename == None:
            filename = BaseAut.__generateFileName(self)
        if colors == None:
            colors = BaseAut.__getDefaultColors(self)

        assert type(magnification) == int and magnification >= 1
        assert len(colors) == self.stateCount

        im = Image.new(
            'RGB', (self.width*magnification, self.height*magnification),
            (255, 255, 255) )
        for i in range(self.height):
            for j in range(len(self.aut[i])):
                for k in range(magnification):
                    for l in range(magnification):
                        im.putpixel(
                            (j*magnification+k, i*magnification+l),
                            colors[self.aut[i][j]] )
        im.save(filename + '.png')


    @staticmethod
    def __generateFileName(aut):
        # Gets the name of the type of automaton (e.g., ECAut)
        prefix = str(type(aut))[8:-2].split('.')[-1]
        # Generate random 16-character filename
        random.seed()
        return prefix + '_' + ''.join(random.choice(
            string.ascii_lowercase + string.ascii_uppercase + string.digits) \
                           for i in range(16))


    @staticmethod
    def __getDefaultColors(aut):
        # Default color scheme for binary automaton: 0=white, 1=black
        if aut.stateCount == 2:
            return ((255, 255, 255), (0, 0, 0))
        # Default color scheme for ternary automaton: 0=red, 1=blue, 2=green
        elif aut.stateCount == 3:
            return ((255, 0, 0), (0, 255, 0), (0, 0, 255))
        else: return None
            

    @staticmethod
    def ruleDict(code, base):
        '''code is the Wolfram code for an automaton, ranging from 0 to
        base**(base**3).
        Returns a dictionary telling the resulting cell state for each
        possible configuration.'''
        assert code >= 0 and code < base**(base**3)
        d = dict()
        ruleList = BaseAut.decToBaseNList(code, base)
        BaseAut.padList(ruleList, base**3)
        # Keep track of position in ruleList
        ind = 0
        for i in range(base-1, -1, -1):
            for j in range(base-1, -1, -1):
                for k in range(base-1, -1, -1):
                    d[(i, j, k)] = ruleList[ind]
                    ind += 1
        return d

    @staticmethod
    def generalizedRuleDict(code, base, cellCount=3):
        '''code is the Wolfram code for an automaton, ranging from 0 to
        base**(base**neighborCount).
        Returns a dictionary telling the resulting cell state for each possible
        configuration.
        The difference between this and ruleDict() is that this allows the user
        to specify the cell count, meaning the number of cells used to determine
        the next state of a particular cell. (cellCount is 3 for a standard cellular
        automaton.)
        Once I'm sure this method is working, I can rename this
        as ruleDict and get rid of the old ruleDict() method.'''
        assert code >= 0 and code < base**(base**cellCount)
        d = dict()
        ruleList = BaseAut.decToBaseNList(code, base)
        BaseAut.padList(ruleList, base**cellCount)
        maximum = base ** cellCount - 1
        # Keep track of position in ruleList
        ind = 0
        for i in range(maximum, -1, -1):
            # Get rid of leading '0b'
            config = bin(i)[2:]
            config = [int(c) for c in config]
            BaseAut.padList(config, cellCount)
            config = tuple(config)
            d[config] = ruleList[ind]
            ind += 1
        return d
            

    @staticmethod
    def decToBaseNList(n, base):
        '''Returns n converted to the specified base. The answer is in list
        form (e.g., 123456 = [1, 2, 3, 4, 5, 6])'''
        l = list()
        while n > 0:
                l = [n%base] + l
                n = n // base
        return l


    @staticmethod
    def padList(l, length):
        '''Adds on 0's to the beginning of l to make its length match what
        the user specifies.'''
        l.reverse()
        l.extend([0]*(length - len(l)))
        l.reverse()
