import tkinter as t
import time
import lib.env as env
import lib.AI as AI

def comma(k=None):
    pass

class App:
    def __init__(self, master):
        self.root = master
        self.root.geometry('800x600+150+150')
        self.frame = t.Frame(self.root, background='blue')
        self.frame.pack()
        self.board = t.Canvas(self.frame)
        self._init_menu()
        self._init_board()
        self.AI = AI.DefAI
        
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

        self.menu[3].add_command(label='Licence', command=comma)
        self.menu[3].add_command(label='Instruction', command=comma)
        self.menu[3].add_command(label='FAQ', command=comma)

    def _init_board(self, size=15, wc=5, player=1):
        self.game = env.gomoku(size, wc, player)
        self.root.geometry('{}x{}'.format(50*size+100, 50*size+100))
        self.board.destroy()
        self.p_bg = {-1: 'white', 1: 'black'}
        self.t_bg = {-1: '#eeeeee', 1: '#888888'}
        self.board = t.Canvas(self.frame, height=50*size, width=50*size)
        self.board.pack()
        for i in range(size):
            self.board.create_line(25+i*50, 25, 25+i*50, 25+50*(size-1))
            self.board.create_line(25, 25+i*50, 25+50*(size-1), 25+i*50)
        self.board.bind("<Motion>", func=self.pp)
        self.board.bind("<Button-1>", func=self.clicked)

    def clicked(self, event=None):
        if self.game.gameover:
            return 0
        print('Click')
        bg = self.p_bg[self.game.player]
        x = event.x
        y = event.y
        xg = x - x%50
        yg = y - y%50
        tn = self.game.turn(x//50, y//50)
        if tn:
            self.board.create_oval(5+xg, 5+yg, 45+xg, 45+yg, fill=bg, tags=(bg, 'f'))
            if tn != 2:
                self.winner(tn)
                return 0
            if self.AI:
                x, y = self.AI(self.game)
                bg = self.p_bg[self.game.player]
                tn = self.game.turn(x, y)
                self.board.create_oval(5+x*50, 5+y*50, 45+x*50, 45+y*50, fill=bg, tags=(bg, 'f'))
                if tn != 2:
                    self.winner(tn)
                    return 0

    def pp(self, event = None):
        if self.game.gameover:
            return 0
        x = event.x
        y = event.y
        xg = x - x%50
        yg = y - y%50
        self.board.delete('tmp')
        self.board.create_oval(5+xg, 5+yg, 45+xg, 45+yg, tags=('tmp'),
                                fill=self.t_bg[self.game.player],
                                outline='#eeeeee')
        self.board.tag_lower('tmp')
        
    def winner(self, player):
        pt = 1 if player == 1 else 2
        print("Победил игрок {}!".format(pt))            

    def new_game(self):
        self._init_board()

if __name__ == '__main__':
    root = t.Tk()
    app = App(root)
    root.mainloop()
