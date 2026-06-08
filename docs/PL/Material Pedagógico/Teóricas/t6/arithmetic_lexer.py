import ply.lex as lex

# ----------------------------
# Lexer
# ----------------------------

class LexError(Exception):
    pass

tokens = ("INT",)
literals = "+*"

def t_INT(t):
  r"\d+"
  t.value = int(t.value)
  return t
  
t_ignore = " \t\n"

def t_error(t):
    raise LexError(f"Invalid symbol: {t.value[0]}")

__file__ = "Untitled.ipynb"   # sometimes needed by PLY in notebooks
lexer = lex.lex()

_lookahead = None

def next_token():
    global _lookahead
    _lookahead = lexer.token()

def lookahead():
  return (_lookahead.type,_lookahead.value,_lookahead.lineno,_lookahead.lexpos) if _lookahead else ("$",None,None,None)