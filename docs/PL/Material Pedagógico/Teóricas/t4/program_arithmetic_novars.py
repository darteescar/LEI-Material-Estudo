import sys
from lexer_arithmetic_novars import tokenize

for tok in tokenize(sys.stdin.read()):
  print(tok)