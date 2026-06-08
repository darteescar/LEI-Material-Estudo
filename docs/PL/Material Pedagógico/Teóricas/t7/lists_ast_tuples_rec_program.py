import sys
from lists_ast_tuples_rec_parser import parse

sys.stdout.write("Insert a list: ")
sys.stdout.flush()

for line in sys.stdin:
    try:
        v = parse(line)
        print("Parsing succeeded.")
        print("Return value:", v)
    except Exception as e:
        print(e)
    sys.stdout.write("Insert a list: ")
    sys.stdout.flush()

print("Done")