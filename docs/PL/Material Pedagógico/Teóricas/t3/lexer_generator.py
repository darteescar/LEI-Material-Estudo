import sys
import json

def generate(token_file):
  with open(token_file, "r") as f:
    token_dict = json.load(f)

  if "UNKNOWN" in token_dict:
    print("Reserved token name UNKNOWN")
    return

  regex = ("|".join(f"(?P<{token}>{pattern})" for token, pattern in token_dict.items()))+"|(?P<UNKNOWN>.)"
  code = f"""import re
import sys
def tokenize(line):
  line_num = 1
  recognized = []
  errors = []
  for mtch in re.finditer(r"{regex}",line):
    for k,v in mtch.groupdict().items():
      if v != None:
        token = (k, v, line_num, mtch.start())
        break

    if token[0] == "NEWLINE":
      line_num += token[1].count("\\n")
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
"""
  print(code)

def main():
    if len(sys.argv) < 2:
        print("Usage: python generator.py <filename>")
        sys.exit(1)

    filename = sys.argv[1]

    generate(filename)

if __name__ == "__main__":
    main()