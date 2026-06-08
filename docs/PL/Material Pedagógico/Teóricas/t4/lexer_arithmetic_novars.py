import ply.lex as lex

tokens = ( "INT", "LPAREN", "RPAREN", "ADD", "SUB", "MUL", "DIV" )

t_INT = r"\d+"
t_LPAREN = r"\("
t_RPAREN = r"\)"
t_ADD = r"\+"
t_SUB = r"-"
t_MUL = r"\*"
t_DIV = r"/"

t_ignore = " \t\n"

def t_error(t):
  print("Invalid symbol:", t.value[0])
  t.lexer.skip(1)

lexer = lex.lex()

def tokenize(input):
  lexer.input(input)
  return lexer
