import tkinter
from PIL import Image, ImageTk
import bitstring
from textwrap import wrap

class Board:
    def __init__(self, side=0):
        self.side = side # 0 for white, 1 for black
        self.square_size = 60
        self.make_pieces()
        self.castling = 'KQkq'
        self.white_to_move = True
        self.en_passant = '-'
        self.half_move = 0
        self.full_move = 0
        self.make_bitboards()

    def make_bitboards(self): # Setup bitboards
        
        self.wpawn = bitstring.BitArray('0x000000000000FF00')
        self.bpawn = bitstring.BitArray('0x00FF000000000000')

        self.wrook = bitstring.BitArray('0x0000000000000081')
        self.brook = bitstring.BitArray('0x8100000000000000')
        
        self.wknight = bitstring.BitArray('0x0000000000000042')
        self.bknight = bitstring.BitArray('0x4200000000000000')

        self.wbishop = bitstring.BitArray('0x0000000000000024')
        self.bbishop = bitstring.BitArray('0x2400000000000000')

        self.wqueen = bitstring.BitArray('0x0000000000000010')
        self.bqueen = bitstring.BitArray('0x1000000000000000')

        self.wking = bitstring.BitArray('0x000000000000008')
        self.bking = bitstring.BitArray('0x800000000000000')

        self.all_pieces = bitstring.BitArray('0xFFFF00000000FFFF')

        self.white = [self.wpawn, self.wrook, self.wknight, self.wbishop, self.wqueen, self.wking]
        self.black = [self.bpawn, self.brook, self.bknight, self.bbishop, self.bqueen, self.bking]

    def print_bitboard(self,b): # print a particular bitboard for debugging purposes
        b_str = b.bin
        b_str = '0' * (64 - len(b_str)) + b_str
        print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(b_str, 8)]))

    def make_pieces(self): #
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


    def render(self,canvas):

        for i in range(8):
            for j in range(8):
                fill = '#696969' if (i+j) % 2 == 1 else "#ffffff"

                canvas.create_rectangle(j*self.square_size, i*self.square_size, 
                                        (j+1)*self.square_size, (i+1)*self.square_size,
                                        fill=fill, outline='#000000')

        self.render_pieces(canvas)
        canvas.pack()

    def render_pieces(self,canvas):

        def render_piece(bin,image):
            locs = bin
            locs = '0' * (64 - len(locs)) + locs
            for i in range(8):
                for j in range(8):
                    if locs[i*8 + j] == '1':
                        canvas.create_image(j*self.square_size + self.square_size//2, i*self.square_size+self.square_size//2, image=image)


        # Pawns first
        render_piece(self.wpawn.bin, self.wpawn_image) 
        render_piece(self.bpawn.bin, self.bpawn_image)

        render_piece(self.wrook.bin, self.wrook_image)
        render_piece(self.brook.bin, self.brook_image)

        render_piece(self.wknight.bin, self.wknight_image)
        render_piece(self.bknight.bin, self.bknight_image)

        render_piece(self.wbishop.bin, self.wbishop_image)
        render_piece(self.bbishop.bin, self.bbishop_image)

        render_piece(self.wqueen.bin, self.wqueen_image)
        render_piece(self.bqueen.bin, self.bqueen_image)

        render_piece(self.wking.bin, self.wking_image)
        render_piece(self.bking.bin, self.bking_image)

    def make_move(self,move):
        if len(move) != 4:
            raise IllegalMove(move)
        
        start = move[:2]
        end = move[2:]

        start_index = self.convert_spot_to_index(start)
        end_index = self.convert_spot_to_index(end)

        if self.white_to_move:
            for piece in self.white:
                if piece[start_index]:
                    piece[start_index] = 0
                    piece[end_index] = 1
            
            self.white_to_move = False

    def convert_spot_to_index(self,loc):
        r = int(loc[1])
        f = ord(loc[0]) - 97
        return (8-r) * 8 + f

        



class Error(Exception):
    pass
class IllegalMove(Error):
    pass


def main():
    tk = tkinter.Tk()
    can = tkinter.Canvas(tk, width=800, height=800)
    board = Board()
    board.render(can)
    can.pack()
    board.make_move('e2e4')
    board.render(can)

    tk.mainloop()


b = bitstring.BitArray('0b00001101')
print([b[i] for i in range(len(b))])
a = bitstring.BitArray('0b0100')
print(b.bin)
main()