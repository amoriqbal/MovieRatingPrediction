import numpy as np

def prepNBDset(masterDset,threshold,filterMinSize = 20):
    X = []
    y = []
    for movie in masterDset:
        if masterDset[movie]['Size'] < filterMinSize:
            continue
        try:
            for comment in masterDset[movie]['Comments']:
                try:
                    # yr.append(comment['Review'])
                    if comment['Rating'] <= threshold:
                        y.append(0)
                    else:
                        y.append(1)

                    X.append(comment['Title'])
                except:
                    continue
        except:

            continue
    return np.array(X),np.array(y)

def filterMinSize(masterDset, minSize):
    dset = dict()
    for movie in masterDset:
        if masterDset[movie]['Size'] >= minSize:
            dset[movie] = masterDset[movie]
    return dset

def filterMaxSize(masterDset, maxSize):
    dset = dict()
    for movie in masterDset:
        if masterDset[movie]['Size'] <= maxSize:
            dset[movie] = masterDset[movie]
    return dset