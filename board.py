from bitstring import BitArray
from textwrap import wrap
import json

with open('resources/bitboards/clear_file.json') as f:
    d = json.load(f)
    clear_file = {f:BitArray('0x'+h) for f,h in d.items()}

with open('resources/bitboards/clear_rank.json') as f:
    d = json.load(f)
    clear_rank = {int(r):BitArray('0x'+h) for r,h in d.items()}

with open('resources/bitboards/knight_moves.json') as f:
    d = json.load(f)
    knight_moves = {int(k):BitArray('0x'+h) for k,h in d.items()}

with open('resources/bitboards/mask_file.json') as f:
    d = json.load(f)
    mask_file = {f:BitArray('0x'+h) for f,h in d.items()}

with open('resources/bitboards/mask_rank.json') as f:
    d = json.load(f)
    mask_rank = {int(r):BitArray('0x'+h) for r,h in d.items()}

with open('resources/bitboards/piece.json') as f:
    d = json.load(f)
    piece = {int(f):BitArray('0x'+h) for f,h in d.items()}

with open('resources/bitboards/king_moves.json') as f:
    d = json.load(f)
    king_moves = {int(f):BitArray('0x'+h) for f,h in d.items()}

with open('resources/bitboards/rays.json') as f:
    d = json.load(f)
    rays = {}
    for key,sub_d in d.items():
        rays[key] = {int(i): BitArray('0x'+j) for i,j in sub_d.items()}

class Board:
    def __init__(self, fen=None):
        self.fen = fen if fen else 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
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
        self.all_pieces = self.allwhite | self.allblack

    def print_bitboard(self,b): # print a particular bitboard for debugging purposes
        print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(b.bin, 8)]))

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

    def get_bishop_moves(self, square, blockers):
        attacks = BitArray('0x0000000000000000')

        attacks |= rays['NW'][square]
        if rays['NW'][square] & blockers:
            blockerIndex = bitscan_forward(rays['NW'][square] & blockers)
            attacks &= ~rays['NW'][blockerIndex]
        
        attacks |= rays['NE'][square]
        if rays['NE'][square] & blockers:
            blockerIndex = bitscan_forward(rays['NE'][square] & blockers)
            attacks &= ~rays['NE'][blockerIndex]
        
        attacks |= rays['SE'][square]
        if rays['SE'][square] & blockers:
            blockerIndex = bitscan_reverse(rays['SE'][square] & blockers)
            attacks &= ~rays['SE'][blockerIndex]
        
        attacks |= rays['SW'][square]
        if rays['SW'][square] & blockers:
            blockerIndex = bitscan_reverse(rays['SW'][square] & blockers)
            attacks &= ~rays['SW'][blockerIndex]
        
        return attacks

    def get_rook_moves(self, square, blockers):
        attacks = BitArray('0x0000000000000000')

        attacks |= rays['N'][square]
        if rays['N'][square] & blockers:
            blockerIndex = bitscan_forward(rays['N'][square] & blockers)
            attacks &= ~rays['N'][blockerIndex]

        attacks |= rays['W'][square]
        if rays['W'][square] & blockers:
            blockerIndex = bitscan_forward(rays['W'][square] & blockers)
            attacks &= ~rays['W'][blockerIndex]
        
        attacks |= rays['E'][square]
        if rays['E'][square] & blockers:
            blockerIndex = bitscan_reverse(rays['E'][square] & blockers)
            attacks &= ~rays['E'][blockerIndex]

        attacks |= rays['S'][square]
        if rays['S'][square] & blockers:
            blockerIndex = bitscan_reverse(rays['S'][square] & blockers)
            attacks &= ~rays['S'][blockerIndex]
        
        return attacks

    def get_queen_moves(self, square, blockers):
        return self.get_bishop_moves(square,blockers)  | self.get_rook_moves(square,blockers)

    def get_knight_moves(self, square, blockers):
        return knight_moves[square] & ~blockers

    def get_king_moves(self, color):
        if color == 'w':
            king_loc = bitscan_forward(self.wking)
            bishop_locs = bitscan_all(self.bbishop)
            rook_locs = bitscan_all(self.brook)
            queen_locs = bitscan_all(self.bqueen)
            knight_locs = bitscan_all(self.bknight)
            pawn_attacks = self.get_pawn_attacks('b')
            all_except_king = self.all_pieces & ~self.wking
            opp_king_loc = bitscan_forward(self.bking)

        attacks = BitArray('0x0000000000000000')
        
        for bishop_loc in bishop_locs:
            attacks |= self.get_bishop_moves(bishop_loc,all_except_king)
        for rook_loc in rook_locs:
            attacks |= self.get_rook_moves(rook_loc,all_except_king)
        for queen_loc in queen_locs:
            attacks |= self.get_queen_moves(queen_loc,all_except_king)
        for knight_loc in knight_locs:
            attacks |= self.get_knight_moves(knight,all_except_king)
        
        attacks |= king_moves[opp_king_loc] & ~all_except_king
        attacks |= pawn_attacks
        print_bitboard(attacks)

        return king_moves[king_loc] & ~attacks


    def king_evasions(self, color):
        if color == 'w':
            king_loc = self.bitscan_forward(self.wking)
            opp_bishops = self.bbishop.copy()
            opp_knights = self.bknight.copy()
            opp_rooks = self.brook.copy()
            opp_queens = self.bqueen.copy()
        else:
            king_loc = self.bitscan_forward(self.bking)
            opp_bishops = self.wbishop.copy()
            opp_knights = self.wknight.copy()
            opp_rooks = self.wrook.copy()
            opp_queens = self.wqueen.copy()
        blockers = self.all_pieces.copy()

        attackers = BitArray('0x0000000000000000')
        attackers |= knight_moves[king_loc] & opp_knights
        attackers |= self.get_bishop_moves(king_loc, blockers) & opp_bishops
        attackers |= self.get_rook_moves(king_loc, blockers) & opp_rooks
        attackers |= self.get_queen_moves(king_loc, blockers) & opp_queens





def bitscan_forward(bs): # start at h1 and scan toward a8
    return 63 - bs.rfind('0b1')[0]

def bitscan_reverse(bs): # start at a8 and scan toward h1
    return 63 - bs.find('0b1')[0]

def bitscan_all(bs):
    return [63 - x for x in bs.findall('0b1')]

def print_bitboard(b): # print a particular bitboard for debugging purposes
    print('\n'.join([' '.join(wrap(line, 1)) for line in wrap(b.bin.replace('0','.'), 8)]))

def compute_king(king_loc):
    king_clip_h = king_loc & clear_file['h']
    king_clip_a = king_loc & clear_file['a']

    spot_1 = king_clip_a << 9
    spot_2 = king_loc << 8
    spot_3 = king_clip_h << 7
    spot_4 = king_clip_h >> 1

    spot_5 = king_clip_h >> 9
    spot_6 = king_loc >> 8
    spot_7 = king_clip_a >> 7
    spot_8 = king_clip_a << 1

    return spot_1 | spot_2 | spot_3 | spot_4 | spot_5 | spot_6 | spot_7 | spot_8

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


class Error(Exception):
    pass
class IllegalMove(Error):
    pass



if __name__ == '__main__':
    k = BitArray('0x0000010000000000')
    fen = '4k3/8/8/8/2b1r3/8/4K3/8 w - - 0 1'
    b = Board(fen)
    print()
    print_bitboard(b.all_pieces)
    print()
    a = b.get_king_moves('w')
    print_bitboard(a)
    print(a.int)


    # print_bitboard()
    # k = rays['NE'][2]
    
    # print_bitboard(k)
    # print([63 - x for x in k.findall('0b1')])