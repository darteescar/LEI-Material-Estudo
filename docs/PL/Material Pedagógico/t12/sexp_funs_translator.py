from sexp_lexer import tokens
from symbol_table_funs import SymbolTable, SemanticError
import ply.yacc as yacc

class SyntaxError(Exception):
    pass

def p_program(p):
    r"""
    Program : Statements
    """
    # allocate one slot per declared variable
    alloc = ["PUSHI 0" for i in p.parser.symbols.symbols()]
    # get the code for all the defined functions, put it at the end
    funs = [l for f in (p.parser.symbols.funs()) for l in f["code"]]
    p[0] = alloc + p[1] + ["STOP"] + funs

def p_statements(p):
    r"""
    Statements : Statements Statement
               | Statement
    Statement : Declaration
              | Assignment
              | Conditional
              | Loop
              | Definition
              | Print
              | Read
              | Return
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
    # decide if local context
    if p.parser.symbols.local():
      p.parser.symbols.declare_local(p[3])
    else:
      p.parser.symbols.declare_global(p[3])

    # no code to generate, only affects symbol table
    p[0] = []

def p_assign(p):
    r"""
    Assignment : "(" SET ID Expr ")"
    """
    var_info = p.parser.symbols.lookup(p[3])
    p.parser.symbols.initialize(p[3])
    # produce the value of the expression, and store it
    # test variable scope to decide on global or local region
    p[0] = p[4] + [f"STORE{"G" if var_info['global'] else "L"} {var_info['index']}"]

def p_conditional(p):
    r"""
    Conditional : "(" IF Condition "(" Statements ")" "(" Statements ")" ")"
    """
    # create unique label identifiers
    label_id = p.parser.symbols.new_label()
    else_label = f"ELSE{label_id}"
    end_label = f"FI{label_id}"
    # push instructions for condition, jump depending on the result
    cond = p[3] + [f"JZ {else_label}"]
    # set the labels for the else branch and the end of the conditional
    branches = p[5] + [f"JUMP {end_label}", f"{else_label}:"] + p[8] + [f"{end_label}:"]
    p[0] = cond + branches

def p_loop(p):
    r"""
    Loop : "(" WHILE Condition "(" Statements ")" ")"
    """
    # create unique label identifiers
    label_id = p.parser.symbols.new_label()
    while_label = f"WHILE{label_id}"
    end_label = f"ELIHW{label_id}"
    # set the loop start label, push instructions for condition, jump to end
    cond = [f"{while_label}:"] + p[3] + [f"JZ {end_label}"]
    # push the body instructions, jump back to beginning, set end label
    branches = p[5] + [f"JUMP {while_label}", f"{end_label}:"]
    p[0] = cond + branches

def p_definition(p):
    r"""
    Definition : "(" FUN id_args "(" Statements ")" ")"
    """
    # allocate memory for the local variables
    alloc = ["PUSHI 0" for i in p.parser.symbols.symbols()]
    # set the function start label, allocate variables, push function body
    code = [f"{p[3]}:"] + alloc + p[5]
    # register the code, to appear at the end
    p.parser.symbols.register(p[3],code)
    # pop the function context
    p.parser.symbols.pop()
    # no code to generate, only affects symbol table
    p[0] = []

def p_idargs(p):
    r"""
    id_args : ID "(" Arguments ")"
    """
    # dummy grammar rule to guarantee function scope created before body
    # declare the function and arguments
    p.parser.symbols.define(p[1],p[3])
    p[0] = p[1]

def p_return(p):
    r"""
    Return : "(" RETURN Expr ")"
    """
    # special variable entry to identify return index
    var_info = p.parser.symbols.lookup(None)
    p[0] = p[3] + [f"STOREL {var_info['index']}", "RETURN"]

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
    # read a string from the input, convert it to integer, and store it in appropriate region
    p[0] = [f'PUSHS "Value for {p[3]}: "', "WRITES", "READ", "ATOI", f"STORE{"G" if var_info['global'] else "L"} {var_info['index']}"]

def p_expr_bin(p):
    r"""
    Expr : "(" BinIntOp Expr Expr ")"
    """
    # push instructions for both operands, then apply the operation (post-order)
    p[0] = p[3] + p[4] + p[2]

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
    # push the value from the appropriate region
    p[0] = [f"PUSH{"G" if var_info['global'] else "L"} {var_info['index']}"]

def p_expr_call(p):
    r"""
    Expr : "(" ID Exprs ")"
    """
    args = p.parser.symbols.lookup_fun(p[2])["args"]
    # reserve space for return value, push argument values, call function, pop arguments leaving return value on top
    p[0] = ["PUSHI 0"] + p[3] + [f"PUSHA {p[2]}", "CALL", f"POP {len(args)}"]

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

def p_exprs(p):
    r"""
    Exprs : Exprs Expr
          |
    """
    if len(p) == 1:
      p[0] = []
    else:
      p[0] = p[1] + p[2]

def p_args(p):
    r"""
    Arguments : Arguments ID
              |
    """
    if len(p) == 1:
      p[0] = []
    else:
      p[0] = p[1] + [p[2]]

def p_error(t):
    raise SyntaxError(f"Unexpected token: {t.type if t else '$'}")

parser = yacc.yacc()

def parse(text):
    parser.symbols = SymbolTable()
    code = parser.parse(text)
    return "\n".join(code)
