from app.util.check import *
import unittest

class TestUtilChecks(unittest.TestCase):

    def test_type_check(self):
        self.assertTrue(type_check(1, [float, int, str]))
        self.assertTrue(type_check(1.0, [float, int, str]))
        self.assertTrue(type_check('1', [float, int, str]))
        self.assertTrue(type_check([1, 2, 3], [list]))
        self.assertTrue(type_check(True, [bool]))
        self.assertTrue(type_check(False, [bool]))
        self.assertFalse(type_check([1, 2, 3], [float, int, str]))
        self.assertFalse(type_check(1.0, [int, str]))
        self.assertRaises(TypeError, type_check, 1, int)

    def test_range_check(self):
        self.assertTrue(range_check(1, 0, 2))
        self.assertTrue(range_check('hello', 'he', 'hello_world'))
        self.assertTrue(range_check(60.0, 0.0, 100.0))
        self.assertTrue(range_check([1, 2, 3], [1, 2], [2, 3]))
        self.assertFalse(range_check('123', [1, 2], [2, 3]))
        self.assertFalse(range_check(1, '0', 2))
        self.assertFalse(range_check(1, 0, '2'))
        self.assertFalse(range_check('1', 0, 2))
        self.assertFalse(range_check(0, 50, 100))
        self.assertFalse(range_check(150.0, 0.0, 100.0))
        self.assertFalse(range_check('2016', '2017', '2018'))
        self.assertFalse(range_check(bool, True, False))