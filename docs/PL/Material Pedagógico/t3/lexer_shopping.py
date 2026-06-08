import re
import sys
def tokenize(line):
  line_num = 1
  recognized = []
  errors = []
  for mtch in re.finditer(r"(?P<HEADER>\*\s+[^\n]*)|(?P<TEXT>[^\n]+)|(?P<SKIP>\n+)|(?P<UNKNOWN>.)",line):
    for k,v in mtch.groupdict().items():
      if v != None:
        token = (k, v, line_num, mtch.start())
        break

    if token[0] == "NEWLINE":
      line_num += token[1].count("\n")
    elif token[0] == "UNKNOWN":
        errors.append(token)
    elif token[0] != "IGNORE":
        recognized.append(token)
  return recognized, errors

def main():
  toks, errs = tokenize(sys.stdin.read())
  for err in errs:
      print("Invalid symbol:", err)
  for tok in toks:
      print(tok)

if __name__ == "__main__":
    main()

