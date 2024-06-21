#!/usr/bin/env python3

from enum import Enum
from typing import List, Tuple, Union


# IMPORTANT NOTE: DO NOT IMPORT THE ev3dev.ev3 MODULE IN THIS FILE

class HCResult(Enum):
    """
    Return codes for the Hamming Code interface
    """
    VALID = 'OK'
    CORRECTED = 'FIXED'
    UNCORRECTABLE = 'ERROR'


class HammingCode:
    """
    Provides decoding capabilities for the specified Hamming Code
    """

    def __init__(self):
        """
        Initializes the class HammingCode with all values necessary.
        """
        self.total_bits = 10  # n
        self.data_bits = 6  # k
        self.parity_bits = 4  # r

        # Predefined non-systematic generator matrix G'
        gns = [[1,1,1,0,0,0,0,1,0,0],
               [0,1,0,0,1,0,0,1,0,0],
               [1,0,0,1,0,1,0,0,0,0],
               [0,0,0,1,0,0,1,1,0,0],
               [1,1,0,1,0,0,0,1,1,0],
               [1,0,0,1,0,0,0,1,0,1]
               ]

        # Convert non-systematic G' into systematic matrices G, H
        self.g = self.__convert_to_g(gns)
        self.h = self.__derive_h(self.g)

    def __convert_to_g(self, gns: List):
        """
        Converts a non-systematic generator matrix into a systematic

        Args:
            gns (List): Non-systematic generator matrix
        Returns:
            list: Converted systematic generator matrix
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        # pass
        gs = gns.copy()
        
        """ Predefined operation list for converting to g """
        op_list = [[3,5,6],
                   [1,3,6],
                   [1,5,6],
                   [1,3],
                   [2,3],
                   [1,2,5]]
        
        """ Adjusted list for converting to generator matrix """
        op_list_adjusted = op_list.copy()
        for i in range(len(op_list)):
          for j in range(len(op_list[i])):
            op_list_adjusted[i][j] = op_list[i][j] - 1 
            
        for i in range(len(gs)):
          for j in range(len(op_list_adjusted[i])):
            for m in range(10):
              gs[op_list_adjusted[i][j]][m] = abs(gs[op_list_adjusted[i][j]][m] - gs[i][m])
              
        #self.print_matrix(gs)
        #print()
        return gs

    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        # pass
        gs_copy = self.g.copy()
        par_dump = self.create_matrix(6,4)
        for i in range(len(par_dump)):
          index = self.shape_matrix(par_dump)[1]
          for j in range(len(par_dump[i])):
            pos = (self.shape_matrix(gs_copy))[1]
            par_dump[i][j] = gs_copy[i][pos-index]
            index = index -1
            
        par_dump_t = self.transposed_matrix(par_dump)
        i_matrix = self.identity_matrix(4,4) 

        parity_check_matrix = par_dump_t.copy()
        for i in range(4):
          for j in range(4):
            parity_check_matrix[i].append(i_matrix[i][j])
            
        #self.print_matrix(parity_check_matrix)
        #print()
        return parity_check_matrix
        
    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        # pass
        g_calculate = self.g.copy()
        a_vector = [i for i in source_word]
        source_word_lst_format = []
        source_word_lst_format.append(a_vector)  
        x_vector = self.multiply_matrix(source_word_lst_format,g_calculate)

        """ Add parity bit P5 (even parity) """
        x_vector_parity = x_vector.copy()
        index_parity = 2
        parity_bit = (x_vector_parity[0][0]+x_vector_parity[0][1])%2
        while (index_parity < len(x_vector_parity[0])):
          parity_bit = (parity_bit + x_vector_parity[0][index_parity])%2
          index_parity = index_parity + 1
        #parity_bit = 1 - parity_bit # for odd parity

        x_vector_parity[0].append(parity_bit)
        encode_tuple_parity = tuple(x_vector_parity[0])
        
        return encode_tuple_parity

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        # pass
        par_h = self.h.copy()
        #self.print_matrix(par_h)
        #print()
        x_vector = [i for i in encoded_word]
        x_vector_striped = x_vector[:-1]
        encoded_word_lst_fmt = []
        encoded_word_lst_fmt.append(x_vector_striped) 
        
        """ do parity check """
        encoded_word_lst_fmt_parity = encoded_word_lst_fmt.copy()
        index_parity = 2
        parity_bit_bool = True
        parity_bit = (encoded_word_lst_fmt_parity[0][0]+encoded_word_lst_fmt_parity[0][1])%2
        while (index_parity < len(encoded_word_lst_fmt_parity[0])):
          parity_bit = (parity_bit + encoded_word_lst_fmt_parity[0][index_parity])%2
          index_parity = index_parity + 1
        # parity_bit = 1 - parity_bit # for odd parity
        
        """ Overall parity bit check """
        if (parity_bit == x_vector[-1]):
            parity_bit_bool = True
        else:
            parity_bit_bool = False
        
        # print(parity_bit_bool)
        
        """ Get syndrome vector """
        
        encoded_word_lst_fmt_transposed = self.transposed_matrix(encoded_word_lst_fmt)
        par_h_t = self.transposed_matrix(par_h)

        z_vector = self.multiply_matrix(par_h,encoded_word_lst_fmt_transposed)
        z_vector_t = self.transposed_matrix(z_vector)
        # self.print_matrix(z_vector_t)
        # print()
        
        """ Match the syndrome with H-matrix"""
        syndrome = []

        for i in range(len(par_h_t)):
          if (par_h_t[i] == z_vector_t[0]):
            syndrome.append(i)

        # print(syndrome)
        # print(len(syndrome))
        
        """ SECDED output decision"""
        
        if ((len(syndrome) == 0 and  z_vector_t[0] == [0,0,0,0]) and parity_bit_bool == True):
          return tuple(encoded_word_lst_fmt[0][0:6]),HCResult.VALID
        elif ((len(syndrome) == 0 and  z_vector_t[0] == [0,0,0,0]) and parity_bit_bool == False): 
          encoded_word_lst_fmt[0][-1]= 1 - encoded_word_lst_fmt[0][-1]
          return tuple(encoded_word_lst_fmt[0][0:6]),HCResult.CORRECTED
        elif ((len(syndrome) != 0 and  z_vector_t[0] != [0,0,0,0]) and parity_bit_bool == False):
          encoded_word_lst_fmt[0][syndrome[0]]= 1 - encoded_word_lst_fmt[0][syndrome[0]] 
          return tuple(encoded_word_lst_fmt[0][0:6]),HCResult.CORRECTED
        elif (((len(syndrome) == 0 and z_vector_t[0] != [0,0,0,0])) and parity_bit_bool == False):
          return None,HCResult.UNCORRECTABLE
        elif (z_vector_t[0] != [0,0,0,0] and parity_bit_bool == True):
          return None,HCResult.UNCORRECTABLE
        else:
            return None,HCResult.UNCORRECTABLE
    
    """ additional methods """
    def print_matrix(self,list):
        for i in range(len(list)):
            for j in range(len(list[i])):
                print(list[i][j], end=' ')
            print()
      
    def create_matrix(self,rows,cols):
        matrix = [[0 for i in range(cols)] for j in range(rows)]
        return matrix
    
    def identity_matrix(self, rows,cols):
          i_matrix = [[(1 if j == i else 0) for i in range(cols)] for j in range(rows)]
          return i_matrix
      
    def shape_matrix(self,list):
        shape = [0,0]
        shape[0] = len(list)
        for i in range(len(list)):
          for j in range(len(list[i])):
            shape[1] = j
          break
        
        shape[1] = shape[1] + 1     
        return shape
    
    def transposed_matrix(self,list):
        transposed_matrix = self.create_matrix((self.shape_matrix(list)[1]),(self.shape_matrix(list)[0]))
        transposed_matrix = [[list[i][j] for i in range(self.shape_matrix(transposed_matrix)[1])] for j in range(self.shape_matrix(transposed_matrix)[0])]
        return transposed_matrix

    def multiply_matrix(self,a,b):
        size_a = self.shape_matrix(a)
        size_b = self.shape_matrix(b)

        if (size_a[1] == size_b[0]):
            output_matrix = self.create_matrix(size_a[0],size_b[1])
            b_t = self.transposed_matrix(b)
            for i in range(len(output_matrix)):
                index = 0
                for j in range(len(output_matrix[i])):
                    output_matrix[i][j] = 0
                    for l in range(len(b_t[index])):
                        output_matrix[i][j] = (output_matrix[i][j] + (a[i][l] * b_t[index][l]))%2
                    index = index + 1
        else:
            return("Incompatible Matrices")
          
        return output_matrix
       

def main():
  encoded_data  = HammingCode()
  encode_lst = [(0, 1, 1, 0, 1, 1),
                (0, 0, 0, 0, 0, 0),
                (1, 0, 1, 1, 0, 1),
                (1, 1, 1, 1, 1, 0)]
  
  for i in range(4):
      print(encoded_data.encode(encode_lst[i]))
  print()
  
  decoded_data  = HammingCode()
  decode_lst = [(0,0,1,0,1,1,1,1,1,1,0),
                (0,0,0,0,0,0,0,0,0,0,1),
                (1,0,1,1,0,1,1,1,1,0,1),
                (1,1,1,1,1,0,1,0,1,1,1)]
  
  for i in range(4):
      print(decoded_data.decode(decode_lst[i]))
  print()
  
if __name__=="__main__":
    main()