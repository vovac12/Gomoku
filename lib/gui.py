import tkinter as t
import lib.env as env
import lib.AI as AI
from tkinter import messagebox as msgbox
from PIL import ImageTk


def comma(k=None):
    pass


class App:
    def __init__(self, master, texture):
        self.sets = {'size': 19, 'wc': 5, 'AI': 0, 'chs': 30, 'player': 1}
        self.i_bg = texture
        self.root = master
        self.root.geometry('800x600+150+150')
        self.root.configure(background='#f56915')
        self.root.title('Гомоку')
        self.frame = t.Frame(self.root, background='#159368')
        self.frame.pack()
        self.board = t.Canvas(self.frame)
        self._init_menu()
        self._init_board()
        self.wopt = None
        self._binds()

    def _init_menu(self):
        self.menu = []
        self.menu.append(t.Menu(self.root, background='#f7e7c7',
                                activebackground='#d7c7a7'))
        self.root.configure(menu=self.menu[0])
        self.menu[0].add_command(label='Новая игра', command=self.new_game)
        self.menu[0].add_command(label='Опции', command=self.options)
        self.menu[0].add_command(label='Выход', command=self.root.destroy)

    def _init_board(self, size=15, wc=5, player=1):
        size = self.sets['size']
        wc = self.sets['wc']
        chs = self.sets['chs']
        self.game = env.gomoku(size, wc)
        self.root.geometry('{}x{}'.format(chs * size, chs * size))
        self.root.minsize(chs * size, chs * size + 30)
        self.root.maxsize(chs * size, chs * size + 30)
        self.board.destroy()
        self.p_bg = {-1: 'white', 1: 'black'}
        self.t_bg = {-1: '#eeeeee', 1: '#888888'}
        self.board = t.Canvas(self.frame, height=chs * size, width=chs * size,
                              background='brown')
        for i in range(0, 1000, 40):
            for j in range(0, 1000, 40):
                self.board.create_image(i, j, image=self.i_bg, anchor='sw',
                                        tags=('img'))
        self.board.tag_lower('img')
        self.board.pack()
        for i in range(size):
            self.board.create_line(chs // 2 + i * chs, chs // 2,
                                   chs // 2 + i * chs,
                                   chs // 2 + chs * (size - 1), width=3)
            self.board.create_line(chs // 2, chs // 2 + i * chs,
                                   chs // 2 + chs * (size - 1),
                                   chs // 2 + i * chs, width=3)
        self.board.bind("<Motion>", func=self.pp)
        self.board.bind("<Button-1>", func=self.clicked)
        self.board.delete('win')

    def clicked(self, event=None):
        if self.game.gameover:
            return 0
        bg = self.p_bg[self.game.player]
        bot = AI.list_AI[self.sets['AI']]
        chs = self.sets['chs']
        x = event.x
        y = event.y
        xg = x - x % chs
        yg = y - y % chs
        if max(x // chs, y // chs) < self.game.size:
            tn = self.game.turn(x // chs, y // chs)
        else:
            return 1
        if not tn:
            return 0
        g = chs // 10
        self.board.create_oval(xg + g, yg + g, chs + xg - g, chs + yg - g,
                               fill=bg, tags=(bg, 'f'))
        if bot and not self.game.gameover:
            x, y = bot(self.game)
            bg = self.p_bg[self.game.player]
            tn = self.game.turn(x, y)
            self.board.create_oval(x * chs + g, y * chs + g,
                                   (1 + x) * chs - g, (1 + y) * chs - g,
                                   fill=bg, tags=(bg, 'f'))
        if self.game.gameover:
            self.winner(self.game.gameover)
            return 0

    def pp(self, event=None):
        if self.game.gameover:
            return 0
        chs = self.sets['chs']
        x = event.x
        y = event.y
        xg = x - x % chs
        yg = y - y % chs
        g = chs // 10
        self.board.delete('tmp')
        self.board.create_oval(xg + g, yg + g, chs + xg - g, chs + yg - g,
                               tags=('tmp'),
                               fill=self.t_bg[self.game.player],
                               outline='#eeeeee')
        self.board.tag_lower('tmp')
        self.board.tag_raise('tmp', 'img')

    def winner(self, player):
        pt = 1 if player == 1 else 2
        msg = msgbox.Message(self.root,
                             message='Игрок %d победил' % pt)
        msg.show()

    def msgtest(self):
        msg = msgbox.Message(self.root)
        msg.show()

    def new_game(self):
        if self.game.size != self.sets['size']:
            self._init_board()
        else:
            self.game = env.gomoku(size=self.sets['size'])
            self.board.delete('f')
            self.board.delete('win')
        if self.sets['player'] == 0:
            tn = self.sets['size'] // 2
            chs = self.sets['chs']
            xg = chs * tn
            g = chs // 10
            bg = self.p_bg[self.game.player]
            self.board.create_oval(xg + g, xg + g,
                                   chs + xg - g, chs + xg - g,
                                   fill=bg, tags=(bg, 'f'))
            self.game.turn(tn, tn)

    def options(self):

        def applysets(k=None):
            if not k:
                pass
            ss['AI'] = vAI.get()
            ss['size'] = vSZ.get()
            ss['player'] = vP.get()
            self.sets = ss
            self.new_game()

        def setai(f):
            ss['AI'] = f
        if self.wopt:
            self.wopt.destroy()
        self.wopt = t.Toplevel(self.root, background='#f7e7c7')
        self.wopt.title('Опции')
        ss = self.sets.copy()
        # self.wopt.geometry('800x600+100+100')
        rbtn = [[], [], []]
        vAI = t.IntVar(self.wopt, ss['AI'])
        vSZ = t.IntVar(self.wopt, ss['size'])
        vP = t.IntVar(self.wopt, ss['player'])

        rbtn[0].append(t.Radiobutton(self.wopt, variable=vAI,
                                  value=2, text='Случайный'))
        rbtn[0].append(t.Radiobutton(self.wopt, variable=vAI,
                                  value=1, text='Улучшенный Случайный',))
        rbtn[0].append(t.Radiobutton(self.wopt, variable=vAI,
                                  value=0, text='Стандартный ИИ'))
        rbtn[0].append(t.Radiobutton(self.wopt, variable=vAI,
                                  value=4, text='Тренированный ИИ'))
        rbtn[0].append(t.Radiobutton(self.wopt, variable=vAI,
                                  value=3, text='Против игрока'))

        rbtn[1].append(t.Radiobutton(self.wopt, variable=vSZ,
                                  value=13, text='13x13'))
        rbtn[1].append(t.Radiobutton(self.wopt, variable=vSZ,
                                  value=15, text='15x15'))
        rbtn[1].append(t.Radiobutton(self.wopt, variable=vSZ,
                                  value=17, text='17x17'))
        rbtn[1].append(t.Radiobutton(self.wopt, variable=vSZ,
                                  value=19, text='19x19'))

        rbtn[2].append(t.Radiobutton(self.wopt, variable=vP,
                                  value=1, text='Игрок'))
        rbtn[2].append(t.Radiobutton(self.wopt, variable=vP,
                                  value=0, text='ИИ'))

        appbtn = t.Button(self.wopt, text='Apply',
                          command=applysets)
        label1 = t.Label(self.wopt, text='Выбор ИИ')
        label2 = t.Label(self.wopt, text='Размер поля')
        label3 = t.Label(self.wopt, text='Первый ход')
        for i in (*rbtn[0], *rbtn[1], *rbtn[2], appbtn,
                  label1, label2, label3):
            i.configure(background='#f7e7c7', activebackground='#d7c7a7')
        label1.grid(row=0, column=0)
        rbtn[0][0].grid(row=1, column=0, sticky='w')
        rbtn[0][1].grid(row=2, column=0, sticky='w')
        rbtn[0][2].grid(row=3, column=0, sticky='w')
        rbtn[0][3].grid(row=4, column=0, sticky='w')
        rbtn[0][4].grid(row=5, column=0, sticky='w')
        label2.grid(row=0, column=2)
        rbtn[1][0].grid(row=1, column=2, sticky='w')
        rbtn[1][1].grid(row=2, column=2, sticky='w')
        rbtn[1][2].grid(row=3, column=2, sticky='w')
        rbtn[1][3].grid(row=4, column=2, sticky='w')
        label3.grid(row=0, column=3)
        rbtn[2][0].grid(row=1, column=3, sticky='w')
        rbtn[2][1].grid(row=2, column=3, sticky='w')
        appbtn.grid(row=6, column=4)

    def _binds(self):
        self.root.bind('<Escape>', lambda x=None: self.root.destroy())
        self.root.bind('<n>', lambda x=None: self.new_game())


if __name__ == '__main__':
    root = t.Tk()
    img = ImageTk.PhotoImage(file='../res/texture.jpg', size='40x40')
    app = App(root, img)
    root.mainloop()
