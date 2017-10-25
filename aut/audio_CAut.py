# Converts a CAut to an audio file. The CAut is assumed to have two connected
# automata with width 6 and 3 respectively. The 6-wide automaton determines
# pitch, and the 3-wide determines rhythm.

import pysynth_b as ps

def getAudio(autom, filename):
    '''Creates a sound file from a CAut object.'''
    aut = autom.aut
    pitches = [row[:6] for row in aut]
    # Adding seven puts the pitches in a more reasonable range (otherwise they'd
    # go down to low A.
    pitches = [numberToPitch(listToNumber(p)+7) for p in pitches]
    # The last three cells in each row determine the rhythm
    rhythms = [row[-3:] for row in aut]
    rhythms = [numberToRhythm(listToNumber(r)) for r in rhythms]
    notes = [(pitches[i], rhythms[i]) for i in range(len(pitches))]
    ps.make_wav(notes, fn=filename)
    
def listToNumber(l):
    '''Converts a list of binary digits into a decimal number.
    For instance, [1, 0, 1] becomes 5.'''
    return int(''.join(str(x) for x in l), 2)            
            
def numberToPitch(n):
    '''n is a number representing a key on the piano. 0 is low A and
    87 is high C. Returns the scientific pitch notation. For instance,
    15 will return c2.'''
    pitches = ['c', 'db', 'd', 'eb', 'e', 'f',
               'gb', 'g', 'ab', 'a', 'bb', 'b']
    pitch = pitches[(n-3)%12]
    octave = (n+9)//12
    return pitch + str(octave)

def pitchToNumber(p):
    pitchNumbers = {'c':0, 'db':1, 'd':2, 'eb':3, 'e':4, 'f':5,
                    'gb':6, 'g':7, 'ab':8, 'a':9, 'bb':10, 'b':11}
    # Flat pitches
    if p[1] == 'b':
        pitch = p[:2]
        octave = int(p[2:])
    else:
        pitch = p[0]
        octave = int(p[1:])
    return (octave-1)*12 + 3 + pitchNumbers[pitch]

def numberToRhythm(n):
    '''n is a number between 0 and 7.'''
    # 0 = sixteenth note (16)
    # 1 = dotted sixteenth (-16)
    # 2 = eighth note (8)
    # 3 = dotted eighth (-8)
    # 4 = quarter note (4)
    # 5 = dotted quarter (-4)
    # 6 = half note (2)
    # 7 = dotted half (-2)
    return (-1)**(n%2) * 2**(4-n//2)
    

