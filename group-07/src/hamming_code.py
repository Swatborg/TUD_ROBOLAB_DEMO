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
        #pass
        
        """ We derive the generator matrix from the predefined steps
        """
        gm_systemiatic = gns.copy()

        operation_steps = [[2,4,5],
                           [0,2,5],
                           [0,4,5],
                           [0,2],
                           [1,2],
                           [0,1,4]]
        
        for k in range(len(operation_steps)):
            for j in operation_steps[k]:
                for i in range(10):
                    gm_systemiatic[j][i]=abs(gm_systemiatic[j][i] - gm_systemiatic[k][i] ) 
                    
                    
        return gm_systemiatic
 

    def __derive_h(self, g: List):
        """
        This method executes all steps necessary to derive H from G.

        Args:
            g (List):
        Returns:
            list:
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #pass
        parity_matrix = [[0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0]]
        
        for j in range(6):
            for i in range(4):
                parity_matrix[i][j]=self.g[j][i+6]
                continue
        
        for i in range(4):
            parity_matrix[i][i+6] = 1
            
        return parity_matrix 

    def encode(self, source_word: Tuple[int, ...]) -> Tuple[int, ...]:
        """
        Encodes the given word and returns the new codeword as tuple.

        Args:
            source_word (tuple): m-tuple (length depends on number of data bits)
        Returns:
            tuple: n-tuple (length depends on number of total bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #pass
        encoded_word = []
        for i in range(10):
            sum = 0; counter = 0
            for j in source_word:
                sum = sum + (j * self.g[counter][i])
                counter = counter + 1
            encoded_word.append((sum)%2)
        #print(encoded_word)
        
        """ Even parity bit added """
        ones_count = 0
        for i in range(10):
            if (encoded_word[i] == 1):
                ones_count = ones_count + 1
                
        if (ones_count % 2 == 0):
            encoded_word.append(0) #0
        else:
            encoded_word.append(1) #1
                
        return tuple(encoded_word)
        

    def decode(self, encoded_word: Tuple[int, ...]) -> Tuple[Union[None, Tuple[int, ...]], HCResult]:
        """
        Checks the channel alphabet word for errors and attempts to decode it.
        Args:
            encoded_word (tuple): n-tuple (length depends on number of total bits)
        Returns:
            Union: (m-tuple, HCResult) or (None, HCResult)(length depends on number of data bits)
        """

        # REPLACE "pass" WITH YOUR IMPLEMENTATION
        #pass
        """ Encoded word list """
        encoded_word_lst = [i for i in encoded_word]
        
        """ Transpose H-Mstrix """
        h_t = []
        
        for i in range(10):
            dump_lst = []
            for j in range(4):
                dump_lst.append(self.h[j][i])
            h_t.append(dump_lst)
            
        #for i in range(len(h_t)):
        #    for j in range(len(h_t[i])):
        #        print(h_t[i][j], end=' ') 
        #    print()
        #print()
                
        """ Parity bit verify """
        zero_count = 0
        for i in range(10):
            if (encoded_word[i] == 0):
                zero_count = zero_count + 1
                
        ones_count = 0
        for i in range(10):
            if (encoded_word[i] == 1):
                ones_count = ones_count + 1
            
        #print("zeros: ",zero_count)
        #print("ones: ",ones_count)
        
        parity_bit = 0 if ones_count%2 == 0 else 1 #change happen
        parity_flag = True if parity_bit == encoded_word[-1] else False
            
        # print(parity_flag)
        
        """ Get syndrome """
        syndrome = []
        for i in range(4):
            sum = 0; counter = 0
            for j in encoded_word[:10]:
                sum = sum + (j * self.h[i][counter])
                counter = counter + 1
            syndrome.append((sum)%2)
        # print(syndrome)
        
        """ Detect flipped bit """
        flipped_bit = -1
        for i in range(len(h_t)):
            if h_t[i] == syndrome:
                flipped_bit = i
                
        # print(flipped_bit)
        
        """ Output """
        if ((flipped_bit == -1 and syndrome == [0,0,0,0]) and parity_flag == True):      # no error
          print("No Error")
          return tuple(encoded_word_lst[0:6])
          #return tuple(encoded_word_lst[0:6]),HCResult.VALID
        elif ((flipped_bit == -1 and syndrome == [0,0,0,0]) and parity_flag == False):   # Only Parity bit flipped
          encoded_word_lst[-1]= 1 - encoded_word_lst[-1] 
          print("Fixed. Only Parity bit flipped!")
          return tuple(encoded_word_lst[0:6])
          #return tuple(encoded_word_lst[0:6]),HCResult.CORRECTED
        elif ((flipped_bit >= 0 and syndrome != [0,0,0,0]) and parity_flag == False):    # Sigle Error
          encoded_word_lst[flipped_bit]= 1 - encoded_word_lst[flipped_bit] 
          print("Fixed. Single Error!")
          return tuple(encoded_word_lst[0:6])
          #return tuple(encoded_word_lst[0:6]),HCResult.CORRECTED
        elif ((flipped_bit == -1 and syndrome != [0,0,0,0]) and parity_flag == False):   # Multiple Error
          print("Multiple Error")
          return None
          #return None,HCResult.UNCORRECTABLE
        elif (syndrome != [0,0,0,0] and parity_flag == True):                            # Multiple Error
          print("Multiple Error")
          return None
          #return None,HCResult.UNCORRECTABLE
        else:
            print("Multiple Error")
            return None
            #return None,HCResult.UNCORRECTABLE 

def main():
  encoded_data  = HammingCode()
  encode_lst = [(0, 0, 0, 1, 0, 1),
                (0, 1, 1, 1, 0, 1),
                (0, 1, 0, 0, 0, 0)]
  #encode_lst = [(0, 1, 1, 0, 1, 1),
  #              (0, 0, 0, 0, 0, 0),
  #              (1, 0, 1, 1, 0, 1),
  #              (1, 1, 1, 1, 1, 0)]
  
  for i in range(4):
      print(encoded_data.encode(encode_lst[i]))
  #print(encoded_data.encode((1, 1, 1, 0, 1, 1)))
  print()
  
  #decoded_data  = HammingCode()
  #decode_lst = [(0,1,1,0,1,1,1,1,1,1,1),
  #              (0,0,0,0,0,0,0,0,0,0,1),
  #              (1,0,1,1,0,1,1,1,1,0,1),
  #              (1,1,1,1,1,0,1,0,1,1,1)]
  #
  #for i in range(4):
  #    print(decoded_data.decode(decode_lst[i]))
  
  #print(encoded_data.decode((0,1,1,0,1,1,0,1,1,0,1)))


if __name__=="__main__":
    main()