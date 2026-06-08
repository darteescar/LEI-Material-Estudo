from ply import yacc
from arithmetic_lexer import tokens, lex

def p_expr(p):
    r"""
    Expr : Expr "+" Term
         | Expr "-" Term
         | Term
    Term : Term "*" Factor
         | Term "/" Factor
         | Factor
    Factor : "(" Expr ")"
           | INT
    """    

class ParseError(Exception):
    pass

def p_error(t):
    raise ParseError(f"Unexpected token: {t.type if t else '$'}") # ply assumes None at end of input

parser = yacc.yacc()
