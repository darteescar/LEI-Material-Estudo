import sys
from lexer_arithmetic_vars import tokenize

for tok in tokenize(sys.stdin.read()):
  print(tok)