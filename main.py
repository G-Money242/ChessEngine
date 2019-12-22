import tkinter
from PIL import Image, ImageTk
from bitstring import BitArray
from textwrap import wrap

def print_bitboard(b): # print a particular bitboard for debugging purposes
    print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(b.bin, 8)]))

def compute_knight(knight_loc):
    """
    . 2 . 3 .
    1 . . . 4
    . . N . .
    8 . . . 5
    . 7 . 6 .

    """
    spot_1_clip = clear_file['a'] & clear_file['b'] & clear_rank[8]
    spot_2_clip = clear_file['a'] & clear_rank[8] & clear_rank[7]
    spot_3_clip = clear_file['h'] & clear_rank[8] & clear_rank[7]
    spot_4_clip = clear_file['h'] & clear_file['g'] & clear_rank[8]

    spot_5_clip = clear_file['h'] & clear_file['g'] & clear_rank[1]
    spot_6_clip = clear_file['h'] & clear_rank[1] & clear_rank[2]
    spot_7_clip = clear_file['a'] & clear_rank[1] & clear_rank[2]
    spot_8_clip = clear_file['a'] & clear_file['b'] & clear_rank[1]

    
    spot_1 = (knight_loc & spot_1_clip) << 10
    spot_2 = (knight_loc & spot_2_clip) << 17
    spot_3 = (knight_loc & spot_3_clip) << 15
    spot_4 = (knight_loc & spot_4_clip) << 6

    spot_5 = (knight_loc & spot_5_clip) >> 10
    spot_6 = (knight_loc & spot_6_clip) >> 17
    spot_7 = (knight_loc & spot_7_clip) >> 15
    spot_8 = (knight_loc & spot_8_clip) >> 6

    return spot_1 | spot_2 | spot_3 | spot_4 | spot_5 | spot_6 | spot_7 | spot_8


mask_rank = {1:BitArray('0x00000000000000FF'),
            2:BitArray('0x000000000000FF00'),
            3:BitArray('0x0000000000FF0000'),
            4:BitArray('0x00000000FF000000'),
            5:BitArray('0x000000FF00000000'),
            6:BitArray('0x0000FF0000000000'),
            7:BitArray('0x00FF000000000000'),
            8:BitArray('0xFF00000000000000')}
clear_rank = {rank:~bitboard for rank,bitboard in mask_rank.items()}

mask_file={'a':BitArray('0x8080808080808080'),
        'b':BitArray('0x4040404040404040'),
        'c':BitArray('0x2020202020202020'),
        'd':BitArray('0x1010101010101010'),
        'e':BitArray('0x0808080808080808'),
        'f':BitArray('0x0404040404040404'),
        'g':BitArray('0x0202020202020202'),
        'h':BitArray('0x0101010101010101')}

clear_file = {f:~bitboard for f,bitboard in mask_file.items()}
    
p = BitArray('0x0000000000000001')
piece = {0:p}
for i in range(8):
    for j in range(8):
        if (8*i + j) not in piece: 
            p = p << 1
            piece[8*i+j] = p

knight_moves = {i:compute_knight(knight) for i,knight in piece.items()}

class Board:
    def __init__(self, fen=None,tk=None):
        if tk == None:
            tk = tkinter.Tk()
        self.fen = fen if fen else 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.square_size = 60
        self.make_pieces()
        self.castling = 'KQkq'
        self.white_to_move = True
        self.en_passant = '-'
        self.half_move = 0
        self.full_move = 0
        self.make_bitboards()

    def make_bitboards(self): # Setup bitboards
        self.wpawn = BitArray('0x0000000000000000')
        self.bpawn = BitArray('0x0000000000000000')

        self.wrook = BitArray('0x0000000000000000')
        self.brook = BitArray('0x0000000000000000')
        
        self.wknight = BitArray('0x0000000000000000')
        self.bknight = BitArray('0x0000000000000000')

        self.wbishop = BitArray('0x0000000000000000')
        self.bbishop = BitArray('0x0000000000000000')

        self.wqueen = BitArray('0x0000000000000000')
        self.bqueen = BitArray('0x0000000000000000')

        self.wking = BitArray('0x0000000000000000')
        self.bking = BitArray('0x0000000000000000')

        setup = self.fen.split(' ')[0]
        ranks = setup.split('/')
        
        for i,rank in enumerate(ranks):
            j = 0
            for char in rank:
                if char.isdigit():
                    j += int(char)
                else:
                    if char == 'r':
                        self.brook[8*i+j] = 1
                    elif char == 'n':
                        self.bknight[8*i+j] = 1
                    elif char == 'b':
                        self.bbishop[8*i+j] = 1
                    elif char == 'q':
                        self.bqueen[8*i+j] = 1
                    elif char == 'k':
                        self.bking[8*i+j] = 1
                    elif char == 'p':
                        self.bpawn[8*i+j] = 1
                    elif char == 'R':
                        self.wrook[8*i+j] = 1
                    elif char == 'N':
                        self.wknight[8*i+j] = 1
                    elif char == 'B':
                        self.wbishop[8*i+j] = 1
                    elif char == 'Q':
                        self.wqueen[8*i+j] = 1
                    elif char == 'K':
                        self.wking[8*i+j] = 1
                    elif char == 'P':
                        self.wpawn[8*i+j] = 1
                    j += 1

        self.allwhite = self.wpawn | self.wrook | self.wknight | self.wbishop | self.wqueen | self.wking
        self.allblack = self.bpawn | self.brook | self.bknight | self.bbishop | self.bqueen | self.bking
        self.all_pieces = self.allwhite & self.allblack

    def print_bitboard(self,b): # print a particular bitboard for debugging purposes
        print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(b.bin, 8)]))

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


    def render(self,canvas):

        for i in range(8):
            for j in range(8):
                fill = '#AF8A66' if (i+j) % 2 == 1 else "#EDDAB7"

                canvas.create_rectangle(j*self.square_size, i*self.square_size, 
                                        (j+1)*self.square_size, (i+1)*self.square_size,
                                        fill=fill, outline="")

        self.render_pieces(canvas)
        canvas.pack()

    def render_bitboard(self, canvas, bitboard):
        self.print_bitboard(bitboard)
        for index,char in enumerate(bitboard.bin):
            if char == '1':
                true_index = 63-index
                print(index,true_index)
                i,j = 7-true_index//8, 7-(true_index % 8)
                print(i,j)
                canvas.create_rectangle(j*self.square_size, i*self.square_size, (j+1)*self.square_size, (i+1)*self.square_size, outline="#f11",fill="#f11", width=1)

        canvas.pack()


    def render_pieces(self,canvas):

        def render_piece(locs,image):
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
            
            # self.white_to_move = False

    def convert_spot_to_index(self,loc):
        r = int(loc[1])
        f = ord(loc[0]) - 97
        return (8-r) * 8 + f

    def get_pawn_attacks(self, color):
        pawns = self.wpawn if color == 'w' else self.bpawn
        if color == 'w':
            west_attack = pawns.copy()
            west_attack.rol(9)
            west_attack = west_attack & (clear_file['h'])
            
            east_attack = pawns.copy()
            east_attack.rol(7)
            east_attack = east_attack & (clear_file['a'])

            return east_attack | west_attack
        else:
            west_attack = pawns.copy()
            west_attack.ror(7)
            west_attack = west_attack & (clear_file['h'])
            
            east_attack = pawns.copy()
            east_attack.ror(9)
            east_attack = east_attack & (clear_file['a'])

            return east_attack | west_attack
        


class Error(Exception):
    pass
class IllegalMove(Error):
    pass



def main():
    tk = tkinter.Tk()
    can = tkinter.Canvas(tk, width=800, height=800)
    board = Board('4k3/8/8/8/4R3/8/8/4K3 w - - 0 1',tk)
    board.render(can)
    can.pack()
    board.render_bitboard(can, board.wrook)


    # while True:
    #     move = input("make move:")
    #     board.make_move(move)
    #     board.render(can)

    tk.mainloop()


b = BitArray('0b1110')
print([b[i] for i in range(len(b))])
a = BitArray('0b1100')
c = a & b
print('here',(b << 2).bin)
c = BitArray(64)

if __name__ == '__main__':
    pass
    # main()
