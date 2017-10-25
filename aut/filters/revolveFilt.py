def rFilt(autom, amount, proportion=True):
    '''Revolve filter. Rotates the columns in autom from left to right. For
    instance, ABCDEF rotated by 1 would become FABCDE.

    When proportion is True, the user specifies a number between 0 and 1.
    For instance a rotation of 0.5 with proportion=True would rotate
    ABCDEF to DEFABC. If proprtion is False, the user specifies a number of
    pixels to rotate instead.'''
