from sexp_lexer import tokens
from symbol_table_arrays import SymbolTable, SemanticError
import ply.yacc as yacc

class SyntaxError(Exception):
    pass

def p_program(p):
    r"""
    Program : Statements
    """
    # allocate one slot per declared variable
    alloc = [f"PUSHN {len(p.parser.symbols.symbols())}"]
    # get the code for all the defined functions, put it at the end
    p[0] = alloc + p[1] + ["STOP"] 

def p_statements(p):
    r"""
    Statements : Statements Statement
               | Statement
    Statement : Declaration
              | Assignment
              | Conditional
              | Loop
              | Print
              | Read
    """
    # simply concatenate instructions from each statement
    if len(p) == 2:
      p[0] = p[1]
    else:
      p[0] = p[1] + p[2]

def p_decl_int(p):
    r"""
    Declaration : "(" DECL ID ")"
    """
    p.parser.symbols.declare(p[3])
    
    # no code to generate, only affects symbol table
    p[0] = []

def p_decl_array(p):
    r"""
    Declaration : "(" DECL ID Expr ")"
    """
    p.parser.symbols.declare(p[3], True)
    var_info = p.parser.symbols.lookup(p[3])

    # calculate size, allocate memory, store address    
    p[0] = p[4] + ["ALLOCN", f"STOREG {var_info['index']}"]

def p_assign_id(p):
    r"""
    Assignment : "(" SET ID Expr ")"
    """
    var_info = p.parser.symbols.lookup(p[3])
    if var_info["array"]:
        raise SemanticError(f"Invalid type, expected int: {p[3]}")

    p.parser.symbols.initialize(p[3])
    # produce the value of the expression, and store it in global region
    p[0] = p[4] + [f"STOREG {var_info['index']}"]

def p_assign_array(p):
    r"""
    Assignment : "(" SET ID "[" Expr "]" Expr ")"
    """
    var_info = p.parser.symbols.lookup(p[3])
    if not var_info["array"]:
        raise SemanticError(f"Invalid type, expected array: {p[3]}")

    p.parser.symbols.initialize(p[3])
    
    # with dynamic allocation, we don't know at static time which blocks of the struct to mark as initialized

    # produce the value of the expression, the offset, and store it in heap
    p[0] = [f"PUSHG {var_info['index']}"] + p[5] + p[7] + [f"STOREN"]

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

def p_print(p):
    r"""
    Print : "(" PRINT Expr ")"
    """
    # produce the value of the expression, and send it to the output
    p[0] = p[3] + [f"WRITEI"]

def p_read_id(p):
    r"""
    Read : "(" READ ID ")"
    """
    var_info = p.parser.symbols.lookup(p[3])
    if var_info["array"]:
        raise SemanticError(f"Invalid type, expected int: {p[3]}")

    p.parser.symbols.initialize(p[3])
    # read a string from the input, convert it to integer, and store it in global region
    p[0] = [f'PUSHS "Value for {p[3]}: "', "WRITES", "READ", "ATOI", f"STOREG {var_info['index']}"]

def p_read_array(p):
    r"""
    Read : "(" READ ID "[" Expr "]" ")"
    """
    var_info = p.parser.symbols.lookup(p[3]) 
    if not var_info["array"]:
        raise SemanticError(f"Invalid type, expected array: {p[3]}")

    p.parser.symbols.initialize(p[3])
    
    # with dynamic allocation, we don't know at static time which blocks of the struct to mark as initialized

    # read a string from the input, convert it to integer, calculate offset, and store it in heap
    p[0] = [f"PUSHG {var_info['index']}"] + p[5] + [f'PUSHS "Value for {p[3]}[.]: "', "WRITES", "READ", "ATOI"] + [f"STOREN"]

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
    if var_info["array"]:
        raise SemanticError(f"Invalid type, expected int: {p[1]}")

    if not var_info['initialized']:
      raise SemanticError(f"Uninitialized variable: {p[1]}")
    # push the value from the global region
    p[0] = [f"PUSHG {var_info['index']}"]

def p_expr_array(p):
    r"""
    Expr : ID "[" Expr "]"
    """
    var_info = p.parser.symbols.lookup(p[1])
    if not var_info["array"]:
        raise SemanticError(f"Invalid type, expected array: {p[1]}")

    if not var_info['initialized']:
      raise SemanticError(f"Uninitialized variable: {p[1]}")

    # with dynamic allocation, we can't know at static time which blocks of the struct are initialized

    # push the value from the heap
    p[0] = [f"PUSHG {var_info['index']}"] + p[3] + ["LOADN"]
            
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
