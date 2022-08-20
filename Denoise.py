import numpy as np
import pywt

def denoise():
    mitdb_records = []
    num = [100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 111, 112, 113, 114, 115, 116, 117, 118, 119,
           121, 122, 123, 124, 200, 201, 202, 203, 205, 207, 208, 209, 210, 212, 213, 214, 215, 217, 219,
           220, 221, 222, 223, 228, 230, 231, 232, 233, 234]
    for i in range(48):
        path = 'E://MIT-BIH//' + np.str(num[i])
        mitdb_records.append(path)

    mitdb_signals, mitdb_beats, mitdb_beat_types = data.data_from_records(mitdb_records, channel=0)

    signals = []
    for i in range(48):
        sig = mitdb_signals[i]
        min = np.min(sig)
        max = np.max(sig)
        for j in range(len(sig)):
            sig[j] = float(sig[j] - min) / (max - min) * 2 - 1
        signals.append(sig)

    
    for i in range(48):
        coeffs = pywt.wavedec(signals[i], 'db8', level=9)
        coeffs[-1] = np.zeros(len(coeffs[-1]))
        coeffs[-2] = np.zeros(len(coeffs[-2]))
        coeffs[-3] = np.zeros(len(coeffs[-3]))
        coeffs[0] = np.zeros(len(coeffs[0]))
        signal = pywt.waverec(coeffs, 'db8')

        with open('E:/MIT-BIH/' + str(i) + '_denoise.txt', 'w') as outfile:
            np.savetxt(outfile, signal, fmt='%f', delimiter=',')
