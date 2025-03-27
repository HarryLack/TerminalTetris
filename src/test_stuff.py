import unittest

from src.render import create_world


class TestMain(unittest.TestCase):
    def test_create_world(self):
        expect = "####\n#  #\n#  #\n####\n"
        world = create_world(4, 4)
        self.assertEqual(world, expect)
