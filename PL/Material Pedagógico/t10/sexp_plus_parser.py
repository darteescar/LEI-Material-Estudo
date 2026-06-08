import ply.yacc as yacc
from sexp_plus_lexer import tokens
from symbol_table import SymbolTable, SemanticError

class SyntaxError(Exception):
    pass

def p_program(p):
    r"""
    Program : Statements
    Statements : Statements Statement
               | Statement
    Statement : Assignment
              | VarDeclaration
              | FunDeclaration
              | Print
    """

def p_decl(p):
    r"""
    VarDeclaration : "(" DECL ID ")"
    """
    # declare the variable
    p.parser.symbols.declare_var(p[3])

# will only be applied after Parameters and Expr are built, by the local context must created before
def p_fun(p):
    r"""
    FunDeclaration : "(" fun ID "(" Parameters ")" Expr ")"
    """
    # declare the variable
    p.parser.symbols.pop()
    p.parser.symbols.declare_fun(p[3], p[5])

# a "dummy" production that allows the creation of the function context
def p_fun_aux(p): 
    r"""
    fun : FUN
    """
    p.parser.symbols.push()

def p_assign(p):
    r"""
    Assignment : "(" SET ID Expr ")"
    """
    # mark variable as initialized
    p.parser.symbols.initialize(p[3])

def p_print(p):
    r"""
    Print : "(" PRINT Expr ")"
    """

def p_expr(p):
    r"""
    Expr : "(" BinIntOp Expr Expr ")"
         | INT
    """

def p_expr_call(p):
    r"""
    Expr : "(" ID Arguments ")"
    """
    if p.parser.symbols.lookup_fun(p[2]) != p[3]:
        raise SemanticError(f"Invalid number of arguments: {p[3]}")

def p_expr_ID(p):
    r"""
    Expr : ID
    """
    # test if declared and initialized in symbol table
    if not p.parser.symbols.lookup_var(p[1]):
        raise SemanticError(f"Uninitialized variable: {p[1]}")

def p_ops(p):
  r"""
  BinIntOp : ADD
           | SUB
           | MUL
           | DIV
  """

def p_params(p):
  r"""
  Parameters : Parameters ID
             |
  """
  if len(p) > 1:
    p.parser.symbols.declare_var(p[2])
    p.parser.symbols.initialize(p[2])
    p[0] = 1 + p[1]
  else:
    p[0] = 0

def p_args(p):
  r"""
  Arguments : Arguments Expr
            |
  """
  if len(p) > 1:
    p[0] = 1 + p[1]
  else:
    p[0] = 0

def p_error(t):
    raise SyntaxError(f"Unexpected token: {t.type if t else '$'}")

parser = yacc.yacc()

def parse(text):
    # initialize an empty symbol table
    parser.symbols = SymbolTable()
    parser.parse(text)
