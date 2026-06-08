from ply import yacc
from arithmetic_lexer import tokens, lex

def p_expr(p):
    r"""
    Expr : Expr "+" Term
         | Expr "-" Term
         | Term
    """
    if len(p) == 2:
        p[0] = p[1]
    elif p[2] == "+":
        p[0] = p[1] + p[3]
    elif p[2] == "-":
        p[0] = p[1] - p[3]

def p_term_mul(p):
    """
    Term : Term "*" Factor
    """
    p[0] = p[1] * p[3]

def p_term_div(p):
    """
    Term : Term "/" Factor
    """
    p[0] = p[1] / p[3]

def p_term_factor(p):
    """
    Term : Factor
    """
    p[0] = p[1]

def p_factor_paren(p):
    """
    Factor : "(" Expr ")"
    """
    p[0] = p[2]

def p_factor_int(p):    
    """
    Factor : INT
    """
    p[0] = p[1]
    

class ParseError(Exception):
    pass

def p_error(t):
    raise ParseError(f"Unexpected token: {t.type if t else '$'}") # ply assumes None at end of input

parser = yacc.yacc()
