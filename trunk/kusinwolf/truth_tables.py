
truth_table = {}
truth_table['order'] = ['P', 'Q', 'R', 'Z', 'W', 'D']

value = True

# Assign the columns automatically
for col in truth_table['order']:
    truth_table[col] = []
    
    while len(truth_table[col]) < pow(2, len(truth_table['order'])):
        for var in range(pow(2, len(truth_table['order']) - (truth_table['order'].index(col) + 1) ) ):
            truth_table[col].append(value)
        value = value ^ True # Similar to an xor operator without writing my own
    
    value = True