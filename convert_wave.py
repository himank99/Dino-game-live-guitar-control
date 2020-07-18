import chords_imp as ci
import numpy as np
import HPCP
def generate(chords_dir,chords,semi_tones,total_chords):
    chromas = np.zeros((sum(total_chords),13))
    k=0
    for i in range(len(chords)):
        for j in range(total_chords[i]):
            file = chords[i] + str(j+1) + '.wav'
            path = chords_dir + '/' + chords[i] + '/' + file
            chroma = HPCP.hpcp(path, norm_frames=False, win_size=4096, hop_size=1024, output='numpy')
            chroma = np.mean(chroma, axis=0)
            chroma /= sum(chroma)
            chroma = np.append(chroma, i)
            chromas[k]=chroma
            k+=1
    np.savetxt('pcp.data', chromas, delimiter=',')
generate(ci.chords_dir,ci.chords,ci.semi_tones,ci.total_chords)
