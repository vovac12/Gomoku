import numpy as np
from lib.my_debug_utils import timeof


class gomoku():
    def __init__(self, size=15, wincond=5, player=1):
        self.board = np.zeros((size, size), 'int')
        self.player = player
        self.size = size
        self.wincond = wincond
        self.coords = [[], []]
        self.diags_p = [[], []]
        self.gameover = 0
        self.turn_n = 0
        self.avail = [(i, j) for i in range(size) for j in range(size)]
    def turn(self, x, y):
        if self.board[x][y]:
            return 0
        if self.gameover:
            return 0
        self.turn_n += 1
        self.avail.pop(self.avail.index((x, y)))
        self.board.itemset((x, y), self.player)
        if self.player == -1:
            self.coords[1].append((x, y))
        else:
            self.coords[0].append((x, y))
        self.diags_p = [self.diags(p=1), self.diags(p=-1)]
        if self.gameover:
            return self.gameover
        self.player = -self.player
        return 2
    @timeof
    def diags(self, p=None):
        rs = []

        def some(sel, ls, t1, t2):
            res = ['', [sel]]
            if sel in self.avail:
                res[0] = '.'
            else:
                res[0] = 'x'
            for i in range(1, 10):
                tmp = (sel[0] + t1 * i, sel[1] + t2 * i)
                if tmp in ls:
                    res[1].append(tmp)
                    res[0] += 'x'
                else:
                    if tmp in self.avail:
                        res[0] += '.'
                    else:
                        res[0] += 'n'
                    res[1].append(tmp)
                    break
            for i in range(1, 10):
                tmp = (sel[0] - t1 * i, sel[1] - t2 * i)
                if tmp in ls:
                    res[0] = 'x' + res[0]
                    res[1].insert(0, tmp)
                else:
                    if tmp in self.avail:
                        res[0] = '.' + res[0]
                    else:
                        res[0] = 'n' + res[0]
                    res[1].insert(0, tmp)
                    break
            return tuple(res)

        if p == None:
            p = self.player
        if p == 1:
            wr = self.coords[0].copy()
        else:
            wr = self.coords[1].copy()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == -p:
                    continue
                k = some((i, j), wr, 1, 1)
                if k not in rs and 'x' in k[0] and '..' not in k[0]\
                   and '.' in k[0]:
                    rs.append(k)
                if 'xxxxx' in k[0]:
                    self.gameover = p
                k = some((i, j), wr, 0, 1)
                if k not in rs and 'x' in k[0] and '..' not in k[0]\
                   and '.' in k[0]:
                    rs.append(k)
                if 'xxxxx' in k[0]:
                    self.gameover = p
                k = some((i, j), wr, 1, 0)
                if k not in rs and 'x' in k[0] and '..' not in k[0]\
                   and '.' in k[0]:
                    rs.append(k)
                if 'xxxxx' in k[0]:
                    self.gameover = p
                k = some((i, j), wr, -1, 1)
                if k not in rs and 'x' in k[0] and '..' not in k[0]\
                   and '.' in k[0]:
                    rs.append(k)
                if 'xxxxx' in k[0]:
                    self.gameover = p
        return rs


if __name__ == '__main__':
    g = gomoku()
    print('Gomoku environment')
