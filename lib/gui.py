import tkinter as t
import lib.env as env
import lib.AI as AI
from tkinter import messagebox as msgbox


def comma(k=None):
    pass


class App:
    def __init__(self, master):
        self.sets = {'size': 15, 'wc': 5, 'AI': None, 'chs': 35, 'player': 1}
        self.root = master
        self.root.geometry('800x600+150+150')
        self.frame = t.Frame(self.root, background='blue')
        self.frame.pack()
        self.board = t.Canvas(self.frame)
        self._init_menu()
        self._init_board()
        self.AI = AI.ImRdAI
        self.wopt = None

    def _init_menu(self):
        self.menu = []
        self.menu.append(t.Menu(self.root))
        self.root.configure(menu=self.menu[0])
        self.menu.append(t.Menu(self.root))
        self.menu.append(t.Menu(self.root))
        self.menu.append(t.Menu(self.root))
        self.menu[0].add_cascade(label='Game', menu=self.menu[1])
        self.menu[0].add_cascade(label='Settings', menu=self.menu[2])
        self.menu[0].add_cascade(label='About', menu=self.menu[3])
        self.menu[0].add_command(label='Quit', command=self.root.destroy)

        self.menu[1].add_command(label='New game', command=self.new_game)

        self.menu[2].add_command(label='Options', command=self.options)

        self.menu[3].add_command(label='Licence', command=self.msgtest)
        self.menu[3].add_command(label='Instruction', command=comma)
        self.menu[3].add_command(label='FAQ', command=comma)

    def _init_board(self, size=15, wc=5, player=1):
        size = self.sets['size']
        wc = self.sets['wc']
        player = self.sets['player']
        chs = self.sets['chs']
        self.game = env.gomoku(size, wc, player)
        self.root.geometry('{}x{}'.format(chs * size + 100, chs * size + 100))
        self.board.destroy()
        self.p_bg = {-1: 'white', 1: 'black'}
        self.t_bg = {-1: '#eeeeee', 1: '#888888'}
        self.board = t.Canvas(self.frame, height=chs * size, width=chs * size,
                              background='brown')
        self.board.pack()
        for i in range(size):
            self.board.create_line(chs // 2 + i * chs, chs // 2,
                                   chs // 2 + i * chs,
                                   chs // 2 + chs * (size - 1))
            self.board.create_line(chs // 2, chs // 2 + i * chs,
                                   chs // 2 + chs * (size - 1),
                                   chs // 2 + i * chs)
        self.board.bind("<Motion>", func=self.pp)
        self.board.bind("<Button-1>", func=self.clicked)

    def clicked(self, event=None):
        if self.game.gameover:
            return 0
        bg = self.p_bg[self.game.player]
        AI = self.sets['AI']
        chs = self.sets['chs']
        x = event.x
        y = event.y
        xg = x - x % chs
        yg = y - y % chs
        if max(x // chs, y // chs) < self.game.size:
            tn = self.game.turn(x // chs, y // chs)
        else:
            return 1
        if tn:
            self.board.create_oval(xg, yg, chs + xg, chs + yg,
                                   fill=bg, tags=(bg, 'f'))
            if tn != 2:
                self.winner(tn)
                return 0
            if AI:
                x, y = AI(self.game)
                bg = self.p_bg[self.game.player]
                tn = self.game.turn(x, y)
                self.board.create_oval(x * chs, y * chs,
                                       (1 + x) * chs, (1 + y) * chs,
                                       fill=bg, tags=(bg, 'f'))
                if tn != 2:
                    self.winner(tn)
                    return 0

    def pp(self, event=None):
        if self.game.gameover:
            return 0
        chs = self.sets['chs']
        x = event.x
        y = event.y
        xg = x - x % chs
        yg = y - y % chs
        self.board.delete('tmp')
        self.board.create_oval(xg, yg, chs + xg, chs + yg, tags=('tmp'),
                               fill=self.t_bg[self.game.player],
                               outline='#eeeeee')
        self.board.tag_lower('tmp')

    def winner(self, player):
        pt = 1 if player == 1 else 2
        print("Победил игрок {}!".format(pt))

    def msgtest(self):
        msg = msgbox.Message(self.root)
        msg.show()

    def new_game(self):
        self._init_board()

    def options(self):
        if self.wopt:
            self.wopt.destroy()

        def applysets(k=None):
            if not k:
                pass
            print(type(sets['AI']))
            sets['AI'] = sets['AI'].get()
            self.sets = sets
            print(self.sets, sets)
        self.wopt = t.Tk()
        self.wopt.geometry('300x300+150+150')
        sets = self.sets.copy()
        rbtn = []
        rbtn.append(t.Radiobutton(self.wopt, variable=sets['AI'],
                                  value=AI.RdAI, text='Random'))
        rbtn.append(t.Radiobutton(self.wopt, variable=sets['AI'],
                                  value=AI.ImRdAI, text='Improved Random'))
        rbtn.append(t.Radiobutton(self.wopt, variable=sets['AI'],
                                  value=AI.RdAI, text='SSRandom'))
        rbtn.append(t.Radiobutton(self.wopt, variable=sets['AI'],
                                  value=AI.ImRdAI, text='RRRandom'))
        appbtn = t.Button(self.wopt, text='Apply',
                          command=applysets)
        rbtn[0].pack()
        rbtn[1].pack()
        rbtn[2].pack()
        rbtn[3].pack()
        appbtn.pack()


if __name__ == '__main__':
    root = t.Tk()
    app = App(root)
    root.mainloop()
