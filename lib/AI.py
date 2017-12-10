import lib.env as env
import random as rd

templates = [
    '.x.', '.x', '.xx.', '.xx',
    '.xxx.', '.xxx', '.xxxx',
    '.xxxx.', 'xxxxx']

def f_temp(diags, avail):
    res = []
    for i in diags:
        pass

def RdAI(game):
    return rd.choice(game.avail)

def ImRdAI(game):
    res = set()
    res.add(rd.choice(game.avail))
    for i in range(game.size):
        for j in range(game.size):
            if game.board[i][j] == game.player:
                res.add((i+1, j))
                res.add((i+1, j+1))
                res.add((i+1, j-1))
                res.add((i, j+1))
                res.add((i-1, j))
                res.add((i-1, j+1))
                res.add((i-1, j-1))
                res.add((i, j-1))
    res = res.intersection(set(game.avail))
    return rd.choice(tuple(res))

def DefAI(game):
    diags = game.diags(-game.player, 1)
    if not diags:
        return rd.choice(game.avail)
    diags = sorted(diags, key=len, reverse=True)
    print(len(diags[0]))
    for i in diags:
        for j in i:
            if j[-1] == 'e':
                return j[0:-1]
