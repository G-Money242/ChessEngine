import os
import unittest
import main


class TestLegality(unittest.TestCase):
    def white_pawn_attack(self):
        board = main.Board('4k3/8/8/8/8/2P5/PP1P1PPP/4K3 w - - 0 1')
        res = board.get_pawn_attacks('w')
        self.assertEqual(res.int,1357840384) # white attack squares

        board = main.Board('4k3/3pp3/1pPPPP1p/P1P3P1/p1p5/1P1P4/8/4K3 w - - 0 1')
        res = board.get_pawn_attacks('b')
        self.assertEqual(res.int, board.wpawn.int)


if __name__ == '__main__':
    unittest.main()