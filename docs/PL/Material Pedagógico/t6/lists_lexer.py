import ply.lex as lex

class LexError(Exception):
    pass

tokens = ("INT",)
literals = "[],"

def t_INT(t):
  r"\d+"
  t.value = int(t.value)
  return t
  
t_ignore = " \t\n"

def t_error(t):
  raise LexError(f"Invalid symbol: {t.value[0]}")

__file__ = "Untitled.ipynb" # needed to run PLY inside notebook
lexer = lex.lex()

_lookahead = None

# asks the lexer for the next token
def next_token():
  global _lookahead
  _lookahead = lexer.token()

# auxiliary function for token type, returns special end of input $ token if no more tokens
def lookahead():
  return (_lookahead.type,_lookahead.value,_lookahead.lineno,_lookahead.lexpos) if _lookahead else ("$",None,None,None)