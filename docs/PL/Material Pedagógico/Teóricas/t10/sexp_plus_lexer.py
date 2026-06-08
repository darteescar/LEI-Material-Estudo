import ply.lex as lex

class LexicalError(Exception):
    pass

tokens = ("DECL", "SET", "FUN", "PRINT",
          "INT", "ID",
          "ADD", "SUB", "MUL", "DIV")

literals = "()"

t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"

keywords = {
    "decl"  : "DECL",
    "fun"   : "FUN",
    "set"   : "SET",
    "print" : "PRINT" }

def t_ID(t):
  r"[A-Za-z]\w*"
  if t.value in keywords:
    t.type = keywords[t.value]
  return t

def t_INT(t):
  r"\d+"
  t.value = int(t.value)
  return t

t_ignore = " \t\n"

def t_error(t):
  raise LexicalError(f"Invalid symbol: {t.value[0]}")

lexer = lex.lex()