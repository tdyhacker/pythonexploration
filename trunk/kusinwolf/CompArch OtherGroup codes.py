it = 1
if it == 0:
    d = {
    'a': "0010", "h": "0011", "i": "0000",
    "n": "00011", "p": "111", "sp": "010",
    "u": "000100", "l": "100", "c": "1100",
    "e": "1101", "k": "0110", "s": "0111",
    "t": "0001010", "etx": "00010111", "stx": "00010110",
    "y": "10100", "g": "10101", "o": "1011",

    "0010": "a", "0011": "h", "0000": "i",
    "00011": "n", "111": "p", "010": "sp",
    "000100": "u", "100": "l", "1100": "c",
    "1101": "e", "0110": "k", "0111": "s",
    "0001010": "t", "00010111": "etx", "00010110": "stx",
    "10100": "y", "10101": "g", "1011": "o",

    '0000': "0", '0001': "1", '0010': "2", '0011': "3",
    '0100': "4", '0101': "5", '0110': "6", '0111': "7",
    '1000': "8", '1001': "9", '1010': "A", '1011': "B",
    '1100': "C", '1101': "D", '1110': "E", '1111': "F",

    "0": '0000', "1": '0001', "2": '0010', "3": '0011',
    "4": '0100', "5": '0101', "6": '0110', "7": '0111',
    "8": '1000', "9": '1001', "A": '1010', "B": '1011',
    "C": '1100', "D": '1101', "E": '1110', "F": '1111'
    }

    con = {
    "0010": "a", "0011": "h", "0000": "i",
    "00011": "n", "111": "p", "010": "sp",
    "000100": "u", "100": "l", "1100": "c",
    "1101": "e", "0110": "k", "0111": "s",
    "0001010": "t", "00010111": "etx", "00010110": "stx",
    "10100": "y", "10101": "g", "1011": "o",
    }

    z = ""

    for hx in ["1","6","B","B","A","C","8","8","5","2","B","B","0","2","3","8","A","7","1","7"]:
        print d[hx], 
        z = z + d[hx]

    print "\n"
    t = ""
    for val in z:
        if t in con.keys():
            print con[t],
            print t
            t = val
        else:
            t += val
elif it == 1:
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
    text = "rat trap"

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

            hamming += ":"
            
            hammingcon = ""
            thamming = ""
            t = ""
    print "Hammming: %s" % hamming
        

    
