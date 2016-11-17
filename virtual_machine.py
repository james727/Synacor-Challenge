from struct import unpack
import sys, time

FILENAME = "challenge.bin"

class synacor_machine( object ):
    def __init__( self ):
        self.memory = [ 0 ] * ( 2 ** 15 )
        self.registers = { i: 0 for i in range( 32768, 32776 ) }
        self.stack = []
        self.handlers = {   1: self.handle_1,
                            2:  self.handle_2,
                            3:  self.handle_3,
                            4:  self.handle_4,
                            5:  self.handle_5,
                            6:  self.handle_6,
                            7:  self.handle_7,
                            8:  self.handle_8,
                            9:  self.handle_9,
                            10: self.handle_10,
                            11: self.handle_11,
                            12: self.handle_12,
                            13: self.handle_13,
                            14: self.handle_14,
                            15: self.handle_15,
                            16: self.handle_16,
                            17: self.handle_17,
                            18: self.handle_18,
                            19: self.handle_19,
                            20: self.handle_20,
                            21: self.handle_21 }

    def run( self ):
        current_address = 0
        while True:
            current_instruction = self.memory[ current_address ]
            if current_instruction == 0: break
            current_address = self.handlers[ current_instruction ]( current_address )

    @staticmethod
    def read_file( filename ):
        file_array = []
        with open( filename, 'rb' ) as f:
            while True:
                try:
                    file_array.append( unpack( "<H", f.read( 2 ) )[ 0 ] )
                except:
                    break
            return file_array

    def load_file( self, filename ):
        for index, command in enumerate( self.read_file( filename ) ):
            self.memory[ index ] = command

    def load_test_file( self ):
        filenums = [ 9, 32768, 32769, 4, 19, 32768 ]
        for index, num in enumerate( filenums ):
            self.memory[ index ] = num

    def getnum( self, mem_address ):
        val = self.memory[ mem_address ]
        if val < 32768:
            return val
        else:
            return self.registers[ val ]

    def getnumfromaddr( self, addr ):
        if addr < 32768:
            return self.memory[ addr ]
        else:
            return self.registers[ addr ]

    def setmem( self, address_mem_index, val ):
        address = self.memory[ address_mem_index ]
        if address < 32768:
            self.memory[ address ] = val
        else:
            self.registers[ address ] = val

    def handle_1( self, address ):
        # set
        val = self.getnum( address + 2 )
        self.setmem( address + 1, val )
        return address + 3

    def handle_2( self, address ):
        # push
        val = self.getnum( address + 1 )
        self.stack.append( val )
        return address + 2

    def handle_3( self, address ):
        # pop
        if len( self.stack ) == 0:
            raise Exception( "Empty Stack" )
        else:
            val = self.stack.pop( -1 )
            self.setmem( address + 1, val )
            return address + 2

    def handle_4( self, address ):
        # eq
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, 1 if b == c else 0 )
        return address + 4

    def handle_5( self, address ):
        # gt
        register = self.memory[ address + 1 ]
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, 1 if b > c else 0 )
        return address + 4

    def handle_6( self, address ):
        # jmp
        a = self.getnum( address + 1 )
        return a

    def handle_7( self, address ):
        # jt
        a, b = self.getnum( address + 1 ), self.getnum( address + 2 )
        if a != 0:
            return b
        return address + 3

    def handle_8( self, address ):
        # jf
        a, b = self.getnum( address + 1 ), self.getnum( address + 2 )
        if a == 0:
            return b
        return address + 3

    def handle_9( self, address ):
        # add
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, ( b + c ) % 32768 )
        return address + 4

    def handle_10( self, address ):
        # mult
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, ( b * c ) % 32768 )
        return address + 4

    def handle_11( self, address ):
        # mod
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, ( b % c ) % 32768 )
        return address + 4

    def handle_12( self, address ):
        # and
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, ( b & c ) % 32768 )
        return address + 4

    def handle_13( self, address ):
        # or
        b, c = self.getnum( address + 2 ), self.getnum( address + 3 )
        self.setmem( address + 1, ( b | c ) % 32768 )
        return address + 4

    def handle_14( self, address ):
        # not
        b = self.getnum( address + 2 )
        self.setmem( address + 1, ( ~b ) & ( 2 ** 15 - 1 ) )
        return address + 3

    def handle_15( self, address ):
        # rmem
        addr = self.memory[ address + 2 ]
        val = self.memory[ self.registers[ addr ] ] if addr >= 32768 else self.memory[ addr ]
        self.setmem( address + 1, val )
        return address + 3

    def handle_16( self, address ):
        # wmem
        target = self.getnum( address + 1 )
        num = self.getnum( address + 2 )
        self.memory[ target ] = num
        return address + 3

    def handle_17( self, address ):
        # call
        self.stack.append( address + 2 )
        func_addr = self.getnum( address + 1 )
        return func_addr

    def handle_18( self, address ):
        # ret
        if len( self.stack ) == 0: return -1
        ret_addr = self.stack.pop( -1 )
        return ret_addr

    def handle_19( self, address ):
        # out
        target = self.getnum( address + 1 )
        char = chr( target )
        sys.stdout.write( "%s" % char )
        sys.stdout.flush()
        time.sleep(.005)
        return address + 2

    def handle_20( self, address ):
        # in
        a = sys.stdin.read( 1 )
        num = ord( a )
        self.setmem( address + 1, num )
        return address + 2

    def handle_21( self, address ):
        return address + 1

if __name__ == "__main__":
    mach = synacor_machine()
    mach.load_file( FILENAME )
    mach.run()
