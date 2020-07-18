import os

chords_dir = 'Desktop/dino/Guitar_Only'
if os.path.isdir(chords_dir):
    chords = []
    for c in os.listdir(chords_dir):
        if not os.path.isfile(c):
            chords.append(c)
    chords.sort()
    #print(chords)
else:
    chords = ['a', 'am', 'bm', 'c', 'd', 'dm', 'e', 'em', 'f', 'g']
semi_tones = ['c', 'c#', 'd', 'd#', 'e', 'f', 'f#', 'g', 'g#', 'a', 'a#', 'b']
total_chords = []
for c in chords:
    total_chords.append(len(os.listdir(chords_dir + '/'+ c)))
#print(total_chords)
