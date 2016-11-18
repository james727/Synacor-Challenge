import sys, ast

def synacor_compile( in_file, out_file ):
    src = get_source( in_file )
    tree = ast.parse( src )
    binary = gen_binary( tree )
    write_to_file( binary, out_file )

def get_source( in_file ):
    with open( in_file, 'r' ) as f:
        return f.read().rstrip()

def gen_binary( tree ):
    # Compile AST using nodevisitor subclass
    C = Compiler()
    C.visit( tree )
    return C.bin

class AstVisitor( object ):
    def visit( self, node ):
        method_name = "visit_" + type( node ).__name__
        visitor = getattr( self, method_name, self.generic_visit )
        return visitor( node )

    def generic_visit( self, node ):
        raise Exception( "No visitor implemented for node of type " + type( node ).__name__ )

class Compiler( AstVisitor ):
    def __init__( self ):
        self.namespace = {} # map from variable names to memory addresses
        self.bin = [ 0 for _ in range( 2**15 ) ]
        self.current_addr = 0

    def visit_Module( self, node ):
        for tree_node in node.body:
            self.visit( tree_node )

    def visit_Expr( self, node ):
        self.visit( node.value )

    def visit_BinOp( self, node ):
        print "omg", ast.dump( node )
        if type( node.op ).__name__ == "Add":
            pass
        elif type( node.op ).__name__ == "Sub":
            new_bin = gen_push( )
        elif type( node.op ).__name__ == "Mult":
            pass
        elif type( node.op ).__name__ == "Div":
            pass


if __name__ == "__main__":
    in_file = sys.argv[ 1 ]
    out_file = sys.argv[ 2 ]
    #synacor_compile( in_file, out_file )
    src = get_source( in_file )
    tree = ast.parse( src )
    print ast.dump( tree )
    p = Compiler()
    p.visit( tree )
