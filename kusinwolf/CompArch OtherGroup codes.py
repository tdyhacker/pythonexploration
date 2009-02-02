from random import Random

it = 0
if it == 0:
    treevalues = {
    'a': "0010", "h": "0011", "i": "0000",
    "n": "00011", "p": "111", "sp": "010",
    "u": "000100", "l": "100", "c": "1100",
    "e": "1101", "k": "0110", "s": "0111",
    "t": "0001010", "etx": "00010111", "stx": "00010110",
    "y": "10100", "g": "10101", "o": "1011",
    }
    keys = treevalues.keys()[:]
    for info in keys:
        treevalues[treevalues[info]] = info

    hexvalues = {
    '0000': "0", '0001': "1", '0010': "2", '0011': "3",
    '0100': "4", '0101': "5", '0110': "6", '0111': "7",
    '1000': "8", '1001': "9", '1010': "A", '1011': "B",
    '1100': "C", '1101': "D", '1110': "E", '1111': "F",
    "0": '0000', "1": '0001', "2": '0010', "3": '0011',
    "4": '0100', "5": '0101', "6": '0110', "7": '0111',
    "8": '1000', "9": '1001', "A": '1010', "B": '1011',
    "C": '1100', "D": '1101', "E": '1110', "F": '1111'
    }
    
elif it == 1:
    # Computer Architicture Class, our Huffman tree codes
    treevalues = {
        "etx": "011011", "e": "11011", "stx": "011010",
        "v": "11010", "s": "01100", "i": "00111", "l": "00110",
        "c": "00001", "r": "00000", "p": "1100", "w": "0111",
        "a": "0101", "u": "0100", "n": "0010", "o": "0001",
        "z": "111", "t": "101", "sp": "100"
    }
    keys = treevalues.keys()[:]
    for info in keys:
        treevalues[treevalues[info]] = info

    # Binary to Hex & Hex to Binary
    hexvalues = {
        '0000': "0", '0001': "1", '0010': "2", '0011': "3",
        '0100': "4", '0101': "5", '0110': "6", '0111': "7",
        '1000': "8", '1001': "9", '1010': "A", '1011': "B",
        '1100': "C", '1101': "D", '1110': "E", '1111': "F",
        "0": '0000', "1": '0001', "2": '0010', "3": '0011',
        "4": '0100', "5": '0101', "6": '0110', "7": '0111',
        "8": '1000', "9": '1001', "A": '1010', "B": '1011',
        "C": '1100', "D": '1101', "E": '1110', "F": '1111'
    }

binary = ""
bTohex = ""
t = ""
hamming = ""
thamming = ""
hammingcon = ""
stream = []
#text = "lol pwnsauce"
#text = "rat trap"
text =  "look at locusts"

stream.append("stx")
for char in text:
    if char == " ":
        stream.append("sp")
    else:
        stream.append(char)

stream.append("etx")

for letter in stream:
    binary += treevalues[letter]

hsize = 0
n = 0
for size in range(0,len(binary),4):
    for small in range(4):
        if not ((size + small) > len(binary) - 1 ):
            t += binary[size+small]
        else:
            n += 1
            t += "0"
    hsize += 1
    bTohex += hexvalues[t]
    t = ""
    if hsize % 2 == 0 and size + 4 < len(binary):
        bTohex += ":"
for amount in range(n):
    binary += "0"
if hsize % 2 == 1:
    bTohex += "0"
    binary += "0000"

t = binary
binary = ""
hsize = 0
for nibble in t:
    binary += nibble
    hsize += 1
    if hsize % 4 == 0:
        binary += " "

print "Binary: %s" % binary
print text, "= %s" % bTohex

t = ""
for byte in bTohex:
    if byte != ":":
        t += byte
    if len(t) == 2:
        thamming += hexvalues[t[0]] + hexvalues[t[1]]
        #position =   0  123  4567
        #size     = 1234,5678,9012
        #pow      = 12 4    8
        
        # Check bet, 1
        if (int(thamming[0]) + int(thamming[1]) + int(thamming[3]) + int(thamming[4]) + int(thamming[6])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"

        # Check bet, 2
        if (int(thamming[0]) + int(thamming[2]) + int(thamming[3]) + int(thamming[5]) + int(thamming[6])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"
            
        hammingcon += thamming[0]

        # Check bet, 4
        if (int(thamming[1]) + int(thamming[2]) + int(thamming[3]) + int(thamming[7])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"

        hammingcon += thamming[1] + thamming[2] + thamming[3]

        # Check bet, 8
        if (int(thamming[4]) + int(thamming[5]) + int(thamming[6]) + int(thamming[7])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"

        hammingcon += thamming[4] + thamming[5] + thamming[6] + thamming[7]

        hamming += hexvalues[hammingcon[0:4]] + hexvalues[hammingcon[4:8]] + hexvalues[hammingcon[8:]]

        if len(hamming.split(":")) != len(bTohex.split(":")):
            hamming += ":"
        
        hammingcon = ""
        thamming = ""
        t = ""
        
correctHamming = hamming
hamming = ""
hammingcon = ""
thamming = ""
t = ""
changed = [0.0,1.0]
def mightChange(value):
    if (Random().random() < (changed[0] /changed[1])) and ((changed[0] /changed[1]) > 0.5):
        if value == "0":
            value = "1"
        else:
            value = "0"
        changed[1] += 1
    else:
        changed[0] += 1

    return value
    
for byte in bTohex:
    if byte != ":":
        t += byte
    if len(t) == 2:
        thamming += hexvalues[t[0]] + hexvalues[t[1]]
        #position =   0  123  4567
        #size     = 1234,5678,9012
        #pow      = 12 4    8
        
        # Check bet, 1
        if (int(thamming[0]) + int(thamming[1]) + int(thamming[3]) + int(thamming[4]) + int(thamming[6])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"

        # Check bet, 2
        if (int(thamming[0]) + int(thamming[2]) + int(thamming[3]) + int(thamming[5]) + int(thamming[6])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"
            
        hammingcon += thamming[0]

        # Check bet, 4
        if (int(thamming[1]) + int(thamming[2]) + int(thamming[3]) + int(thamming[7])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"

        hammingcon += thamming[1] + thamming[2] + thamming[3]

        # Check bet, 8
        if (int(thamming[4]) + int(thamming[5]) + int(thamming[6]) + int(thamming[7])) % 2 == 0:
            hammingcon += "0"
        else:
            hammingcon += "1"

        hammingcon += thamming[4] + thamming[5] + thamming[6] + thamming[7]

        loc = int(round(Random().random() * (len(hammingcon) - 1)))
        translate = []
        for char in hammingcon:
            translate.append(char)
        translate[loc] = mightChange(hammingcon[loc])
        hammingcon = ""
        for char in translate:
            hammingcon += char

        hamming += hexvalues[hammingcon[0:4]] + hexvalues[hammingcon[4:8]] + hexvalues[hammingcon[8:]]
        if len(hamming.split(":")) != len(bTohex.split(":")):
            hamming += ":"
        
        hammingcon = ""
        thamming = ""
        t = ""

print "Safe Hammming:    %s" % correctHamming
print "Changed Hammming: %s" % hamming

"566:A37:08C:618:8B2:AB7:292:078:257:4B7" # The correct string
"526:A37:0CC:618:8B2:A37:212:078:257:437" # What they gave us
"0-40:000:040:000:000:0-80:0-80:000:000:0-80" # The differences
encodedHamminghex = hamming or "" #"566:A37:08C:618:8B2:AB7:292:078:257:4B7"
decodehammingpart = []
decodedhamming = ""
errors = []
triplet = 0
for hamhex in encodedHamminghex:

    if hamhex != ":":
        for hh in hexvalues[hamhex]:
            decodehammingpart.append( hh )
        triplet += 1
    
        if triplet % 3 == 0:
            #position =   0  123  4567
            #size     = 1234,5678,9012
            #pow      = 12 4    8

            # This checks 3, 5, 7, 9, 11
            # Check bet, 1
            if not (int(decodehammingpart[0]) + int(decodehammingpart[2]) + int(decodehammingpart[4]) + int(decodehammingpart[6]) + int(decodehammingpart[8]) + int(decodehammingpart[10])) % 2 == 0:
                errors.append(1)

            # This checks 3, 6, 7, 10, 11
            # Check bet, 2
            if not (int(decodehammingpart[1]) + int(decodehammingpart[2]) + int(decodehammingpart[5]) + int(decodehammingpart[6]) + int(decodehammingpart[9]) + int(decodehammingpart[10])) % 2 == 0:
                errors.append(2)

            # Checks 5, 6, 7, 12
            # Check bet, 4
            if not (int(decodehammingpart[3]) + int(decodehammingpart[4]) + int(decodehammingpart[5]) + int(decodehammingpart[6]) + int(decodehammingpart[11])) % 2 == 0:
                errors.append(4)

            # Checks 9, 10, 11, 12
            # Check bet, 8
            if not (int(decodehammingpart[7]) + int(decodehammingpart[8]) + int(decodehammingpart[9]) + int(decodehammingpart[10]) + int(decodehammingpart[11])) % 2 == 0:
                errors.append(8)

            if sum(errors) > 12:
                print "Multiple Bit Error, unrecoverable data"
            if errors:
                if decodehammingpart[sum(errors) - 1] == "0":
                    decodehammingpart[sum(errors) - 1] = "1"
                else:
                    decodehammingpart[sum(errors) - 1] = "0"
                errors = []
                
            t = decodehammingpart[2] + decodehammingpart[4] + decodehammingpart[5] + decodehammingpart[6]
            decodedhamming += hexvalues[t]
            t = ""

            t = decodehammingpart[8] + decodehammingpart[9] + decodehammingpart[10] + decodehammingpart[11]
            decodedhamming += hexvalues[t]
            t = ""
            
            decodehammingpart = []

            decodedhamming += ":"

print "Decoded and Corrected: %s" % decodedhamming

encodedhuffmanhex = decodedhamming
decodedbinary = ""
decodetext = []
decodedtext = ""

for hh in encodedhuffmanhex:
    if hh != ":":
        decodedbinary += hexvalues[hh]

t = ""
for bi in decodedbinary:
    t += bi
    if t in treevalues.keys():
        if decodetext:
            if decodetext[len(decodetext) - 1] != 'etx':
                decodetext.append(treevalues[t])
                t = ""
        else:
            decodetext.append(treevalues[t])
            t = ""
if decodetext[0] == "stx":
    for char in decodetext:
        if char != "stx" and char != "etx":
            if char != "sp":
                decodedtext += char
            else:
                decodedtext += " "
else:
    print "Decoding error, no STX"
    
print "Decoded text: %s" % decodedtext
