import ply.lex as lex

# exclusive state, does not accumulate with INITIAL
states = ( ("COMMENT", "exclusive"), )

tokens = ( "INT", "ADD", "SUB", "MUL", "DIV", "LET", "IDEN" )
literals = "()=;"

# default behavior (INITIAL state)

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

# change lexer state, register start of comment block
def t_enter_comment(t):
    r"/\*"
    t.lexer.comment_line = t.lexer.lineno
    t.lexer.begin("COMMENT")

t_ignore = " \t"

# new lines must be matched to count lines, cannot be simply ignored
def t_newline(t):
  r"\n"
  t.lexer.lineno += 1

# ANY means it will apply to all states (should not occur in COMMENT state)
def t_ANY_error(t):
  print("Invalid symbol:", t.value[0])
  t.lexer.skip(1)

# comment-block behaviour (state COMMENT)

# change lexer state back to default
def t_COMMENT_exit_comment(t):
    r"\*/"
    t.lexer.begin("INITIAL")

# ignore anything while in comment (except */, has higher priority)
def t_COMMENT_comments(t):
    r".|\n"
    t.lexer.lineno += t.value.count("\n")

# EOF while in comment is an error, report properly
def t_COMMENT_eof(t):
    line = t.lexer.comment_line
    print(f"Comment block starting in line {line} not closed.")

# the rules above already ignore everything
t_COMMENT_ignore = ""

def tokenize(input):
  lexer = lex.lex()
  lexer.input(input)
  return lexer
