import sys
from lists_check_table_parser import parse

sys.stdout.write("Insert a list: ")
sys.stdout.flush()

for line in sys.stdin:
    try:
        parse(line)
    except Exception as e:
        print(e)
    sys.stdout.write("Insert a list: ")
    sys.stdout.flush()

print("Done")