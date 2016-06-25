from PIL import Image
import random, string

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


    def infoStr(self):
        raise NotImplementedError()


    def addFilter(self, filterName):
        self.filters.append(filterName)


    def save(self, filename=None, magnification=1, colors=None):
        '''Creates a png image of the automaton and a log telling
        all of essential info about the automaton and image (i.e., everything
        you would need to reconstruct them).'''
        if filename ==  None:
            # Gets the name of the type of automaton (e.g., ECAut)
            prefix = str(type(self))[8:-2].split('.')[-1]
            # Generate random 16-character filename
            random.seed()
            filename = prefix + '_' + ''.join(random.choice(
                string.ascii_lowercase + string.ascii_uppercase + string.digits) \
                               for i in range(16))

        # Default color scheme for binary automaton: 0=white, 1=black
        if self.stateCount == 2 and not colors:
            colors = ((255, 255, 255), (0, 0, 0))
        # Default color scheme for ternary automaton: 0=red, 1=blue, 2=green
        elif self.stateCount == 3 and not colors:
            colors = ((255, 0, 0), (0, 255, 0), (0, 0, 255))

        self.saveImage(filename, colors, magnification)

        # Save info about automaton in a log
        f = open(filename + '.txt', 'w')
        f.write(self.__str__())
        f.write('\n\nMagnification: {}'.format(magnification))
        for i in range(len(colors)):
            f.write('\nColor for state {}: {}'.format(i, colors[i]))        
        f.close()        
            

    def saveImage(self, filename, colors, magnification):
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
                #im.putpixel((j, i), colors[self.aut[i][j]])
        im.save(filename + '.png')


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
