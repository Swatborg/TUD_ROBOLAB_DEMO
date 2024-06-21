#!/usr/bin/env python3

import unittest
from hamming_code import *


class TestHammingCode(unittest.TestCase):
    def test_instance(self):
        """ Essential: Test class instantiation """
        expected_class = HammingCode()
        self.assertIsInstance(expected_class, HammingCode)
        # self.fail('implement me!')

    def test_decode_valid(self):
        """ Essential: Test method decode() with VALID input """
        expected_class = HammingCode()
        expected_output = ((1, 0, 1, 1, 0, 1), HCResult.VALID)
        test = HammingCode.decode(expected_class, (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1))
        self.assertEqual(expected_output, test)
        # self.fail('implement me!')

    def test_decode_corrected(self):
        """ Essential: Test method decode() with CORRECTED input """
        expected_class = HammingCode()
        expected_output = ((0, 1, 1, 0, 1, 1), HCResult.CORRECTED)
        test = HammingCode.decode(expected_class, (0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0))
        self.assertEqual(expected_output, test)
        
        expected_output = ((0, 0, 0, 0, 0, 0), HCResult.CORRECTED)
        test = HammingCode.decode(expected_class, (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1))
        self.assertEqual(expected_output, test)
        
        expected_output = ((1, 1, 1, 1, 1, 0), HCResult.CORRECTED)
        test = HammingCode.decode(expected_class, (1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1))
        self.assertEqual(expected_output, test)
        
        expected_output = ((0, 0, 0, 0, 0, 0), HCResult.CORRECTED)
        test = HammingCode.decode(expected_class, (0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0))
        self.assertEqual(expected_output, test)
        # self.fail('implement me!')

    def test_decode_uncorrectable(self):
        """ Essential: Test method decode() with UNCORRECTABLE input """
        expected_class = HammingCode()
        expected_output = (None, HCResult.UNCORRECTABLE)
        test = HammingCode.decode(expected_class, (0, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1))
        self.assertEqual(expected_output, test)
        # self.fail('implement me!')

    def test_encode(self):
        """ Essential: Test method encode() """
        expected_class = HammingCode()
        encode_lst = [(0, 1, 1, 0, 1, 1),
                      (0, 0, 0, 0, 0, 0),
                      (1, 0, 1, 1, 0, 1),
                      (1, 1, 1, 1, 1, 0)]
        
        expected_output = [(0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0),
                        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
                        (1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1),
                        (1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1)]
        
        for i in range(len(encode_lst)):
            self.assertEqual(HammingCode.encode(expected_class,encode_lst[i]), expected_output[i])
        # self.fail('implement me!')


if __name__ == '__main__':
    unittest.main()
