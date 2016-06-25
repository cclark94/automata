def replace(autom, state, replacement):
    '''Replaces every occurrence of "state" with "replacement"'''
    autom.addFilter('replace state:{} replacement:{}'.format(state, replacement))
    for i in range(autom.height):
        for j in range(autom.width):
            if autom.aut[i][j] == state: autom.aut[i][j] = replacement
