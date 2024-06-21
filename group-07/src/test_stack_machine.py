#!/usr/bin/env python3


import unittest
import io
import unittest.mock
from stack_machine import *


class TestStackMachine(unittest.TestCase):

    def setUp(self):
        self.sm = StackMachine()

    def testing_instance(self):
        """ Essential: Test class instantiation """
        self.assertIsInstance(self.sm, StackMachine)

    def test_stack_machine(self):
        self.sm.stack.clear()
        code_word = [(0, 0, 1, 0, 1, 0), (0, 1, 0, 0, 0, 1), (0, 1, 0, 0, 0, 1), (0, 1, 0, 1, 1, 0), (0, 1, 1, 1, 1, 1),(0, 0, 0, 1, 0, 0),
                     (0, 1, 1, 0, 1, 1), (0, 0, 0, 1, 0, 0), (0, 1, 1, 0, 0, 1), (0, 0, 0, 1, 1, 0), (0, 1, 1, 0, 0, 0),(1, 0, 0, 0, 1, 0),
                     (1, 1, 0, 1, 1, 0), (1, 0, 1, 0, 0, 0), (1, 1, 0, 1, 0, 1), (0, 0, 0, 1, 0, 1), (1, 0, 0, 0, 0, 1),(0, 1, 0, 0, 0, 0)]
        out0 = SMState.RUNNING
        in1 = []
        for i in range(len(code_word)-1):
            in1.append(self.sm.do(code_word[i]))
        for i in range(len(code_word)-1):
            self.assertEqual(in1[i], out0)
        out1 = None
        #self.sm.stack.clear()
        out2 = self.sm.top()
        self.assertEqual(out1, out2)
        #out3 = self.sm.do((0, 1, 0, 0, 0, 0))
        #out4 = SMState.STOPPED
        #self.assertEqual(out4, out3)

    def test_dup_(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 0, 0, 1), (0, 1, 0, 0, 0, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 1, 0, 0, 1)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_del(self):
        self.sm.stack.clear()
        #code_word = ((0, 0, 1, 0, 1, 0), (0, 1, 0, 0, 1, 0))
        code_word = ((0, 0, 1, 0, 1, 0), (0, 0, 1, 0, 0, 0), (0, 1, 0, 0, 1, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0,0,0,0,1,0,1,0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)

    def testing_swap(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 1, 0, 0, 1, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 1, 0, 0, 1)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_ADD(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 1, 1), (0, 0, 0, 0, 0, 1), (0, 1, 0, 1, 0, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 1, 0, 0, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_sub(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 0, 0, 0), (0, 0, 0, 0, 1, 1), (0, 1, 0, 1, 0, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 0, 1, 0, 1)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_MUL(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 0, 1), (0, 1, 0, 1, 1, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 1, 0, 0, 1)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_DIV(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 1, 1), (0, 1, 0, 1, 1, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 0, 0, 1, 1)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    #def test_DIV1(self):
    #    self.sm.stack.clear()
    #    code_word = ((0, 0, 1, 0, 0, 1), (0, 0, 0, 0, 0, 0), (0, 1, 0, 1, 1, 1))  # division by zero(exception)
    #    for i in range(len(code_word)):
    #        j = self.sm.do(code_word[i])
    #    eout = None
    #    out0 = self.sm.top()
    #    self.assertEqual(eout, out0)
    #    self.assertEqual(j, SMState.ERROR)
    #    self.assertEqual(self.sm.overflow, False)

    def test_EXP(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 0, 1, 1), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 0, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 1, 0, 0, 1)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_MOD(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 0, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 0, 0, 0, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_SHL(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 1, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 1, 0, 0, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_SHR(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 1, 1), (0, 0, 1, 0, 1, 0), (0, 1, 1, 0, 1, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 0, 0, 0, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_HEX(self):
        self.sm.stack.clear()
        code_word = ((1, 0, 1, 0, 0, 0), (0, 0, 0, 1, 1, 1), (0, 1, 1, 1, 0, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 1, 1, 1, 1, 1, 1, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_FAC(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 0, 1, 1), (0, 1, 1, 1, 0, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 0, 1, 1, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_NOT(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 1, 1, 1, 1), (0, 1, 1, 1, 1, 0))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (1, 1, 1, 1, 0, 0, 0, 0)
        out0 = self.sm.top()
        self.assertEqual(eout, out0)
        self.assertEqual(self.sm.overflow, False)

    def test_XOR(self):
        self.sm.stack.clear()
        code_word = ((0, 0, 0, 1, 0, 1), (0, 0, 0, 0, 0, 1), (0, 1, 1, 1, 1, 1))
        for i in range(len(code_word)):
            self.sm.do(code_word[i])
        eout = (0, 0, 0, 0, 0, 1, 0, 0)
        out = self.sm.top()
        self.assertEqual(eout, out)
        self.assertEqual(self.sm.overflow, False)

    #def test_exception(self):  # exception case-- operands are not sufficent
    #    self.sm.stack.clear()
    #    code_word = ((0, 0, 0, 1, 1, 1))
    #    self.sm.do(code_word)
    #    eout = SMState.ERROR
    #    out0 = self.sm.do((0, 1, 0, 1, 0, 1))
    #    self.assertEqual(eout, out0)

    #def test_exception2(self):  # exception case for different type
    #    self.sm.stack.clear()
    #    code_word = ((1, 0, 0, 1, 1, 1))
    #    self.sm.do(code_word)
    #    eout = SMState.ERROR
    #    out0 = self.sm.do((0, 1, 0, 1, 0, 1))
    #    self.assertEqual(eout, out0)


if __name__ == '__main__':
    unittest.main()