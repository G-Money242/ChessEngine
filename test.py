import os
import unittest
import board


class TestLegality(unittest.TestCase):
    def white_pawn_attack(self):
        board = board.Board('4k3/8/8/8/8/2P5/PP1P1PPP/4K3 w - - 0 1')
        res = board.get_pawn_attacks('w')
        self.assertEqual(res.int,1357840384) # white attack squares

        board = main.Board('4k3/3pp3/1pPPPP1p/P1P3P1/p1p5/1P1P4/8/4K3 w - - 0 1')
        res = board.get_pawn_attacks('b')
        self.assertEqual(res.int, board.wpawn.int)


if __name__ == '__main__':
    unittest.main()

rays = {}
rays['N'] = {}
start = BitArray('0x0101010101010100')
for i in range(64):
    rays['N'][i] = start.hex
    start = start << 1

rays['S'] = {}
start = BitArray('0x0080808080808080')
for i in range(63,-1,-1):
    rays['S'][i] = start.hex
    start = start >> 1

rays['W'] = {}
start = BitArray('0x0000000000000001')
for i in range(8):
    rank = mask_rank[i+1]
    b = rank & ~start
    for j in range(8):
        index = 8*i + j
        rays['W'][index] = b.hex
        start = start << 1
        b = b & ~start

rays['E'] = {}
start = BitArray('0x0000000000000000')
start = '0b0000000000000000000000000000000000000000000000000000000000000000'
for i in range(8):
    rank = mask_rank[i+1]
    for j in range(8):
        index = 8*i + j 
        rays['E'][index] = (rank & BitArray(start)).hex
        s = list(start)
        neg_index = -index-1
        s[neg_index] = '1'
        start = "".join(s)

rays['NW'] = {}
b = BitArray('0x8040201008040200')
start = BitArray('0x0000000000000000')
l = list('abcdefgh')[::-1]
for i in range(64):
    j = i % 8
    clear = ~start
    for k in range(j):
        clear = clear & clear_file[l[k]]
    rays['NW'][i] = (b & clear).hex
    b = b << 1

rays['SE'] = {}
b = BitArray('0x0040201008040201')
l = list('abcdefgh')
for i in range(63,-1,-1):
    j = 7 - (i % 8)
    clear = ~start
    for k in range(j):
        clear &= clear_file[l[k]]

    rays['SE'][i] = (b & clear).hex
    b = b >> 1

rays['SW'] = {}
for i in range(64):
    l = ['0' for _ in range(64)]
    y,x = i//8, i%8
    while y != 8 and x != -1:
        l[8*y + x] = '1'
        y += 1
        x -= 1
    l[i] = '0'
    b = BitArray('0b' + "".join(l))
    rays['SW'][63-i] = b.hex

rays['NE'] = {}
for i in range(64):
    l = ['0' for _ in range(64)]
    y,x = i//8, i%8
    while y != -1 and x != 8:
        l[8*y + x] = '1'
        y -= 1
        x += 1
    l[i] = '0'
    b = BitArray('0b' + "".join(l))
    rays['NE'][63-i] = b.hex

with open('resources/bitboards/rays.json','w') as f:
    json.dump(rays,f)
