def build_cache( z ):
    # build cache for f( 3, y, z )

    d = {}
    mod = 32768

    def f( x, y, z):
        x0, y0, z0 = x, y, z
        if ( x, y ) in d: return d[ ( x, y ) ]
        elif x == 2:
            return ( ( 2 + y ) * z + y + 1 ) % 32768
        elif y == 0 and x == 3:
            ret = ( ( z + 1 ) ** 2 + z ) % 32768
        else:
            ret = f( x - 1, f( x, y - 1, z ), z )
        d[ ( x, y ) ] = ret
        return ret

    for y in range( 0, mod ):
        x = 3
        _ = f( x, y, z )
    return d

def check_z_value( z ):
    # eval f( 4, 1, z )
    cache = build_cache( z )
    f1 = cache[ ( 3, z ) ]
    return cache[ ( 3, f1 ) ]

for i in range( 32768 ):
    print "Checking", i
    ret = check_z_value( i )
    if ret == 6:
        print "FOUND SOLN FOR Z =", i
        break
