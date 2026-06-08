import sys
from lexer_arithmetic_comments_nostate import tokenize

for tok in tokenize(sys.stdin.read()):
  print(tok)