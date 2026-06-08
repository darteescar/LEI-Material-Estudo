import ply.lex as lex

class LexError(Exception):
    pass

tokens = ("INT",)
literals = "+*-/()"

def t_INT(t):
  r"\d+"
  t.value = int(t.value)
  return t
  
t_ignore = " \t\n"

def t_error(t):
    raise LexError(f"Invalid symbol: {t.value[0]}")

lexer = lex.lex()
