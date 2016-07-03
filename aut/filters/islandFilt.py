def iFilt(autom, state, lower, upper, replacement, negate=False):
    '''Island filter. If negate=Fase, replaces all islands such that
    lower <= size <= upper.
    If negate=True, replaces all islands such that size < lower or
    size > upper.'''
    
    # Shouldn't try to replace a state that doesn't exist
    assert state >= 0 and state < autom.stateCount

    # The replacement should either be an existing state or the state
    # one higher than the current maximum state (e.g., replacement could
    # be 2 for a binary automaton, which would turn the automaton into a
    # ternary automaton)
    assert replacement >= 0 and replacement <= autom.stateCount
    if replacement == autom.stateCount:
        autom.stateCount = replacement + 1
    
    autom.addFilter('iFilt state:{} lowerBound:{} upperBound:{} replacement:{} negate:{}'.format(
        state, lower, upper, replacement, negate))

    l = autom.aut
    # visited[i][j] tells whether the pixel at (i, j) has already been
    # found to be part of an island
    visited = [[False for j in range(len(l[i]))] for i in range(len(l))]
    # The new grid should be a copy of the original with EVERY occurence of
    # state replaced by replacement
    # When this function finishes, new will contain all islands such that
    # lower <= size <= upper, and l will contain all other islands
    new = [[0 for j in range(len(l[i]))] for i in range(len(l))]
    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] == state:
                new[i][j] = replacement
            else:
                new[i][j] = l[i][j]

    for i in range(len(l)):
        for j in range(len(l[i])):
            if l[i][j] == state and not visited[i][j]:
                # Stores the set of coordinates for pixels in the island
                coords = set()
                # The boolean value is all that matters, but it is placed
                # inside a list to make it mutable. If it is changed to True
                # in one recursive call, it will change to True in other
                # recursive calls too
                connects = [False]
                buildIsland(
                    l, visited, coords, connects, state, upper, i, j)
                # The biggest the island can get is upper+1. (This restriction
                # exists to keep the depth of recursion in buildIsland minimal.
                # Once the island's size reaches upper+1, we know it shouldn't
                # be copied over to new
                assert len(coords) <= upper+1
                # Three possible reasons to keep an island in l:
                # - size is below lower bound
                # - size is above upper 
                if len(coords) < lower or len(coords) > upper or connects[0]:
                    for (x, y) in coords:   
                        visited[x][y] = True
                # The pixels form an island such that lower <= size <= upper,
                # so they'll added to new but removed from l
                else:
                    for (x, y) in coords:
                        new[x][y] = state
                        l[x][y] = replacement
    if negate:
        for i in range(len(l)):
            for j in range(len(l[i])):
                l[i][j] = new[i][j]
        

def buildIsland(l, visited, coords, connects, state, cutoff, i, j):
    '''Recursively builds up an island of pixels.'''
    # Base cases:
    #   - Current pixel is not state
    #   - Current pixel is already in list of coordinates
    #   - Island is already big enough (size = cutoff+1)
    #   - Already known that island connects to a pre-existing island

    if l[i][j] == state and (i, j) not in coords and len(coords) < cutoff+1 \
       and not connects[0]:
        if visited[i][j]:
            connects[0] = True
        else:
            coords.add((i, j))
            if i > 0: buildIsland(
                l, visited, coords, connects, state, cutoff, i-1, j)
            if i < len(l)-1: buildIsland(
                l, visited, coords, connects, state,cutoff, i+1, j)
            width = len(l[0])
            buildIsland(l, visited, coords, connects, state, cutoff,
                        i, (j-1)%width)
            buildIsland(l, visited, coords, connects, state, cutoff,
                        i, (j+1)%width)
            
