import unittest

from components.board import Board
from components.piece import STATES, Orientation
from game import Piece, Tetronimo


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


class TestPieceI(unittest.TestCase):
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
        

