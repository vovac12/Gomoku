import random as rd


trained = {'1n': 0.0,
           '1w': 1.7927745815682576,
           '2m': 2.46183734964439,
           '2n': 0.8281654847214509,
           '2w': 28.328990106158763,
           '3a': 3.919455296544752,
           '3m': 3.2543738602658467,
           '3n': 0.9439557240746125,
           '3w': 390.034915638539,
           'ac': 0.8579854604253398,
           'dc': 1.4669388088150683}


def RdAI(game):
    return rd.choice(game.avail)


def ImRdAI(game):
    res = set()
    res.add(rd.choice(game.avail))
    for i in range(game.size):
        for j in range(game.size):
            if game.board[i][j] == game.player:
                res.add((i + 1, j))
                res.add((i + 1, j + 1))
                res.add((i + 1, j - 1))
                res.add((i, j + 1))
                res.add((i - 1, j))
                res.add((i - 1, j + 1))
                res.add((i - 1, j - 1))
                res.add((i, j - 1))
    res = res.intersection(set(game.avail))
    return rd.choice(tuple(res))


def AI(game, kw={'ac': 1.01, 'dc': 0.99, '3w': 300, '3m': 4, '3n': 0.75,
                 '2w': 50, '2m': 2, '2n': 0.75, '1w': 3, '1n': 0, '3a': 4}):
    chlist = []
    if not game.avail:
        return 1
    wt = []
    coef = (kw['dc'], kw['ac'])
    curp = 0 if game.player == 1 else 1
    if game.player == -1:
        coef = coef[::-1]
    for i in range(2):
        for j in game.diags_p[i - curp]:
            if j[0].count('x') == 4:
                if '.' not in j[0].strip('.'):
                    return j[1][j[0].index('.')]
                else:
                    return j[1][j[0][1:].index('.') + 1]
            elif j[0][0] == 'n' and j[0][-1] == 'n':
                continue
            elif j[0].count('x') == 3:
                co = kw['3w'] * coef[i]
                if 'xxx' in j[0]:
                    co *= kw['3m']
                    if 'n' not in j[0]:
                        co *= kw['3a']
                if 'n' in j[0]:
                    co *= kw['3n']
                for k in range(len(j[0])):
                    if j[0][k] == '.':
                        if j[1] not in chlist:
                            chlist.append(j[1][k])
                            wt.append(co)
                        else:
                            wt[chlist.index(j[1][k])] += co
            elif j[0].count('x') == 2:
                co = kw['2w'] * coef[i]
                if 'xx' in j[0]:
                    co *= kw['2w']
                if 'n' in j[0]:
                    co *= kw['2n']
                for k in range(len(j[0])):
                    if j[0][k] == '.':
                        if j[1] not in chlist:
                            chlist.append(j[1][k])
                            wt.append(co)
                        else:
                            wt[chlist.index(j[1][k])] += co
            elif j[0].count('x') == 1:
                co = kw['1w'] * coef[i - curp]
                if 'n' in j[0]:
                    co *= kw['1n']
                for k in range(len(j[0])):
                    if j[0][k] == '.':
                        if j[1] not in chlist:
                            chlist.append(j[1][k])
                            wt.append(co)
                        else:
                            wt[chlist.index(j[1][k])] += co

    if not chlist:
        return rd.choice(game.avail)
    chlist = sorted(zip(wt, chlist), key=lambda x: x[0])
    return chlist[-1][1]


def TrAI(game):
    return AI(game, kw=trained)


list_AI = [AI, ImRdAI, RdAI, None, TrAI]
