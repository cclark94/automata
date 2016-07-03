def rFilt(autom, state, replacement):
    '''Replace filter. Replaces every occurrence of "state" with
    "replacement"'''
    
    autom.addFilter('rFilt state:{} replacement:{}'.format(state, replacement))
    for i in range(autom.height):
        for j in range(autom.width):
            if autom.aut[i][j] == state: autom.aut[i][j] = replacement
