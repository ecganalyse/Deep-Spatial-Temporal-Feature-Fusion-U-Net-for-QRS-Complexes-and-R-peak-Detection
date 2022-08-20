import numpy as np

def dwtr(y,yt,threshold):
    resultSet = {}
    l1 = len(y)
    width = []
    jg = []
    yi = []
    i = 0
    while i < l1-1:
        time = 0
        x = y[i]
        z = y[i]
        while y[i+1] - y[i] < 10 and i < l1-2:
            time += 1
            z = y[i]
            i += 1
        width.append(time+1)
        jg.append(y[i+1] - y[i])
        yi.append(int((z + x) / 2))
        i += 1

    del jg[-1]

    min_width = min(width)
    min_width_index = width.index(min_width)
    for T1 in list(range(0,1,0.1)):
        while min_width < T1 * np.mean(width):
            if min_width_index > len(width)-2:
                break
            if jg[min_width_index - 1] + min_width + jg[min_width_index] < 1.5*np.mean(jg):
                jg[min_width_index - 1] += min_width + jg[min_width_index]
                del jg[min_width_index]
                del width[min_width_index]
                del yi[min_width_index]
            else:
                width[min_width_index] *= 2
            min_width = min(width)
            min_width_index = width.index(min_width)

        for T2 in list(range(0, 1, 0.1)):
            i = 0
            while i < len(width)-1:
                if width[i] < T2 * np.mean(width):
                    del width[i]
                    del jg[i]
                    del yi[i]
                i += 1

            for T3 in list(range(0, 1, 0.1)):
                i = 0
                while i < len(jg)-1:
                    if jg[i] < T3 * np.mean(jg):
                        del width[i]
                        del jg[i]
                        del yi[i]
                    i += 1
                resultSet.setdefault(T1+"+"+T2+"+"+T3, compare(yi, yt, threshold))

    T1,T2,T3 = getMaxValue(resultSet)
    return T1,T2,T3

def compare(y,yt,threshold):
    TP = 0 #检测正确
    FN = 0 #漏检
    FP = 0 #错检

    for i in range(len(y)):
        m = min(abs(y[i] - yt))
        if m < threshold:
            TP += 1
        else:
            FP += 1
    FN = abs(len(yt) - len(y) + FP)

    return TP / (TP + FN + FP)
