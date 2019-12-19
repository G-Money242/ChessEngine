import tkinter
from PIL import Image, ImageTk

class Board:
    def __init__(self, side=0):
        self.side = side # 0 for white, 1 for black

    def render(self,canvas):
        width = canvas.winfo_width()
        height = canvas.winfo_height()

        square_size = min(width//8,height//8)

        for i in range(8):
            for j in range(8):
                fill = '#000000' if i+j % 2 == 0 else "#ffffff"

                canvas.create_rectangle(j*square_size, i*square_size, 
                                        (j+1)*square_size, (i+1)*square_size,
                                        fill=fill)
        canvas.pack()

tk = tkinter.Tk()
can = tkinter.Canvas(tk, width=500, height=500)
board = Board()
board.render(can)

tk.mainloop()