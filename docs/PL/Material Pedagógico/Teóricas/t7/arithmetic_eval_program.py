import sys
from arithmetic_eval_parser import parse

sys.stdout.write("Insert an expression: ")
sys.stdout.flush()

for line in sys.stdin:
    try:
        v = parse(line)
        print("Parsing succeeded.")
        print("Return value:", v)
    except Exception as e:
        print(e)
    sys.stdout.write("Insert an expression: ")
    sys.stdout.flush()

print("Done")