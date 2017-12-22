#!/usr/bin/python

import lib.gui
import tkinter
from PIL import ImageTk
import os
import sys


os.chdir(sys.path[0])


def main():
    root = tkinter.Tk()
    img = ImageTk.PhotoImage(file='./res/texture.png', size='40x40')
    app = lib.gui.App(root, img)
    if app:
        pass
    root.mainloop()
    exit(0)


if __name__ == '__main__':
    main()
