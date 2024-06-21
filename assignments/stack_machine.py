#!/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class SMState(IntEnum):
    """
    Return codes for the stack machine
    """
    RUNNING = 1
    STOPPED = 0
    ERROR = -1


class StackMachine:
    """
    Implements the 8-bit stack machine according to the specification
    """

    def __init__(self) -> None:
        """
        Initializes the class StackMachine with all values necessary.
        """
        self.overflow = False
        self.stack = []
        
        """ Create dictionary for instructions """
        
        ins_bin = self.bin_seq(4)
        
        ins_lst = ('STP', 'DUP', 'DEL', 'SWP',
                   'ADD', 'SUB', 'MUL', 'DIV',
                   'EXP', 'MOD', 'SHL', 'SHR',
                   'HEX', 'FAC', 'NOT', 'XOR')

        self.ins_dict= dict(zip(ins_bin, ins_lst))
        
        """ Create dictionary for operands """

        operand_bin = self.bin_seq(5)
        
        mis_char_start = ('NOP', 'SPEAK', 'SPACE','NOP')
        mis_char_end = ('NOP', 'NOP')
        alpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        alpha_char_lst = [i for i in alpha]
        operand_tple = mis_char_start + tuple(alpha_char_lst) + mis_char_end  

        self.operand_dict= dict(zip(operand_bin, operand_tple))

    def do(self, code_word: Tuple[int, ...]) -> SMState:
        """
        Processes the entered code word by either executing the instruction or pushing the operand on the stack.

        Args:
            code_word (tuple): Command for the stack machine to execute
        Returns:
            SMState: Current state of the stack machine
        """
        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #pass
        code_word_lst = list(code_word)
        # Operand
        if (code_word_lst[0] == 0 and code_word_lst[1] == 0 ):
            outptut = (8 * code_word_lst[2] + 4 * code_word_lst[3] + 2 * code_word_lst[4] + 1 * code_word_lst[5])
            self.stack.append(outptut)
            return SMState.RUNNING
        
        # Instruction
        elif (code_word_lst[0] == 0 and code_word_lst[1] == 1 ):
            instruction_lst = code_word_lst.copy()
            instruction_tple = tuple(instruction_lst[2:])
            if (instruction_tple in self.ins_dict.keys()):
                return self.execute(self.ins_dict[instruction_tple])
            
        # Character
        elif (code_word_lst[0] == 1):
            operand_lst = code_word_lst.copy() 
            operand_tple = tuple(operand_lst[1:])
            if (operand_tple in self.operand_dict.keys()):
                if (self.operand_dict[operand_tple] == 'NOP'):
                    return SMState.RUNNING
                elif (self.operand_dict[operand_tple] == 'SPEAK'):
                    return self.execute('SPEAK')
                elif (self.operand_dict[operand_tple] == 'SPACE'):
                    self.stack.append(' ')
                    return SMState.RUNNING
                else:
                    self.stack.append(self.operand_dict[operand_tple])
                    return SMState.RUNNING

    def top(self) -> Union[None, str, Tuple[int, int, int, int, int, int, int, int]]:
        """
        Returns the top element of the stack.

        Returns:
            union: Can be tuple, str or None
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #pass
        if (len(self.stack) <= 0) :
            return None
        else:
            last_operand = self.stack.pop()
            if type(last_operand) == int:
                bin_str = bin(last_operand)[2:].zfill(8)
                output=tuple(map(int, bin_str))
            else:
                output = last_operand
            return output
        
    """ Function to create binary sequence """
    def bin_seq(self, num_bits):
        bin_lst = []
        for i in range(1<<num_bits):
            inner_lst = []
            s="{:0{}b}".format(i,num_bits)
            for i in s:
                inner_lst.append(int(i))
            bin_lst.append(tuple(inner_lst))
        ouput_tple = tuple(bin_lst)
        return ouput_tple
    
    """ Execute instructions """
    def execute(self, keys):
        if (keys == 'STP'):
            self.overflow = False
            print(SMState.STOPPED.value)
            return SMState.STOPPED
        
        elif (keys == 'DUP'):
            self.overflow = False
            if (len(self.stack) <= 0):
                print(SMState.ERROR.value)
                return SMState.ERROR
            else:
                lst_oprnd = self.stack.pop()
                self.stack.append(lst_oprnd)
                self.stack.append(lst_oprnd)
                print(SMState.RUNNING.value)
                return SMState.RUNNING
        
        elif (keys == 'DEL'):
            self.overflow = False
            if(len(self.stack) > 0):
                self.stack.pop()
                print(SMState.RUNNING.value)
                return SMState.RUNNING
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
        
        elif (keys == 'SWP'):
            self.overflow = False
            if(len(self.stack) > 1):
                lst_oprnd = self.stack.pop()
                scnd_lst_oprnd = self.stack.pop()
                self.stack.append(lst_oprnd)
                self.stack.append(scnd_lst_oprnd)
                print(SMState.RUNNING.value)
                return SMState.RUNNING
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
        
        elif (keys == "ADD"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               sum = lst_oprnd + scnd_lst_oprnd
               if(sum >= 0 and sum <= 255):
                   self.overflow = False
                   sum = c_ubyte(sum)
                   print(sum.value)
                   #sum = sum.value
                   self.stack.append(sum.value)
                   return SMState.RUNNING
               else:
                   self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
        
        elif (keys == "SUB"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               diff = scnd_lst_oprnd - lst_oprnd
               if(diff >= 0 and diff <= 255):
                   self.overflow = False
                   diff = c_ubyte(diff)
                   diff = diff.value
                   self.stack.append(diff)
                   print(diff)
                   return SMState.RUNNING
               else:
                   self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
            
        elif (keys == "MUL"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               product =lst_oprnd * scnd_lst_oprnd
               if(product >= 0 and product <= 255):
                   self.overflow = False
                   product = c_ubyte(product)
                   #sum = sum.value
                   self.stack.append(product.value)
                   print(product.value)
                   return SMState.RUNNING
               else:
                   self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
        
        elif (keys == "DIV"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            else:
                lst_oprnd = self.stack.pop()
                scnd_lst_oprnd = self.stack.pop()
                if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int and lst_oprnd > 0):
                    quotient = scnd_lst_oprnd // lst_oprnd
                    if(quotient >= 0 and quotient <= 255):
                        self.overflow = False
                        quotient = c_ubyte(quotient)
                        self.stack.append(quotient.value)
                        print(quotient.value)
                        return SMState.RUNNING
                    else:
                        self.overflow = True
                else:
                    print(SMState.ERROR.value)
                    return SMState.ERROR
            
        elif (keys == "EXP"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
                exp_output = scnd_lst_oprnd ** lst_oprnd
                if (type(exp_output) == int and exp_output >= 0 and exp_output <= 255):
                    self.overflow = False
                    exp_output = c_ubyte(exp_output)
                    #sum = sum.value
                    self.stack.append(exp_output.value)
                    print(exp_output.value)
                    return SMState.RUNNING
                else:
                    self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
            
        elif (keys == "MOD"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (lst_oprnd > 0 and type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               mod_output = scnd_lst_oprnd % lst_oprnd
               if(type(mod_output) == int and mod_output >= 0 and mod_output <= 255):
                   self.overflow = False
                   mod_output = c_ubyte(mod_output)
                   #sum = sum.value
                   self.stack.append(mod_output.value)
                   print(mod_output.value)
                   return SMState.RUNNING
               else:
                   self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
            
        elif (keys == "SHL"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               shl_output = scnd_lst_oprnd * (2**lst_oprnd)
               if(type(shl_output) == int and shl_output >= 0 and shl_output <= 255):
                   self.overflow = False
                   shl_output = c_ubyte(shl_output)
                   #sum = sum.value
                   self.stack.append(shl_output.value)
                   print(shl_output.value)
                   return SMState.RUNNING
               else:
                   self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
            
        elif (keys == "SHR"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               shr_output = (scnd_lst_oprnd // (2**lst_oprnd))
               if(type(shr_output) == int and shr_output >= 0 and shr_output <= 255):
                   self.overflow = False
                   shr_output = c_ubyte(shr_output)
                   #sum = sum.value
                   self.stack.append(shr_output.value)
                   print(shr_output.value)
                   return SMState.RUNNING
               else:
                   self.overflow = True
            else:
                print(SMState.ERROR.value)
                return SMState.ERROR
            
        #elif (keys == "HEX"):
        #    if(len(self.stack) <= 1):
        #        print(SMState.ERROR.value)
        #        return SMState.ERROR
        #    h_dec=[0,1,2,3,4,5,6,7,8,9,'A','B','C','E','F']
        #    lst_oprnd = self.stack.pop()
        #    scnd_lst_oprnd = self.stack.pop()
        #    if lst_oprnd in h_dec and scnd_lst_oprnd in h_dec:
        #        self.overflow = False
        #        str_output = str(lst_oprnd) + str(scnd_lst_oprnd)
        #        hex_output = int(str_output,16)
        #        hex_output = c_ubyte(hex_output)
        #        #hexa = hex_output.value
        #        self.stack.append(hex_output.value)
        #        print(hex_output.value)
        #        return SMState.RUNNING
        #    else:
        #        print(SMState.ERROR.value)
        #        return SMState.ERROR
        
        elif (keys == "HEX"):
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                #sys.exit()
                #print(SMState.ERROR.value)
                return SMState.ERROR
            h_dec=['A','B','C','E','F']
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (((type(lst_oprnd)==int) or (lst_oprnd in h_dec)) and ((type(scnd_lst_oprnd)==int) or (scnd_lst_oprnd in h_dec))):
                self.overflow = False
                str_output = str(lst_oprnd) + str(scnd_lst_oprnd)
                hex_output = int(str_output,16)
                if(type(hex_output) == int and (hex_output >= 0 and hex_output <= 255)):
                    hex_output = c_ubyte(hex_output)
                    self.stack.append(hex_output.value)
                    print(hex_output.value)
                    #print("HEX is complete!")
                    #self.result_display()
                    return SMState.RUNNING
                else:
                    self.overflow = True
                    print("Overflow!!")
                    return SMState.RUNNING
            else:
                print("Invalid data for hex")
                return SMState.ERROR
                #sys.exit()
        
        elif (keys == "FAC"):
            if(len(self.stack) <= 0):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) != int):
                print(SMState.ERROR.value)
                return SMState.ERROR
            fac = 1
            for i in range(1, lst_oprnd+1):
                fac = fac * i
            if(fac >= 0 and fac <= 255):
                self.overflow = False
                fac = c_ubyte(fac)
                #sum = sum.value
                self.stack.append(fac.value)
                print(fac.value)
                return SMState.RUNNING
            else:
                self.overflow = True
        
        elif (keys == "NOT"):
            if(len(self.stack) <= 0):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) != int):
                print(SMState.ERROR.value)
                return SMState.ERROR
            not_lst_oprnd = 255 - lst_oprnd
            if(not_lst_oprnd >= 0 and not_lst_oprnd <= 255):
                self.overflow = False
                not_lst_oprnd = c_ubyte(not_lst_oprnd)
                not_lst_oprnd = not_lst_oprnd.value
                print(not_lst_oprnd)
                self.stack.append(not_lst_oprnd)
                return SMState.RUNNING
            else:
                self.overflow = True
                
        elif (keys == "XOR"):
            if(len(self.stack) <= 1):
                print(SMState.ERROR.value)
                return SMState.ERROR
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) != int or type(scnd_lst_oprnd) != int):
                print(SMState.ERROR.value)
                return SMState.ERROR
            if (lst_oprnd <= 0 or scnd_lst_oprnd <= 0):
                print(SMState.ERROR.value)
                return SMState.ERROR
            self.overflow = False
            exor_output = lst_oprnd ^ scnd_lst_oprnd
            exor_output = c_ubyte(exor_output)
            #exor = exor.value
            self.stack.append(exor_output.value)
            print(exor_output.value)
            return SMState.RUNNING
            
        elif (keys == "SPEAK"):
            a = self.stack.pop()
            b = []
            while a <= len(self.stack):
                #print(a)
                if type(a) != int:
                    print(SMState.ERROR.value)
                    return SMState.ERROR
                else:
                    for i in range(0, a):
                        c = self.stack.pop()
                        b.append(str(c))
                    d = ''.join(b)
                    print(d)
                    print(SMState.RUNNING.value)
                    return SMState.RUNNING


def main():
    sm = StackMachine()
    sm.stack.clear()
    code_word = ((0, 0, 1, 0, 1, 1), (1, 0, 1, 0, 0, 1), (0, 1, 1, 1, 0, 0))
    for i in range(len(code_word)):
        sm.do(code_word[i])
    print(sm.stack)
    

if __name__ == '__main__':
    main()