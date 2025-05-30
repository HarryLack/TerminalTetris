import unittest

from game import STATES, Board, Orientation, Piece, Tetronimo
from src.render import create_world


class TestMain(unittest.TestCase):
    def test_create_world(self):
        expect = "####\n#  #\n#  #\n####\n"
        world = create_world(4, 4)
        self.assertEqual(world, expect)


class TestBoard(unittest.TestCase):
    def test_board_size(self):
        expect = "#####\n#   #\n#   #\n#   #\n#####\n"
        board = Board(5, 5)
        self.assertEqual(board.render(), expect)

    def test_board_add(self):
        board = Board(5, 5)
        piece = Piece(Tetronimo.I, (1, 1))
        board.add_piece(piece=piece)
        self.assertEqual(len(board.pieces), 1)
        self.assertEqual(board.pieces[0], piece)


class TestPiece(unittest.TestCase):
    def test_rotate(self):
        piece = Piece(Tetronimo.I, (0, 0))

        self.assertEqual(piece.rotation, Orientation.NONE)
        piece.rotate()
        self.assertEqual(piece.rotation, Orientation.RIGHT)
        piece.rotate()
        self.assertEqual(piece.rotation, Orientation.DOWN)
        piece.rotate()
        self.assertEqual(piece.rotation, Orientation.LEFT)
        piece.rotate()
        self.assertEqual(piece.rotation, Orientation.NONE)

        self.assertEqual(piece.rotation, Orientation.NONE)
        piece.rotate(False)
        self.assertEqual(piece.rotation, Orientation.LEFT)
        piece.rotate(False)
        self.assertEqual(piece.rotation, Orientation.DOWN)
        piece.rotate(False)
        self.assertEqual(piece.rotation, Orientation.RIGHT)
        piece.rotate(False)
        self.assertEqual(piece.rotation, Orientation.NONE)

    def test_move(self):
        piece = Piece(Tetronimo.I, (0, 0))

        self.assertEqual(piece.position, (0, 0))

        piece.move(0, 1)

        self.assertEqual(piece.position, (0, 1))

        piece.move(1, 0)

        self.assertEqual(piece.position, (1, 1))

    def test_I(self):
        piece = Piece(Tetronimo.I, (0, 0))
        self.assertEqual(piece.state, STATES[Tetronimo.I][Orientation.NONE])
