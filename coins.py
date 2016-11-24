COINVALS = {"red": 2,
            "corroded": 3,
            "shiny": 5,
            "concave": 7,
            "blue": 9}

EVAL_F = lambda a, b, c, d, e: a + b * ( c ** 2 ) + ( d ** 3 ) - e
TARGET = 399

def eval_coins( perm ):
    vals = map( lambda x: COINVALS[ x ], perm )
    return EVAL_F( *vals )

def gen_perms( items ):
    if len( items ) == 1: return [ items ]
    out = []
    for item in items:
        subperms = gen_perms( [ x for x in items if x != item ] )
        for perm in subperms:
            out.append( [ item ] + perm )
    return out

def get_combo():
    perms = gen_perms( COINVALS.keys() )
    for perm in perms:
        if eval_coins( perm ) == TARGET: return perm
    return None

if __name__ == "__main__":
    print get_combo()
