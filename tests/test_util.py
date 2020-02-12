import unittest
from scorechecker.util.check import *
from scorechecker.util.cryptography import *
from keyring import get_password

message = b'hello world'

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


class TestUtilCrypto(unittest.TestCase):

    def test_encrypt_and_decrypt(self):
        encrypt(message)
        first_key = get_password('ScoreChecker Crypto', 'scc_key')
        first_nonce = get_password('ScoreChecker Crypto', 'scc_nonce')
        first_tag = get_password('ScoreChecker Crypto', 'scc_tag')
        decrypted = decrypt()
        self.assertEqual(decrypted, message)
        second_key = get_password('ScoreChecker Crypto', 'scc_key')
        second_nonce = get_password('ScoreChecker Crypto', 'scc_nonce')
        second_tag = get_password('ScoreChecker Crypto', 'scc_tag')
        self.assertNotEqual(first_key, second_key)
        self.assertNotEqual(first_nonce, second_nonce)
        self.assertNotEqual(first_tag, second_tag)

    def test_reset(self):
        reset()
        self.assertEqual(get_password('ScoreChecker Crypto', 'scc_key'), '')
        self.assertEqual(get_password('ScoreChecker Crypto', 'scc_nonce'), '')
        self.assertEqual(get_password('ScoreChecker Crypto', 'scc_tag'), '')