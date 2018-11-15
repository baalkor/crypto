###############3
#   Viginiere.py
# Author : baalkor
# Goal :
# The goal of this script is to
#     1 - encrypt a given text with a key using viginiere
#     2 - decrypt a given ciphered text  with a key using viginiere
#     3 - decrypt a given ciphered text  with statistical analysis
################
import string

fr_LETTER_ = {
'E':15.87,
'N':7.15,
'D':3.39,
'Q':1.06,
'H':0.77,
'A':9.42,
'R':6.46,
'M':3.24,
'G':1.04,
'Z':0.32,
'I':8.41,
'U':6.24,
'P':2.86,
'B':1.02,
'X':0.30,
'S':7.90,
'L':5.34,
'C':2.64,
'F':0.95,
'Y':0.24,
'T':7.26,
'O':5.14,
'V':2.15,
'J':0.89,
'K':0.001,
 'W':0.001
}

########################3
# Return a an array of a letter starting from a given letter
def aplhabet_from_here(char):
    ouAlphabet = []
    for i in range(26):
        pos_char = string.ascii_uppercase.find(char.upper())
        pos_nchar = (pos_char + i) % 26
        ouAlphabet.append(string.ascii_uppercase[pos_nchar])

    return ouAlphabet


#################
# vignier cipher
#   for a given plain text and a key encode *or decode* the text
#
def cipher_vignier(plain_text, key, encode=True):
    oStr = ''
    keyIndexCt=0
    lKey = len(key)
    for character in plain_text.upper():
        if string.ascii_uppercase.find(character) >=0:
            keyEntry = aplhabet_from_here(key[keyIndexCt % lKey].upper())
            if encode:
                indexOfChar = string.ascii_uppercase.index(character)
                cipherData = keyEntry[indexOfChar]
            else:
                cipherData = string.ascii_uppercase[ keyEntry.index(character) ]

            oStr+= cipherData
            keyIndexCt = (keyIndexCt + 1) % lKey
        else:
            oStr += character


    return oStr
#########################3
# sanitize a string and pad to match key  len, keeps only alphabet character
#  IN : text
#     : klen
# OUT : data
def sanitize(text, klen):
    oData = []
    for letter in text.upper():
        if string.ascii_uppercase.find(letter) >= 0:
            oData.append(letter)

    padding = len(oData) % klen

    return oData



###############
# ic : Coincidence indice for a given text
# IN : test < Test to analyse
# OUT: ic : indice
def ic(text):
    dicCount = {}.fromkeys(string.ascii_uppercase)
    for k in dicCount:
        dicCount[k] = 0
    for letter in text:
            dicCount[letter] += 1
    ic = 0.
    for occurence in dicCount:
        n =  len(text)
        ic += (dicCount[occurence] * (dicCount[occurence] - 1 )) / (n * ( n - 1 ))

    return ic

####################
# blockify : cut a given text in pieces of given length
# IN : data : Text to cut
#    : estKeyLen : Estimated key length
# out : matrix

def blockify(data, estKeyLen):
    matrix = []
    hasData = True

    ki = 0
    while hasData:
        block_end = ki + estKeyLen
        matrix.append(data[ki:block_end])
        ki = block_end
        hasData = block_end < len(data)
    return matrix
#####################
# Transpose : create a matrix where first line is the concatenation of
#             every first char, second every snd characters, third ...
#             eg :
#                    [ A X F R E , B E G D, E A G R ] => [ A, B, E ] [ X, E, A ] ..
# IN : original matrix
# OUT : transformed matrix
def transpose(matrix):
    matrix_inv = [[] for x in range(len(matrix))]

    c = 0
    for x in range(len(matrix[c])):
        line = []
        for y in range(len(matrix)):
            try:  # This excpection if matrix is not squared.. not the best solution probably
                line.append(matrix[y][x])
            except IndexError:
                continue
        matrix_inv.append(line)
        c += 1
    matrix_inv = [x for x in matrix_inv if x]
    return matrix_inv
##########################
# ics_matrix : compute coindicence index for a given matrix
def ics_matrix(matrix):
    ics_score = []
    k = 0.
    for y in range(len(matrix)):
        data = "".join(matrix[y])
        if len(data) > 1:
            k  += ic(data)

    return k
##############################
# decode : Produce a charcater with shifted value like the caesar cipher does
# IN : letter
# OUT : letter declaed eg A + 3 => D
def decode(letter,shift):
    if letter.isspace() or letter == "'":
        return letter
    letter_pos = ord(letter) - ord('A') - 1
    n_letter_pos = (letter_pos + shift) % 26
    n_letter = chr(ord('A') + n_letter_pos )
    return n_letter.upper()

#####################
# chiSquared : Compute chi-squared indice for a given test
# IN : text to analyze
# OUT: indice
def chiSquared(text):
    ch = 0
    letter = dict(zip([ x for x in string.ascii_uppercase] , [0 for x in range(26)])) #
    for char in text.upper():
        letter[char] +=1

    for le in letter:
        expected = fr_LETTER_[le] * 0.01
        ch  += (letter[le] - expected) ** 2.  / expected

    return ch

######################
# decodeB : decode a buffer with a given shift
#  IN : buffer : text
#     : buffsize : How many characyer
#     : shift : shift to apply to each letter
#  OUT :
def decodeB(buffer, buffsize, shift):
    oStr = ""

    for i in range(0, len(buffer),buffsize):
        for char in buffer[i:i+buffsize]:
            oStr += decode(char, shift)

    return oStr
##################
# get_key_len : Determine key length for the viginiere cipher
# IN : text
#     : key_range, estimated key range
# OUT : Key length found
def get_key_len(text, key_range):
    avglen = {}
    for estKeyLen in key_range:
        data = sanitize(text, estKeyLen)
        matrix_inv = transpose(blockify(data, estKeyLen))
        avglen[ics_matrix(matrix_inv)] = estKeyLen
    return avglen[max(avglen)]

################
# low : for a given matrix of chi-squared return the corresponding letter
# IN : matrix of [ ('AVDFE':0.002) , ('EDSGE' : 1.000 }
# OUT : corresponding character
def low(matrix):
    old = matrix[0][1]
    ko = 0
    for i in range(len(matrix)):
        if matrix[i][1] > old:
            old = matrix[i][1]
            ko = i

    return chr(ord('A')  + ko )

########################
# chiSquaedM :
#     INT :
def chiSquaedM(data,l):
    caesr_chi = []
    for x in range(1,26):
            d = decodeB(data,l,x)
            c = chiSquared(d)
            caesr_chi.append((d,c))
    return caesr_chi

def vignier_crack(cipherData, key_range):
    keyLen = get_key_len(cipherData, key_range)
    data = sanitize(cipherData.upper(), keyLen)
    results = []
    for h in range(keyLen):
        td = []
        for i in range(h, len(data), keyLen):  td.append(data[i])
        results.append(low(chiSquaedM(td,keyLen)))
    return "".join(results)


if __name__ == "__main__":
    plainText = "Attaquer a l'aube".upper()
    key = "axfre".upper()
    cipheredText = cipher_vignier(plainText, key)
    print("Demo : ")
    print("KEY   |%s" % key)
    print("PLAIN |%s" % plainText)
    print("ENC   |%s" % cipheredText)
    print("DEC   |%s" % cipher_vignier(cipheredText, key,False))
    print("CRACK |%s" % (vignier_crack(cipheredText, range(1,6))))


