import numpy as np
import time
from lib.my_debug_utils import timeof

class gomoku():
    def __init__(self, size=15, wincond=5, player=1):
        self.board = np.zeros((size, size), 'int')
        self.player = player
        self.size = size
        self.wincond = wincond
        self.coords = [[],[]]
        self.gameover = 0
        self.turn_n = 0
        self.avail = [(i, j) for i in range(size) for j in range(size)]
    def turn(self, x, y):
        if self.board[x][y]:
            return 0
        if self.gameover:
            return 0
        self.turn_n += 1
        self.avail.pop(self.avail.index((x,y)))
        self.board.itemset((x,y), self.player)
        if self.player == -1:
            self.coords[1].append((x,y))
        else:
            self.coords[0].append((x,y))
        diags = self.diags()
        try:
            if diags and max(map(len, diags)) >= 5:
                self.gameover = self.player
                return self.player
        except:
            print(diags)
        self.player = -self.player
        return 2
    @timeof
    def diags(self, p = None, tpl=False):
        rs = []
        def some(sel, ls, t1, t2):
            res = []
            for i in range(10):
                tmp = (sel[0]+t1*i, sel[1]+t2*i)
                if tmp in ls:
                    res.append(tmp)
                else:
                    if tmp in self.avail and tpl:
                        res.append((*tmp, 'e'))
                    break
            for i in range(1, 10):
                tmp = (sel[0]-t1*i, sel[1]-t2*i)
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
            if not k in rs:
                rs.append(k)
            k = sorted(some(wr[i], wr, 0, 1))
            if not k in rs:
                rs.append(k)
            k = sorted(some(wr[i], wr, 1, 0))
            if not k in rs:
                rs.append(k)
            k = sorted(some(wr[i], wr, -1, 1))
            if not k in rs:
                rs.append(k)
        return rs

if __name__ == '__main__':
    g = gomoku()
    print('Gomoku environment')
