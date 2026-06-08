import sys
from arithmetic_eval_parser import parse

sys.stdout.write("Insert an expression: ")
sys.stdout.flush()

for line in sys.stdin:
    try:
        print(parse(line))
    except Exception as e:
        print(e)
    sys.stdout.write("Insert an expression: ")
    sys.stdout.flush()

print("Done")