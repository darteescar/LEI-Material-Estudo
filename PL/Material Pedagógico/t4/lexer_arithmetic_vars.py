import ply.lex as lex

tokens = ( "INT", "ADD", "SUB", "MUL", "DIV", "LET", "IDEN" )
# moved some token symbols into literals
literals = "()=;"

t_IDEN = r"[A-Za-z]+"
t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"

# functions have higher priority, avoid clash with IDEN
def t_LET(t):
  r"let"
  return t

# functions allow can update the token value
def t_INT(t):
  r"\d+"
  t.value = int(t.value)
  return t

t_ignore = " \t"

# new lines must be matched to count lines, cannot be simply ignored
def t_newline(t):
  r"\n"
  t.lexer.lineno += 1

# typical behavior is to report and continue, could also abort immediately
def t_error(t):
  print("Invalid symbol:", t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

def tokenize(input):
  lexer.input(input)
  return lexer
