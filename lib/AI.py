import random as rd

templates = [
    'xxxxx',
    '.xxxx.',
    '.xxxx',
    'x.xxx.',
    'xx.xx.',
    'xxx.x.',
    '.xxx.',
    '.xxx',
    '.xx.x',
    '.x.xx',
    '.xx.']


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


def AI(game, dc=0.99, ac=1.01):
    chlist = []
    wt = []
    coef = (dc, ac)
    curp = 0 if game.player == 1 else 1
    for i in range(2):
        for j in game.diags_p[i - curp]:
            if j[0].count('x') == 4:
                print(j[0])
                if '.' not in j[0].strip('.'):
                    print(j[1][j[0].index('.')])
                    return j[1][j[0].index('.')]
                else:
                    print(j[1][j[0][1:].index('.') + 1])
                    return j[1][j[0][1:].index('.') + 1]
            elif j[0][0] == 'n' and j[0][-1] == 'n':
                continue
            elif j[0].count('x') == 3:
                co = 300 * coef[i - curp]
                if 'xxx' in j[0]:
                    co *= 4
                if 'n' in j[0]:
                    co *= 0.7
                for k in range(len(j[0])):
                    if j[0][k] == '.':
                        if j[1] not in chlist:
                            chlist.append(j[1][k])
                            wt.append(co)
                        else:
                            wt[chlist.index(j[1][k])] += co
            elif j[0].count('x') == 2:
                co = 50 * coef[i - curp]
                if 'xx' in j[0]:
                    co *= 2
                if 'n' in j[0]:
                    co *= 0.7
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


list_AI = [RdAI, ImRdAI, AI]
