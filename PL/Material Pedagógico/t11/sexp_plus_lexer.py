import ply.lex as lex

class LexicalError(Exception):
    pass

tokens = ("DECL", "SET", "PRINT", "READ",
          "INT", "ID", "TRUE", "FALSE",
          "IF", "ADD", "SUB", "MUL", "DIV", "LT", "GT", "EQ")

literals = "()"

t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"
t_LT = r"<"
t_GT = r">"
t_EQ = r"="

keywords = {
    "true"  : "TRUE",
    "false" : "FALSE",
    "decl"  : "DECL",
    "set"   : "SET",
    "print" : "PRINT",
    "read"  : "READ",
    "if"    : "IF" }

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