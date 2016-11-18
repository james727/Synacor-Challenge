from virtual_machine import synacor_machine, FILENAME

FILE_OUT = "dis.txt"

OP_CODES = { 0: ( "halt", 0 ),
            1:  ( "set ", 2 ),
            2:  ( "push", 1 ),
            3:  ( "pop ", 1 ),
            4:  ( "eq  ", 3 ),
            5:  ( "gt  ", 3 ),
            6:  ( "jmp ", 1 ),
            7:  ( "jt  ", 2 ),
            8:  ( "jf  ", 2 ),
            9:  ( "add ", 3 ),
            10: ( "mult", 3 ),
            11: ( "mod ", 3 ),
            12: ( "and ", 3 ),
            13: ( "or  ", 3 ),
            14: ( "not ", 2 ),
            15: ( "rmem", 2 ),
            16: ( "wmem", 2 ),
            17: ( "call", 1 ),
            18: ( "ret ", 0 ),
            19: ( "out ", 1 ),
            20: ( "in  ", 1 ),
            21: ( "noop", 0 ) }

def disassemble( memory ):
    distxt = ""
    memloc = 0
    dis_dict = {}
    while memloc < len( memory ):
        old_loc = memloc
        line, memloc = dis_loc( memory, memloc )
        distxt += line + "\n"
        dis_dict[ old_loc ] = line
    return dis_dict, distxt

def format_arg( arg ):
    return "%5d" % arg

def dis_loc( memory, loc ):
    code = memory[ loc ]
    while code not in OP_CODES:
        loc += 1
        code = memory[ loc ]
    op, args = OP_CODES[ code ]
    if code == 19:
        arg, new_loc = join_outs( memory, loc )
        line = format_arg( loc ) + " " + op + " " + arg
    else:
        arg_string = " ".join( [ format_arg(x) for x in memory[ loc + 1: loc + 1 + args ]])
        line = format_arg( loc ) + " " + op + " " + arg_string
        new_loc = loc + args + 1
    return line, new_loc

def join_outs( memory, loc ):
    if memory[ loc + 1 ] > 256:
        return format_arg( memory[ loc + 1 ] ), loc + 2
    out = ""
    while memory[ loc ] == 19 and memory[ loc + 1 ] < 256:
        out += chr( memory[ loc + 1 ] )
        loc += 2
    return out, loc

def write_to_disc( s ):
    with open( FILE_OUT, "w" ) as f:
        f.write( s )

def strip_zeroes( memory ):
    while memory[ -1 ] == 0:
        memory.pop( -1 )
    memory.append( 0 )
    return memory

if __name__ == "__main__":
    vm = synacor_machine()
    vm.load_file( FILENAME )
    memory = strip_zeroes( vm.memory )
    _, distxt = disassemble( memory )
    write_to_disc( distxt )
