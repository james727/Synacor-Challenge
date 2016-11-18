import virtual_machine
import disassembler

class synacor_debugger( object ):
    def __init__( self ):
        self.vm = virtual_machine.synacor_machine()
        self.vm.load_file( virtual_machine.FILENAME )
        self.dis_dict, _ = disassembler.disassemble( self.vm.memory )
        self.current_loc = 0

    def dump( self ):
        # dump register contents
        registers = range( 32768, 32768 + 8 )
        for i, reg in enumerate( registers ):
            val = self.vm.registers[ reg ]
            print "Register " + str( i + 1 ) + " (" + str( reg ) + "): " + str( val )

    def asm( self, num_lines = 5 ):
        # print current assembly
        line_no = self.current_loc
        lines_printed = 0
        while lines_printed < num_lines:
            current_line = self.dis_dict[ line_no ]
            print current_line
            lines_printed += 1
            line_no += 1
            while line_no not in self.dis_dict: line_no += 1

    def step( self, num_lines = 1 ):
        # Perform num_lines operations
        lines_run = 0
        while lines_run < num_lines:
            instruction = self.vm.memory[ self.current_loc ]
            if instruction == 0: break
            self.current_loc = self.vm.handlers[ instruction ]( self.current_loc )
            lines_run += 1

    def steptil( self, dest ):
        # run until we hit memory address dest
        while self.current_loc != dest:
            self.step()

if __name__ == "__main__":
    db = synacor_debugger()
    db.print_state()
    db.print_asm()
    db.step( 230 )
