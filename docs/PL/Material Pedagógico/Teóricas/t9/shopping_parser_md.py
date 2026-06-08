import ply.yacc as yacc
from shopping_lexer import tokens

# Language design decisions made during class:
#  - The start of a category is marked by any special symbol
#  - An empty line is mandatory between categories
#  - Each product is identified by a new line
#  - The quantities may have an optional text associated
#  - An hyphen - marks the beginning of arbitrary optional text
#  - This optional text is allowed to contain other hyphens 
def p_list(p):
    r"""
    List : Categories
    """
    p[0] = "\n".join(["# Shopping list"] + p[1])

def p_categories(p):
    r"""
    Categories : Categories Category
               | Category
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + p[2]

def p_category(p):
    r"""
    Category : SYMBOL TEXT Products NEWLINE NEWLINE
    """
    p[0] = [f"## {p[1]} {p[2]}"] + p[3] + [""]

def p_items(p):
    r"""
    Products : Products Product
             | Product
    """
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1]
            
def p_item(p):
    r"""
    Product : NEWLINE TEXT Quantity HyphenInfoOpt
    """
    p[0] = [f"- {p[2]}: {p[3]} {p[4]}"]

def p_hinfo(p):
    r"""
    HyphenInfoOpt : HYPHEN TEXT
                  |
    """
    if len(p) == 3:
        p[0] = f"(*{p[2]}*)"
    else:
        p[0] = ""

def p_info(p):
    r"""
    InfoOpt : TEXT
            |
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ""

def p_quantity(p):
    r"""
    Quantity : INT InfoOpt
             | FLOAT InfoOpt
    """
    p[0] = f"{p[1]} {p[2]}"

class ParseError(Exception):
    pass

def p_error(t):
    raise ParseError(f"Unexpected token: {t if t else '$'}") # ply assumes None at end of input

parser = yacc.yacc()

import sys
text =  sys.stdin.read()
res = parser.parse(text)
try:
    res = parser.parse(text)
    print(res)
except ParseError as e:
    print("Invalid text:", e)