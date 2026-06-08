import ply.yacc as yacc
from shopping_lexer import tokens

# Language design decisions made during class:
#  - The start of a category is marked by any special symbol
#  - An empty line is mandatory between categories
#  - Each product is identified by a new line
#  - The quantities may have an optional text associated
#  - An hyphen - marks the beginning of arbitrary optional text
#  - This optional text is allowed to contain other hyphens 
def p_parser(p):
    r"""
    List : Categories
    Categories : Categories Category
               | Category
    Category : SYMBOL TEXT Products NEWLINE NEWLINE
    Products : Products Product
             | Product
    Product : NEWLINE TEXT Quantity HyphenInfoOpt
    Quantity : INT InfoOpt
             | FLOAT InfoOpt
    HyphenInfoOpt : HYPHEN TEXT
                  |
    InfoOpt : TEXT
            | 
    """

class ParseError(Exception):
    pass

def p_error(t):
    raise ParseError(f"Unexpected token: {t if t else '$'}") # ply assumes None at end of input

parser = yacc.yacc()

import sys
text = sys.stdin.read()
try:
    parser.parse(text)
    print("Valid text.")
except ParseError as e:
    print("Invalid text:", e)