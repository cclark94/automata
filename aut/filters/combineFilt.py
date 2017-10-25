def cFilt(autom1, autom2, mapping):
    '''Combine filter. autom1 and autom2 must have the same dimensions. Loop
    through the automata, and at each cell, check to see if
    (autom1.aut[i][j], autom2.aut[i][j]) appears as a key in mapping. If it
    does, replace autom1.aut[i][j] with the associated value.

    mapping is a dictionary in this format:
    {(autom1_state, autom2_state) : resultant_autom1_state), ...}

    As an example, say that autom1 and autom2 are binary automata and you
    want to turn autom1.aut into autom1.aut XOR autom2.aut. This is the mapping:
    { (0, 0): 0, (0, 1):1, (1, 0):1, (1, 1):0 }

    Note: I'm pretty sure that you could do XOR with a simpler mapping too:
    { (0, 1): 1, (1, 1):0 }. You don't need to specify the other two
    possibilities, because they won't be changed in autom1 after the filter
    is applied.'''
    
    assert len(autom1.aut) == len(autom2.aut)
    assert len(autom1.aut[0]) == len(autom2.aut[0])
    autom1.addFilter('cFilt mapping:{} autom2:\n{}'.format(
        mapping, autom2.__str__()))
    for i in range(len(autom1.aut)):
        for j in range(len(autom1.aut[i])):
            pair = (autom1.aut[i][j], autom2.aut[i][j])
            # If pair isn't in mapping, the current cell of autom1 will be
            # left unchanged
            if pair in mapping:
                autom1.aut[i][j] = mapping[pair]
                
