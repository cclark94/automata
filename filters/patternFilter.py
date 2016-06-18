##def patternFilter3(autom, pattern, state):
##    '''3x3 patterns.
##    Pattern format: 'XXX XXX XXX', where X can be 0 or 1, and the fifth
##    X is the cell that will be changed if there's a match.'''   
##    autom.addFilter('patternFilter({}, {})'.format(
##        pattern.replace(' ', '_'), state))
##    # Convert pattern into list of list of ints
##    pattern = list(list(int(c) for c in r) for r in pattern.split()) 
##    aut = autom.aut
##    # Deep copy of aut
##    duplicate = list(list(c for c in r) for r in aut)
##    width = len(aut[0])
##    for row in range(1, len(aut)-1):
##        for col in range(width):
##            match = True
##            r = 0
##            while r < 3 and match:
##                c = 0
##                while c < 3 and match:
##                    if aut[row-1+r][(col-1+c)%width] != pattern[r][c]:
##                        match = False
##                    c += 1
##                r += 1
##            if match:
##                duplicate[row][col] = state
##    # Copy contents of duplicate over to aut
##    for i in range(len(aut)):
##        for j in range(width):
##            aut[i][j] = duplicate[i][j]


def patternFilter(autom, pattern, new):
    '''Searches for occurrences of a rectangular pattern and replaces them
    with "new". The character "X" can be used (1) to indicate that a state
    in "pattern" should be disregarded (i.e., any state is okay) or (2) to
    indicate that the state should stay the same.

    Patterns are entered as strings. For instance:
    patternFilter(a, 'X1X 010 X1X', 'XXX 101 XXX')'''

    assert len(pattern) == len(new)
    autom.addFilter('patternFilter pattern:{} replacement:{}'.format(
        pattern.replace(' ', '_'), new.replace(' ', '_')))

    # Convert pattern and new into list of list of ints
    pattern = list(list(c for c in r) for r in pattern.split())
    # Convert everything except 'X' into an integer
    for r in range(len(pattern)):
        for c in range(len(pattern[r])):
            if pattern[r][c] != 'X':
                pattern[r][c] = int(pattern[r][c])

    new = list(list(c for c in r) for r in new.split())
    # Convert everything except 'X' into an integer
    for r in range(len(new)):
        for c in range(len(new[r])):
            if new[r][c] != 'X':
                new[r][c] = int(new[r][c])
    
    aut = autom.aut
    # Deep copy of aut
    duplicate = list(list(c for c in r) for r in aut)

    autWidth = len(aut[0])
    patWidth = len(pattern[0])
    patHeight = len(pattern)

    for row in range(len(aut)-patHeight+1):
        for col in range(autWidth):
            match = True
            r = 0
            while r < patHeight and match:
                c = 0
                while c < patWidth and match:
                    curr = aut[row+r][(col+c)%autWidth]
                    if curr != pattern[r][c] and pattern[r][c] != 'X':
                        #print('curr:{} pat:{}'.format(curr, pattern[r][c]))
                        match = False
                    c += 1
                r += 1
            
            if match:
                #print('match')
                for r in range(patHeight):
                    for c in range(patWidth):
                        if new[r][c] != 'X':
                            duplicate[row+r][(col+c)%autWidth] = new[r][c]

    # Copy contents of duplicate over to aut
    for i in range(len(aut)):
        for j in range(autWidth):
            aut[i][j] = duplicate[i][j]
                    
    
    
    
