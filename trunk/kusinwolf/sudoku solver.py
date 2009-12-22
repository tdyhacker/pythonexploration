# Created by Andrew Dorrycott
# Created: Dec 21st, 2009

def CanPlace(table, x, y):
    available = range(1, 10) # 1 - 9 left over
    contents = table[x][y]
    if contents != 0:
        return contents
    
    for x_pos in range(9):
        if (x_pos != y) and (table[x][x_pos] in available):
            available.remove(table[x][x_pos])
    
    for y_pos in range(9):
        if (y_pos != x) and (table[y_pos][y] in available):
            available.remove(table[y_pos][y])
    
    for q_num in WithinQuadrant(table, x, y):
        if q_num in available:
            available.remove(q_num)
    
    return available

def WithinQuadrant(table, x, y):
    
    q1 = range(3)
    q2 = range(3, 6)
    q3 = range(6, 9)
    
    # x_pos controls the row
    # y_pos controls the col
    if x in q1:
        if y in q1:
            return [table[x_pos][y_pos] for x_pos in q1 for y_pos in q1]
        elif y in q2:
            return [table[x_pos][y_pos] for x_pos in q1 for y_pos in q2]
        elif y in q3:
            return [table[x_pos][y_pos] for x_pos in q1 for y_pos in q3]
        
    elif x in q2:
        if y in q1:
            return [table[x_pos][y_pos] for x_pos in q2 for y_pos in q1]
        elif y in q2:
            return [table[x_pos][y_pos] for x_pos in q2 for y_pos in q2]
        elif y in q3:
            return [table[x_pos][y_pos] for x_pos in q2 for y_pos in q3]
        
    elif x in q3:
        if y in q1:
            return [table[x_pos][y_pos] for x_pos in q3 for y_pos in q1]
        elif y in q2:
            return [table[x_pos][y_pos] for x_pos in q3 for y_pos in q2]
        elif y in q3:
            return [table[x_pos][y_pos] for x_pos in q3 for y_pos in q3]

def FindAllSingles(table):
    for row in range(9):
        for col in range(9):
            r = CanPlace(table, row, col)
            if type(r) == list and len(r) == 1:
                print "Row: %d - Col: %d has %s" % (row + 1, col + 1, r)
                table[row][col] = r[0]
    print "Commited changes to table"

# x = row, y = col
#[0,1,2,3,4,5,6,7,8]
#[1,...]
#[2,...]
#[3,...]
#[4,...]
#[5,...]
#[6,...]
#[7,...]
#[8,...]
# Replace this table with what the Sudoku table looks like
table = [
[0,2,0,3,1,0,0,0,0],
[0,5,1,0,0,0,4,0,0],
[8,4,0,5,0,9,2,0,0],
[0,0,0,0,0,0,0,3,8],
[4,0,5,0,0,0,0,0,0],
[0,0,0,0,0,0,1,0,7],
[7,8,9,0,0,0,0,0,0],
[3,6,4,0,8,0,0,1,0],
[5,1,2,0,0,0,0,9,0],
]

FindAllSingles(talbe)