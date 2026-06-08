from arithmetic_eval import parser
import sys

sys.stdout.write("Insert an expression: ")
sys.stdout.flush()

for line in sys.stdin:
    try:
        res = parser.parse(line)
        print("Parsing succeeded.")
        print("Result:", res)
    except Exception as e:
        print(e)
    sys.stdout.write("Insert a list: ")
    sys.stdout.flush()

print("Done")
