#!/usr/bin/env python
import lib.gui
import tkinter


def main():
    root = tkinter.Tk()
    app = lib.gui.App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
