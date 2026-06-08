import sys
from lists_eval_rec_parser import parse

sys.stdout.write("Insert a list: ")
sys.stdout.flush()

for line in sys.stdin:
    try:
        print(parse(line))
    except Exception as e:
        print(e)
    sys.stdout.write("Insert a list: ")
    sys.stdout.flush()

print("Done")