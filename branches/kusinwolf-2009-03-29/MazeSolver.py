graph = {}

def simplegraph():
    graph = {'start':{'visited': 0, 'reached': [], 'attached': ['p1']},
             'p1':{'visited': 0, 'reached': [],'attached': ['p2','p3']},
             'p2':{'visited': 0, 'reached': [],'attached': ['p1']},
             'p3':{'visited': 0, 'reached': [],'attached': ['p4','p6']},
             'p4':{'visited': 0, 'reached': [],'attached': ['p3','p5','p12']},
             'p5':{'visited': 0, 'reached': [],'attached':['p4','p13']},
             'p6':{'visited': 0, 'reached': [],'attached':['p3','p7','p9']},
             'p7':{'visited': 0, 'reached': [],'attached':['p6','p8']},
             'p8':{'visited': 0, 'reached': [],'attached':['p7']},
             'p9':{'visited': 0, 'reached': [],'attached':['p6','p10','p15']},
             'p10':{'visited': 0, 'reached': [], 'attached':['p9']},
             'p11':{'visited': 0, 'reached': [], 'attached':['p12']},
             'p12':{'visited': 0, 'reached': [], 'attached':['p4','p11','p14']},
             'p13':{'visited': 0, 'reached': [], 'attached':['p5']},
             'p14':{'visited': 0, 'reached': [],'attached':['p12','p16','p20']},
             'p15':{'visited': 0, 'reached': [],'attached':['p9','p16','p19']},
             'p16':{'visited': 0, 'reached': [],'attached':['p14','p15','p29']},
             'p17':{'visited': 0, 'reached': [],'attached':['p21']},
             'p18':{'visited': 0, 'reached': [],'attached':['p24',]},
             'p19':{'visited': 0, 'reached': [],'attached':['p15','p22','p25']},
             'p20':{'visited': 0, 'reached': [],'attached':['p14','p23','p26']},
             'p21':{'visited': 0, 'reached': [],'attached':['p17','p22']},
             'p22':{'visited': 0, 'reached': [],'attached':['p19','p21']},
             'p23':{'visited': 0, 'reached': [],'attached':['p20','p24']},
             'p24':{'visited': 0, 'reached': [],'attached':['p18', 'p23']},
             'p25':{'visited': 0, 'reached': [],'attached':['p28', 'p19']},
             'p26':{'visited': 0, 'reached': [],'attached':['p20','p30']},
             'p27':{'visited': 0, 'reached': [],'attached':['p28']},
             'p28':{'visited': 0, 'reached': [],'attached':['p27','p29', 'p25']},
             'p29':{'visited': 0, 'reached': [],'attached':['p28','p30', 'p16']},
             'p30':{'visited': 0, 'reached': [],'attached':['p26','p29','finish']},
             'finish':{'visited': 0, 'reached': [],'attached':['p30']}}

def aigraph(maxsize = 30, maxconnections = -1):
    #Use AI to build graph nodes and Maze
    pass

def solve_puzzle(start, finish):
    if start == finish:
        return route
    else:
        depth_first(0, start, finish)
    print_info(start, finish)
            
def depth_first (count, vertex, endvertex):
    count += 1

    if vertex != endvertex:   
        graph[vertex]['visited'] = 1
        if len(graph[vertex]['attached'] ) > 0:
            for subvertex in graph[vertex]['attached']:
                if graph[subvertex]['visited'] == 0: # If the point has not been visited, goto it
                    graph[vertex]['reached'].append((count, subvertex))
                    depth_first(count, subvertex, endvertex)
        else:
            graph[vertex]['visited'] = 0
    else:
        return "Finished Buwhahaha"
            
def print_info(vertex, finish):
    total = 0
    step = 0
    for b in [len(graph[node]['reached']) for node in graph]:
        total += b # Total amount of steps taken
    
    print "Total taken steps: %s" % total
    print "Starting position = %s" % vertex
    while( vertex != finish ):
        step = graph[vertex]['reached'][len(graph[vertex]['reached'])-1][0]
        vertex = graph[vertex]['reached'][len(graph[vertex]['reached'])-1][1]
        print "Step %s = %s" % (step,vertex)
    
'''    
graph['start']['visited']
'''