from sexp_plus_lexer import tokens
from symbol_table import SymbolTable, SemanticError
import ply.yacc as yacc

class SyntaxError(Exception):
    pass

def p_program(p):
    r"""
    Program : Statements
    """
    # allocate one slot per declared variable
    alloc = ["PUSHI 0" for i in p.parser.symbols.symbols()]
    p[0] = alloc + p[1]

def p_statements(p):
    r"""
    Statements : Statements Statement
               | Statement
    Statement : Declaration
              | Assignment
              | Print
              | Read
    """
    # simply concatenate instructions from each statement
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = p[1] + p[2]

def p_decl(p):
    r"""
    Declaration : "(" DECL ID ")"
    """
    p.parser.symbols.declare(p[3])
    # no code to generate, only affects symbol table, used elsewhere
    p[0] = []

def p_assign(p):
    r"""
    Assignment : "(" SET ID Expr ")"
    """
    var_info = p.parser.symbols.lookup(p[3])
    p.parser.symbols.initialize(p[3])
    # produce the value of the expression, and store it in the global region
    p[0] = p[4] + [f"STOREG {var_info['index']}"]

def p_print(p):
    r"""
    Print : "(" PRINT Expr ")"
    """
    # produce the value of the expression, and send it to the output
    p[0] = p[3] + [f"WRITEI"]

def p_read(p):
    r"""
    Read : "(" READ ID ")"
    """
    var_info = p.parser.symbols.lookup(p[3])
    p.parser.symbols.initialize(p[3])
    # read a string from the input, convert it to integer, and store it in the global region
    p[0] = [f'PUSHS "Value for {p[3]}: "', "WRITES", "READ", "ATOI", f"STOREG {var_info['index']}"]

def p_expr_bin(p):
    r"""
    Expr : "(" BinIntOp Expr Expr ")"
    """
    # push instructions for both operands, then apply the operation (post-order)
    p[0] = p[3] + p[4] + p[2]

def p_expr_if(p):
    r"""
    Expr : "(" IF Condition Expr Expr ")"
    """
    # create unique label identifiers
    label_id = p.parser.symbols.new_label()
    else_label = f"ELSE{label_id}"
    end_label = f"FI{label_id}"
    # push instructions for condition, jump depending on the result
    cond = p[3] + [f"JZ {else_label}"]
    # set the labels for the else branch and the end of the conditional
    branches = p[4] + [f"JUMP {end_label}", f"{else_label}:"] + p[5] + [f"{end_label}:"]
    p[0] = cond + branches

def p_expr_int(p):
    r"""
    Expr : INT
    """
    # push literal integer
    p[0] = [f"PUSHI {p[1]}"]

def p_expr_id(p):
    r"""
    Expr : ID
    """
    var_info = p.parser.symbols.lookup(p[1])
    if not var_info['initialized']:
      raise SemanticError(f"Uninitialized variable: {p[1]}")
    # push the value from the global region
    p[0] = [f"PUSHG {var_info['index']}"]

def p_cond_bin(p):
    r"""
    Condition : "(" BinCmpOp Expr Expr ")"
    """
    # push instructions for both operands, then apply the operation (post-order)
    p[0] = p[3] + p[4] + p[2]

def p_cond_bin_true(p):
    r"""
    Condition : TRUE
    """
    p[0] = ["PUSHI 1"]

def p_cond_bin_false(p):
    r"""
    Condition : FALSE
    """
    p[0] = ["PUSHI 0"]

def p_ops_add(p):
    r"""
    BinIntOp : ADD 
    """
    p[0] = ["ADD"]

def p_ops_sub(p):
    r"""
    BinIntOp : SUB
    """
    p[0] = ["SUB"]

def p_ops_mul(p):
    r"""
    BinIntOp : MUL 
    """
    p[0] = ["MUL"]

def p_ops_div(p):
    r"""
    BinIntOp : DIV 
    """
    p[0] = ["DIV"]

def p_ops_lt(p):
    r"""
    BinCmpOp : LT 
    """
    p[0] = ["INF"]

def p_ops_gt(p):
    r"""
    BinCmpOp : GT 
    """
    p[0] = ["SUP"]

def p_ops_eq(p):
    r"""
    BinCmpOp : EQ 
    """
    p[0] = ["EQUAL"]

def p_error(t):
    raise SyntaxError(f"Unexpected token: {t.type if t else '$'}")

parser = yacc.yacc()

def parse(text):
    parser.symbols = SymbolTable()
    code = parser.parse(text)
    return "\n".join(code)
