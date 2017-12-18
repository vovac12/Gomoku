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


def f_temp(board, temp):
    pass


def diags(self, p=None, tpl=False):
        rs = []

        def some(sel, ls, t1, t2):
            res = []
            for i in range(10):
                tmp = (sel[0] + t1 * i, sel[1] + t2 * i)
                if tmp in ls:
                    res.append(tmp)
                else:
                    if tmp in self.avail and tpl:
                        res.append((*tmp, 'e'))
                    break
            for i in range(1, 10):
                tmp = (sel[0] - t1 * i, sel[1] - t2 * i)
                if tmp in ls:
                    res.append(tmp)
                else:
                    if tmp in self.avail and tpl:
                        res.append((*tmp, 'e'))
                    break
            return res

        if p == None:
            p = self.player
        if p == 1:
            wr = self.coords[0].copy()
        else:
            wr = self.coords[1].copy()
        for i in range(len(wr)):
            k = sorted(some(wr[i], wr, 1, 1))
            if k not in rs:
                rs.append(k)
            k = sorted(some(wr[i], wr, 0, 1))
            if k not in rs:
                rs.append(k)
            k = sorted(some(wr[i], wr, 1, 0))
            if k not in rs:
                rs.append(k)
            k = sorted(some(wr[i], wr, -1, 1))
            if k not in rs:
                rs.append(k)
        return rs


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


list_AI = [RdAI, ImRdAI]
