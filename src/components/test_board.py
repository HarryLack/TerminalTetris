import unittest
from unittest.mock import MagicMock

from components.board import Board
from components.piece import Orientation, Piece, Tetronimo
from keys import Key


class TestBoard(unittest.TestCase):
    def test_board_add(self):
        board = Board(5, 5)
        piece = Piece(Tetronimo.I, (1, 1))
        board.add_piece(piece=piece)
        self.assertEqual(board.active_piece, piece)

    def test_board_move_left(self):
        board = Board(5, 5)
        piece = Piece(Tetronimo.I, (2, 2))
        piece.move = MagicMock()
        board.add_piece(piece=piece)

        board.action(97)

        piece.move.assert_called_with(-1, 0)

        board = Board(5, 5)
        piece = Piece(Tetronimo.I, (0, 0))
        piece.move = MagicMock()
        board.add_piece(piece=piece)

        piece.move.assert_not_called()

    def test_board_move_right(self):
        board = Board(10, 10)
        piece = Piece(Tetronimo.I, (1, 1))
        piece.move = MagicMock()
        board.add_piece(piece=piece)

        board.action(100)

        piece.move.assert_called_with(1, 0)

        board = Board(5, 5)
        piece = Piece(Tetronimo.I, (4, 4))
        piece.move = MagicMock()
        board.add_piece(piece=piece)

        piece.move.assert_not_called()


class TestBoardPieceI(unittest.TestCase):
    def test_right_wall_right_orientation_right_rotate(self):
        print("\n")
        board = Board(8, 8)
        piece = Piece(Tetronimo.I, (4, 1), Orientation.RIGHT)
        board.add_piece(piece)

        board.action(Key.e.value)

        self.assertEqual(piece.rotation, Orientation.DOWN)
        self.assertEqual(piece.centre, ())
