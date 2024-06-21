#!/usr/bin/env python3

import io
from hamming_code import *
from stack_machine import *

def test_add():
    ham = HammingCode()
    sm = StackMachine()
    barcode = ((0,0,0,0,1,1,0,0,1,0,0),(0,0,0,0,0,1,0,1,0,1,0),(0,1,0,1,0,0,1,1,1,1,1),(0,1,0,0,0,0,0,0,1,1,0))
    for i in range(len(barcode)):
        ham_res = ham.decode(barcode[i])
        sm.do(ham_res)
        
def test_del():
    ham = HammingCode()
    sm = StackMachine()
    barcode = ((0,0,0,0,0,1,0,1,0,1,0),(0,0,0,0,1,0,0,1,1,1,1),(0,1,0,0,1,0,0,1,0,0,0),(0,1,0,0,0,0,0,0,1,1,0))
    for i in range(len(barcode)-1):
        ham_res = ham.decode(barcode[i])
        sm.do(ham_res)
        
def test_fac():
    ham = HammingCode()
    sm = StackMachine()
    barcode = ((0,0,0,1,0,1,1,0,0,1,1),(0,1,1,1,0,1,0,1,0,0,0),(0,1,0,0,0,0,0,0,1,1,0))
    for i in range(len(barcode)-1):
        ham_res = ham.decode(barcode[i])
        sm.do(ham_res)
        
if __name__ == '__main__':
    test_add()
    print()
    test_del()
    print()
    test_fac()
