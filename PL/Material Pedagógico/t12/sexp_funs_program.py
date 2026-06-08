from sexp_funs_translator import parse, SyntaxError
from sexp_lexer import LexicalError
from symbol_table_funs import SemanticError
import sys

try:
    res = parse(sys.stdin.read())
    print("Parsing succeeded.")
    print("Result, run in EWVW:")
    print(res)
except SyntaxError as e:
    print(e)
except LexicalError as e:
    print(e)
except SemanticError as e:
    print(e)
