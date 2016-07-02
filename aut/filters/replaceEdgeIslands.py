import queue

def replaceEdgeIslands(autom, state, replacement):
    '''Replaces all islands of "state" that wrap around the left and right edges
    of autom, regardless of the islands' size.'''

    autom.addFilter('replaceEdgeIslands state:{} replacement:{}'.format(
        state, replacement))

    # Shouldn't try to replace a state that doesn't exist
    assert state >= 0 and state < autom.stateCount

    # The replacement should either be an existing state or the state
    # one higher than the current maximum state (e.g., replacement could
    # be 2 for a binary automaton, which would turn the automaton into a
    # ternary automaton)
    assert replacement >= 0 and replacement <= autom.stateCount
    if replacement == autom.stateCount:
        autom.stateCount = replacement + 1

    # Performed using a simple breadth-first search
    l = autom.aut
    width = autom.width
    height = autom.height
    for i in range(height):
        if l[i][0] == state and l[i][width-1] == state:
            q = queue.Queue()
            l[i][0] = replacement
            l[i][width-1] = replacement
            q.put((i, 0))
            q.put((i, width-1))
            while not q.empty():
                (x, y) = q.get()
                # up
                if x > 0 and l[x-1][y] == state:
                    l[x-1][y] = replacement
                    q.put((x-1, y))
                # down
                if x < height-1 and l[x+1][y] == state:
                    l[x+1][y] = replacement
                    q.put((x+1, y))
                # left
                if l[x][(y-1)%width] == state:
                    l[x][(y-1)%width] = replacement
                    q.put((x, (y-1)%width))
                # right
                if l[x][(y+1)%width] == state:
                    l[x][(y+1)%width] = replacement
                    q.put((x, (y+1)%width))

