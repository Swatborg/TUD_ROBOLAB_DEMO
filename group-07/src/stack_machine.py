#!/usr/bin/env python3

from enum import IntEnum
from typing import List, Tuple, Union
from ctypes import c_ubyte
from robot import*
import sys


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
            print("Given integer: ", outptut)
            self.stack.append(outptut)
            #print(self.stack)
            return SMState.RUNNING
        
        # Instruction
        elif (code_word_lst[0] == 0 and code_word_lst[1] == 1 ):
            instruction_lst = code_word_lst.copy()
            instruction_tple = tuple(instruction_lst[2:])
            if (instruction_tple in self.ins_dict.keys()):
                #print(self.stack)
                return self.execute(self.ins_dict[instruction_tple])
            
        # Character
        elif (code_word_lst[0] == 1):
            operand_lst = code_word_lst.copy() 
            operand_tple = tuple(operand_lst[1:])
            if (operand_tple in self.operand_dict.keys()):
                if (self.operand_dict[operand_tple] == 'NOP'):
                    print('No Operation')
                    return SMState.RUNNING
                elif (self.operand_dict[operand_tple] == 'SPEAK'):
                    return self.execute('SPEAK')
                elif (self.operand_dict[operand_tple] == 'SPACE'):
                    print("Given character: ", self.operand_dict[operand_tple])
                    self.stack.append(' ')
                    return SMState.RUNNING
                else:
                    self.stack.append(self.operand_dict[operand_tple])
                    print("Given character: ", self.operand_dict[operand_tple])
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
    
    """ Display on Robot """
    def result_display(self):
        if (len(self.stack) <= 0):
            print(self.stack)
            print("None")
        else:
            print(self.stack)
            print("last element", self.stack[-1])
    
    """ Execute instructions """
    def execute(self, keys):
        if (keys == 'STP'):
            self.overflow = False
            #return SMState.STOPPED
            print("Stop Function. The program is being terminated!")
            sys.exit()
        
        elif (keys == 'DUP'):
            print("Instruction DUP")
            self.overflow = False
            if (len(self.stack) <= 0):
                print("Not enough items in the stack")
                sys.exit()
            else:
                lst_oprnd = self.stack.pop()
                self.stack.append(lst_oprnd)
                self.stack.append(lst_oprnd)
                self.result_display()
                return SMState.RUNNING
        
        elif (keys == 'DEL'):
            print("Instruction DEL")
            self.overflow = False
            if(len(self.stack) > 0):
                self.stack.pop()
                print("DEL is complete!")
                self.result_display()
                return SMState.RUNNING
            else:
                print("Not enough items in the stack")
                sys.exit()
        
        elif (keys == 'SWP'):
            #print("Instruction SWP")
            self.overflow = False
            if(len(self.stack) > 1):
                #print(self.stack)
                lst_oprnd = self.stack.pop()
                scnd_lst_oprnd = self.stack.pop()
                #print(self.stack)
                self.stack.append(lst_oprnd)
                self.stack.append(scnd_lst_oprnd)
                print("SWP is complete!")
                self.result_display()
                return SMState.RUNNING
            else:
                print("Not enough items in the stack")
                sys.exit()
        
        elif (keys == "ADD"):
            print("Instruction ADD")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               sum = lst_oprnd + scnd_lst_oprnd
               if(sum >= 0 and sum <= 255):
                   self.overflow = False
                   sum = c_ubyte(sum)
                   self.stack.append(sum.value)
                   print("ADD is complete!")
                   self.result_display()
                   return SMState.RUNNING
               else:
                   self.overflow = True
                   print("Overflow!!")
                   return SMState.RUNNING
            else:
                print("Invalid data for addition")
                sys.exit()
        
        elif (keys == "SUB"):
            print("Instruction SUB")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               diff = scnd_lst_oprnd - lst_oprnd
               if(diff >= 0 and diff <= 255):
                   self.overflow = False
                   diff = c_ubyte(diff)
                   diff = diff.value
                   self.stack.append(diff)
                   print("SUB is complete!")
                   self.result_display()
                   return SMState.RUNNING
               else:
                   self.overflow = True
                   print("Overflow!!")
                   return SMState.RUNNING
            else:
                print("Invalid data for subtraction")
                sys.exit()
            
        elif (keys == "MUL"):
            print("Instruction MUL")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
               product =lst_oprnd * scnd_lst_oprnd
               if(product >= 0 and product <= 255):
                   self.overflow = False
                   product = c_ubyte(product)
                   self.stack.append(product.value)
                   print("MUL is complete!")
                   self.result_display()
                   return SMState.RUNNING
               else:
                   self.overflow = True
                   print("Overflow!!")
                   return SMState.RUNNING
            else:
                print("Invalid data for multiplication")
                sys.exit()
        
        elif (keys == "DIV"):
            print("Instruction DIV")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            else:
                lst_oprnd = self.stack.pop()
                scnd_lst_oprnd = self.stack.pop()
                if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int and lst_oprnd > 0):
                    quotient = scnd_lst_oprnd // lst_oprnd
                    if(quotient >= 0 and quotient <= 255):
                        self.overflow = False
                        quotient = c_ubyte(quotient)
                        self.stack.append(quotient.value)
                        print("DIV is complete!")
                        self.result_display()
                        return SMState.RUNNING
                    else:
                        self.overflow = True
                        print("Overflow!!")
                        return SMState.RUNNING
                else:
                    #return SMState.ERROR
                    print("Invalid data for division")
                    sys.exit()
            
        elif (keys == "EXP"):
            print("Instruction EXP")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
                if (lst_oprnd >=0 and scnd_lst_oprnd >=0):
                    exp_output = scnd_lst_oprnd ** lst_oprnd
                    if (type(exp_output) == int and exp_output >= 0 and exp_output <= 255):
                        self.overflow = False
                        exp_output = c_ubyte(exp_output)
                        self.stack.append(exp_output.value)
                        print("EXP is complete!")
                        self.result_display()
                        return SMState.RUNNING
                    else:
                        self.overflow = True
                        print("Overflow!!")
                        return SMState.RUNNING
                else:
                    print("Invalid operand for EXP")
                    sys.exit()
            else:
                print("Invalid data for EXP")
                sys.exit()
            
        elif (keys == "MOD"):
            print("Instruction MOD")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if ((type(lst_oprnd) == int and type(scnd_lst_oprnd) == int) and lst_oprnd >=0):
                mod_output = scnd_lst_oprnd % lst_oprnd
                if(type(mod_output) == int and mod_output >= 0 and mod_output <= 255):
                    self.overflow = False
                    mod_output = c_ubyte(mod_output)
                    self.stack.append(mod_output.value)
                    print("MOD is complete!")
                    self.result_display()
                    return SMState.RUNNING
                else:
                    self.overflow = True
                    print("Overflow!!")
                    return SMState.RUNNING
            else:
                print("Invalid data or operand for MOD")
                sys.exit()
            
        elif (keys == "SHL"):
            print("Instruction SHL")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
                if (lst_oprnd >=0 and scnd_lst_oprnd >= 0):
                    shl_output = scnd_lst_oprnd * (2**lst_oprnd)
                    if(type(shl_output) == int and shl_output >= 0 and shl_output <= 255):
                        self.overflow = False
                        shl_output = c_ubyte(shl_output)
                        #sum = sum.value
                        self.stack.append(shl_output.value)
                        print("SHL is complete!")
                        self.result_display()
                        return SMState.RUNNING
                    else:
                        self.overflow = True
                        print("Overflow!!")
                        return SMState.RUNNING
                else:
                    print("Invalid operand for SHL")
                    sys.exit()
            else:
                print("Invalid data for SHL")
                sys.exit()
            
        elif (keys == "SHR"):
            print("Instruction SHR")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) == int and type(scnd_lst_oprnd) == int ):
                if (lst_oprnd >=0 and scnd_lst_oprnd >= 0):
                    shr_output = (scnd_lst_oprnd // (2**lst_oprnd))
                    if(type(shr_output) == int and shr_output >= 0 and shr_output <= 255):
                        self.overflow = False
                        shr_output = c_ubyte(shr_output)
                        self.stack.append(shr_output.value)
                        print("SHR is complete!")
                        self.result_display()
                        return SMState.RUNNING
                    else:
                        self.overflow = True
                        print("Overflow!!")
                        return SMState.RUNNING
                else:
                    print("Invalid operand for SHR")
                    sys.exit()
            else:
                print("Invalid data for SHR")
                sys.exit()
            
        #elif (keys == "HEX"):
        #    print("Instruction HEX")
        #    if(len(self.stack) <= 1):
        #        print("Not enough items in the stack")
        #        sys.exit()
        #        #print(SMState.ERROR.value)
        #        #return SMState.ERROR
        #    h_dec=[0,1,2,3,4,5,6,7,8,9,'A','B','C','E','F']
        #    lst_oprnd = self.stack.pop()
        #    scnd_lst_oprnd = self.stack.pop()
        #    if ((lst_oprnd in h_dec) and (scnd_lst_oprnd in h_dec)):
        #        self.overflow = False
        #        str_output = str(lst_oprnd) + str(scnd_lst_oprnd)
        #        hex_output = int(str_output,16)
        #        if(type(hex_output) == int and (hex_output >= 0 and hex_output <= 255)):
        #            hex_output = c_ubyte(hex_output)
        #            self.stack.append(hex_output.value)
        #            print("HEX is complete!")
        #            self.result_display()
        #            return SMState.RUNNING
        #        else:
        #            self.overflow = True
        #            print("Overflow!!")
        #            return SMState.RUNNING
        #    else:
        #        print("Invalid data for hex")
        #        sys.exit()
        
        elif (keys == "HEX"):
            print("Instruction HEX")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            h_dec=['A','B','C','D','E','F']
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (((type(lst_oprnd)==int) or (lst_oprnd in h_dec)) and ((type(scnd_lst_oprnd)==int) or (scnd_lst_oprnd in h_dec))):
                self.overflow = False
                str_output = str(lst_oprnd) + str(scnd_lst_oprnd)
                hex_output = int(str_output,16)
                if(type(hex_output) == int and (hex_output >= 0 and hex_output <= 255)):
                    hex_output = c_ubyte(hex_output)
                    self.stack.append(hex_output.value)
                    print("HEX is complete!")
                    self.result_display()
                    return SMState.RUNNING
                else:
                    self.overflow = True
                    print("Overflow!!")
                    return SMState.RUNNING
            else:
                print("Invalid data for hex")
                sys.exit()
        
        elif (keys == "FAC"):
            print("Instruction FAC")
            if(len(self.stack) <= 0):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) != int):
                print("Invalid data for FAC")
                sys.exit()
            fac = 1
            for i in range(1, lst_oprnd+1):
                fac = fac * i
            if(fac >= 0 and fac <= 255):
                self.overflow = False
                fac = c_ubyte(fac)
                #sum = sum.value
                self.stack.append(fac.value)
                print("FAC is complete!")
                self.result_display()
                return SMState.RUNNING
            else:
                self.overflow = True
                print("Overflow!!")
                return SMState.RUNNING
        
        elif (keys == "NOT"):
            print("Instruction NOT")
            if(len(self.stack) <= 0):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) != int):
                print("Invalid data for NOT")
                sys.exit()
            elif (lst_oprnd <=0):
                print("Invalid data for NOT")
                sys.exit()
            not_lst_oprnd = 255 - lst_oprnd
            if(not_lst_oprnd >= 0 and not_lst_oprnd <= 255):
                self.overflow = False
                not_lst_oprnd = c_ubyte(not_lst_oprnd)
                not_lst_oprnd = not_lst_oprnd.value
                self.stack.append(not_lst_oprnd)
                print("NOT is complete!")
                self.result_display()
                return SMState.RUNNING
            else:
                self.overflow = True
                print("Overflow!!")
                return SMState.RUNNING
                
        elif (keys == "XOR"):
            print("Instruction XOR")
            if(len(self.stack) <= 1):
                print("Not enough items in the stack")
                sys.exit()
            lst_oprnd = self.stack.pop()
            scnd_lst_oprnd = self.stack.pop()
            if (type(lst_oprnd) != int or type(scnd_lst_oprnd) != int):
                print("Invalid data for XOR")
                sys.exit()
            if (lst_oprnd <= 0 or scnd_lst_oprnd <= 0):
                print('Invalid operand for XOR')
                sys.exit()
            exor_output = lst_oprnd ^ scnd_lst_oprnd
            if (exor_output >= 0 and exor_output<= 255):
                self.overflow = False
                exor_output = c_ubyte(exor_output)
                self.stack.append(exor_output.value)
                print("XOR is complete!")
                self.result_display()
                return SMState.RUNNING
            else:
                self.overflow = True
                print("Overflow!!")
                return SMState.RUNNING
            
        elif (keys == "SPEAK"):
            print("Instruction SPEAK")
            lst_oprnd = self.stack.pop()
            speaklst = []
            if (type(lst_oprnd) == int):
                if (lst_oprnd <= len(self.stack)):
                    for i in range(0, lst_oprnd):
                        char = self.stack.pop()
                        speaklst.append(str(char))
                    speakstr = ''.join(speaklst)
                    print('speak value:',speakstr)
                    ev3.Sound.speak(speakstr)
                    return SMState.RUNNING     
                else:
                    print('Limit exceeded!!')
                    sys.exit()
            else:
                print("Invalid data for SPEAK")
                sys.exit()
        
        #elif (keys == "SPEAK"):
        #    print("Instruction SPEAK")
        #    a = self.stack.pop()
        #    b = []
        #    while a <= len(self.stack):
        #        #print(a)
        #        if type(a) != int:
        #            print(SMState.ERROR.value)
        #            return SMState.ERROR
        #        else:
        #            for i in range(0, a):
        #                c = self.stack.pop()
        #                b.append(str(c))
        #            d = ''.join(b)
        #            print(d)
        #            print(SMState.RUNNING.value)
        #            return SMState.RUNNING
        

#def main():
#    sm  = StackMachine()
#    sm.stack.clear()
#    code_word = ((1,0,0,1,1,0),(0,0,0,1,0,1),(0,1,0,0,1,1))
#    #code_word = ((1,0,0,1,1,0),(0,0,0,1,0,1),(0,1,1,1,0,0)) # HEX [C,5,HEX] = 92
#    #code_word = ((1,1,0,0,1,0),(1,0,1,1,1,1),(1,0,1,1,1,1),(1,0,1,0,0,0),(1,0,1,0,1,1),(0,0,0,1,0,1),(1,0,0,0,0,1))
#    #code_word = ((0, 0, 1, 1, 0, 0), (0, 0, 0, 0, 1, 0), (0, 0, 0, 0, 1, 0),(1, 0, 0, 0, 0, 1))
#    for i in range(len(code_word)):
#        sm.do(code_word[i])
#
#
#if __name__=="__main__":
#    main()


