import unittest
from unittest.mock import MagicMock

from components.board import Board
from components.piece import Piece, Tetronimo


class TestBoard(unittest.TestCase):
    def test_board_size(self):
        expect = "#####\n#   #\n#   #\n#   #\n#####\n"
        board = Board(5, 5)
        self.assertEqual(board.render(), expect)

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
        board = Board(5, 5)
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
