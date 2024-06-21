#!/usr/bin/env python3

import io
import unittest.mock
from hamming_code import *
from stack_machine import *
import unittest


class TestRobot(unittest.TestCase):
    #@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    #def test_example(self, mock_stdout):
    #    """
    #        Example implementation of whole workflow:
    #            - Decode valid/correctable codes and
    #            - Execute the opcodes on the stack machine
    #            - Checking the final result afterwards
    #    """
    #    self.fail('implement me!')
    
    def setUp(self):
        self.ham = HammingCode()
        self.sm = StackMachine()

    def testing_instance(self):
        """ Essential: Test class instantiation """
        self.assertIsInstance(self.sm, StackMachine)
        self.assertIsInstance(self.ham, HammingCode)
    
    def test_add(self):
        self.sm.stack.clear()
        barcode = ((0,0,0,0,1,1,0,0,1,0,0),(0,0,0,0,0,1,0,1,0,1,0),(0,1,0,1,0,0,1,1,1,1,1),(0,1,0,0,0,0,0,0,1,1,0))
        dec_res = ((0,0,0,0,1,1),(0,0,0,0,0,1),(0,1,0,1,0,0))
        for i in range(len(barcode)-1):
            decoded_word = self.ham.decode(barcode[i])
            self.assertEqual(decoded_word, dec_res[i])
            self.sm.do(decoded_word)
            print()
        expected_output = (0,0,0,0,0,1,0,0)
        output = self.sm.top()
        self.assertEqual(expected_output, output)
        print("################################")
        
    def test_del(self):
        self.sm.stack.clear()
        barcode = ((0,0,0,0,0,1,0,1,0,1,0),(0,0,0,0,1,0,0,1,1,1,1),(0,1,0,0,1,0,0,1,0,0,0),(0,1,0,0,0,0,0,0,1,1,0))
        dec_res = ((0,0,0,0,0,1),(0,0,0,0,1,0),(0,1,0,0,1,0))
        for i in range(len(barcode)-1):
            decoded_word = self.ham.decode(barcode[i])
            self.assertEqual(decoded_word, dec_res[i])
            self.sm.do(decoded_word)
            print()
        expected_output = (0,0,0,0,0,0,0,1)
        output = self.sm.top()
        self.assertEqual(expected_output, output)
        print("################################")
        
    def test_fac(self):
        self.sm.stack.clear()
        barcode = ((0,0,0,1,0,1,1,0,0,1,1),(0,1,1,1,0,1,0,1,0,0,0),(0,1,0,0,0,0,0,0,1,1,0))
        dec_res = ((0,0,0,1,0,1),(0,1,1,1,0,1),(0,1,0,0,1,0))
        for i in range(len(barcode)-1):
            decoded_word = self.ham.decode(barcode[i])
            self.assertEqual(decoded_word, dec_res[i])
            self.sm.do(decoded_word)
            print()
        expected_output = (0,1,1,1,1,0,0,0)
        output = self.sm.top()
        self.assertEqual(expected_output, output)
        print("################################")
        
    def test_xor(self):
        self.sm.stack.clear()
        #barcode = ((0,0,0,0,0,1,0,1,0,1,0), # SUB
        #           (0,0,0,0,1,0,0,1,1,1,1),
        #           (0,1,0,1,0,1,1,0,1,0,0),
        #           (0,1,0,0,0,0,0,0,1,1,0))
        #barcode = ( (0,0,0,0,0,1,0,1,0,1,0), # DEL
        #            (0,0,0,0,1,0,0,1,1,1,1),
        #            (0,1,0,0,1,0,0,1,0,0,0),
        #            (0,1,0,0,0,0,0,0,1,1,0))
        barcode = ((0,0,0,0,1,1,0,0,1,0,0),
                   (0,0,1,1,1,1,0,0,0,0,1),
                   (0,0,1,1,1,1,0,0,0,0,1),
                   (0,1,0,1,0,0,1,1,1,1,1),
                   (0,1,0,1,0,0,1,1,1,1,1),
                   (0,0,0,0,1,0,0,1,1,1,1),
                   (0,0,0,1,1,1,1,1,1,0,1),
                   (0,1,1,0,0,0,1,1,0,1,0),
                   (0,0,0,0,1,1,0,0,1,0,0),
                   (0,1,0,1,0,1,1,0,1,0,0),
                   (0,1,1,1,1,1,0,0,1,1,0),
                   (0,1,0,0,0,0,0,0,1,1,0))

        #barcode = ((0,0,0,1,0,1,1,0,0,1,1),(0,1,1,1,0,1,0,1,0,0,0),(0,1,0,0,0,0,0,0,1,1,0))
        dec_res = ((0,0,0,1,0,1),(0,1,1,1,0,1),(0,1,0,0,1,0))
        for i in range(len(barcode)-1):
            decoded_word = self.ham.decode(barcode[i])
            #elf.assertEqual(decoded_word, dec_res[i])
            self.sm.do(decoded_word)
            print()
        #expected_output = (0,0,0,0,0,0,0,1)
        expected_output = (0,1,0,1,1,1,0,0)
        #expected_output = (0,1,1,1,1,0,0,0)
        output = self.sm.top()
        self.assertEqual(expected_output, output)
        print("################################")
    
    #@unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    #def test_stp(self, mock_stdout):
    #    self.sm.stack.clear()
    #    barcode = (0,1,0,0,0,0,0,0,1,1,0)
    #    decoded_word = self.ham.decode(barcode)
    #    self.sm.do(decoded_word)
    #    self.assertEqual(mock_stdout.getvalue(), "Stop Function. The program is being terminated!\n")
         
if __name__ == '__main__':
    unittest.main()
