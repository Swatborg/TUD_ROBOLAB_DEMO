#!/usr/bin/env python3

import unittest
import io
import unittest.mock
from stack_machine import *


class TestStackMachine(unittest.TestCase):
    
    def setUp(self):
        self.sm = StackMachine()
        
    def test_instance(self):
        """ Essential: Test class instantiation """
        #self.fail('implement me!')
        self.assertIsInstance(self.sm, StackMachine)

    """ Please add your test cases here! """
    
    def test_func(self):
        code_word = ((0, 0, 1, 0, 1, 0), (0, 1, 0, 0, 0, 1), (0, 1, 0, 0, 0, 1), (0, 1, 0, 1, 1, 0), 
                     (0, 1, 1, 1, 1, 1), (0, 0, 0, 1, 0, 0), (0, 1, 1, 0, 1, 1), (0, 0, 0, 1, 0, 0),
                     (0, 1, 1, 0, 0, 1), (0, 0, 0, 1, 1, 0), (0, 1, 1, 0, 0, 0), (1, 0, 0, 0, 1, 0),
                     (1, 1, 0, 1, 1, 0), (1, 0, 1, 0, 0, 0), (1, 1, 0, 1, 0, 1), (0, 0, 0, 1, 0, 1), (1, 0, 0, 0, 0, 1), (0, 1, 0, 0, 0, 0))
        
        self.sm.stack.clear()
        for cw in (code_word):
            result = self.sm.do(cw)
            if cw == (0, 1, 0, 0, 0, 0):
                self.assertEqual(result.value, 0)
            else:
                self.assertEqual(result.value, 1) 
        self.assertEqual(self.sm.top(), None)
                     
    # STP            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_stp(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 0, 0, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '0')
        
    # DUP            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_dup(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 0, 0, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '1')
        
    # DEL            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_del(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 0, 1, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '1')
        
    # SWP            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_swp(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 0, 1, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '1')
        
    # ADD            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_add(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 1, 0, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '6')
        
    # SUB            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_sub(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 1, 0, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '2')
        
    # MUL            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_mul(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 1, 1, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '8')
        
    # DIV            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_div(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 0, 1, 1, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '2')
        
    # EXP            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_exp(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 0, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '16')
    
    # MOD            
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_mod(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 0, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '0')
        
    # SHL           
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_shl(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 1, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '16')
        
    # SHR           
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_shr(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 1, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '1')
        
    # HEX           
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_hex(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((1, 0, 0, 1, 1, 0), (0, 0, 0, 1, 0, 1), (0, 1, 1, 1, 0, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '92')
        
    # FAC           
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_fac(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((1, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 1, 0, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '2')
        
    # NOT           
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_not(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 0, 1, 0), (0, 1, 1, 1, 1, 0))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '253')
        
    # XOR              
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_xor(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 1, 1, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '6')
        
    # DIVISION BY ZERO              
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_div_zero(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 0), (0, 0, 0, 0, 0, 0), (0, 1, 0, 1, 1, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '-1')
        
    # DIFFERENT OPERATION TYPE           
    @unittest.mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_operand(self, mock_stdout):
        self.sm.stack.clear()
        code_word = ((1, 0, 0, 1, 1, 1), (0, 1, 0, 1, 0, 1))
        for cw in code_word:
            self.sm.do(cw)
        self.assertEqual(mock_stdout.getvalue()[:-1], '-1')


if __name__ == '__main__':
    unittest.main()
