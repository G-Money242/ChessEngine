import tkinter
from PIL import Image, ImageTk
from bitstring import BitArray
from textwrap import wrap
import json
import board

class GUI(tkinter.Canvas):
    def __init__(self, master, fen=None):
        tkinter.Canvas.__init__(self, master, width=800, height=800)
        self.master = master
        self.board = board.Board(fen)
        self.square_size = 60
        self.make_pieces()

    def make_pieces(self): 
        self.bpawn_image = tkinter.PhotoImage(file='resources/images/black_pawn.png')
        self.wpawn_image = tkinter.PhotoImage(file='resources/images/white_pawn.png')

        self.brook_image = tkinter.PhotoImage(file='resources/images/black_rook.png')
        self.wrook_image = tkinter.PhotoImage(file='resources/images/white_rook.png')

        self.bknight_image = tkinter.PhotoImage(file='resources/images/black_knight.png')
        self.wknight_image = tkinter.PhotoImage(file='resources/images/white_knight.png')

        self.bbishop_image = tkinter.PhotoImage(file='resources/images/black_bishop.png')
        self.wbishop_image = tkinter.PhotoImage(file='resources/images/white_bishop.png')

        self.bqueen_image = tkinter.PhotoImage(file='resources/images/black_queen.png')
        self.wqueen_image = tkinter.PhotoImage(file='resources/images/white_queen.png')
        
        self.bking_image = tkinter.PhotoImage(file='resources/images/black_king.png')
        self.wking_image = tkinter.PhotoImage(file='resources/images/white_king.png')

    def render(self):
        for i in range(8):
            for j in range(8):
                fill = '#AF8A66' if (i+j) % 2 == 1 else "#EDDAB7"

                self.create_rectangle(j*self.square_size, i*self.square_size, 
                                        (j+1)*self.square_size, (i+1)*self.square_size,
                                        fill=fill, outline="")

        self.render_pieces()

        self.pack()
    
    def render_bitboard(self, bitboard):
        for index,char in enumerate(bitboard.bin):
            if char == '1':
                true_index = 63-index
                i,j = 7-true_index//8, 7-(true_index % 8)
                self.create_rectangle(j*self.square_size, i*self.square_size, (j+1)*self.square_size, (i+1)*self.square_size, outline="#f11",fill="#f11", width=1)

    def render_pieces(self):

        def render_piece(locs,image):
            for i in range(8):
                for j in range(8):
                    if locs[i*8 + j] == '1':
                        self.create_image(j*self.square_size + self.square_size//2, i*self.square_size+self.square_size//2, image=image)


        # Pawns first
        render_piece(self.board.wpawn.bin, self.wpawn_image) 
        render_piece(self.board.bpawn.bin, self.bpawn_image)

        render_piece(self.board.wrook.bin, self.wrook_image)
        render_piece(self.board.brook.bin, self.brook_image)

        render_piece(self.board.wknight.bin, self.wknight_image)
        render_piece(self.board.bknight.bin, self.bknight_image)

        render_piece(self.board.wbishop.bin, self.wbishop_image)
        render_piece(self.board.bbishop.bin, self.bbishop_image)

        render_piece(self.board.wqueen.bin, self.wqueen_image)
        render_piece(self.board.bqueen.bin, self.bqueen_image)
        
        render_piece(self.board.wking.bin, self.wking_image)
        render_piece(self.board.bking.bin, self.bking_image)
        

if __name__ == '__main__':
    root = tkinter.Tk()
    game = GUI(root,'4k3/3pp3/1pPPPP1p/P1P5/p1p5/1P1P4/8/4K3 w - - 0 1')
    game.render()

    root.mainloop()