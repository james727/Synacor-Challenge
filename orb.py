G = [ [ "22", "-", "9",  "*"  ],
      [ "+",  "4", "-",  "18" ],
      [ "4",  "*", "11", "*"  ],
      [ "*",  "8", "-",  "1"  ] ]

START_NODE = ( 0, 0 )
END_NODE = ( 3, 3 )


def get_neighbors( node ):
    x, y = node
    deltas = [ (1, 0), (-1, 0), (0, 1), (0, -1) ]
    potential_neighbors = [ (x + xd, y + yd) for xd, yd in deltas ]
    neighbors = filter( lambda x: 0 <= x[0] <= 3 and 0 <= x[1] <= 3, potential_neighbors )
    neighbors = filter( lambda x: x != (0,0), neighbors)
    return neighbors

def gen_expression( nodes ):
    val = lambda x: G[ x[ 0 ] ][ x[ 1 ] ]
    return " ".join( map( val, nodes ) )

def remove_mults( v ):
    print v
    while True:
        try:
            i = v.index( "*" )
            x = int( v[ i - 1 ] )
            y = int( v[ i + 1 ] )
            val = x * y
            v[ i ] = str( val )
            v.pop( i + 1 )
            v.pop( i - 1 )
        except:
            break
    return v

def eval_expr( v ):
    total = int( v.pop( 0 ) )
    while len( v ) > 0:
        op = v.pop( 0 )
        num = int( v.pop( 0 ) )
        if op == "+":
            total += num
        elif op == "*":
            total *= num
        else:
            total -= num
    return total

def eval_expression( expr ):
    e = expr.split()
    #e = remove_mults( e )
    num = eval_expr( e )
    return num

def test_eval():
    expression = "2 + 3 * 5 - 4"
    assert eval_expression( expression ) == 13

def gen_step_longer_paths( path ):
    end = path[ -1 ]
    neighbors = get_neighbors( end )
    return [ path + [ neighbor ]  for neighbor in neighbors ]

def gen_next_level_paths( paths ):
    out = []
    for p in paths:
        if p[ -1 ] != ( 3, 3 ):
            out += gen_step_longer_paths( p )
    return out

def search_paths( paths ):
    for path in paths:
        if path[ -1 ] == ( 3, 3 ):
            expr = gen_expression( path )
            val = eval_expression( expr )
            if val == 30:
                return path
    return False

if __name__ == "__main__":
    length = 1
    paths = [ [ ( 0, 0 ) ] ]

    while True:
        paths = gen_next_level_paths( paths )
        length += 1
        if length > 6 and length % 2 == 1:
            target_path = search_paths( paths )
            if target_path:
                print "Path found"
                print target_path
                print gen_expression( target_path )
                break
