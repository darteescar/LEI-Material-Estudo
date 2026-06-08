import ply.lex as lex

tokens = ['TEXT', 'INT', 'FLOAT', 'SYMBOL', 'NEWLINE', 'HYPHEN']

# we used - as a delimiter, but we also want - to appear in the additional text
# best was to is to change state once we find a -
states = (("REST", "exclusive"),)

# we decided that a category was identified by any non-regular symbol (emojis)
def t_SYMBOL(t):
    r"[^A-Za-z0-9_\n-]"
    return t

def t_FLOAT(t):
    r'-?\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT(t):
    r'-?\d+'
    t.value = int(t.value)
    return t

# before the first - is found, we do not allow it in the text
def t_TEXT(t):
    r'[A-Za-z ,&]+'
    return t

# once the first - is found, we allow it in the text
def t_REST_TEXT(t):
    r'.+'
    return t

def t_HYPHEN(t):
    r"-"
    t.lexer.begin("REST")
    return t

# we decided that product entries were simply identified by a new line, so we must return these tokens
# also, reset the state so that - are no longer allowed in the text
def t_ANY_NEWLINE(t):
    r"\n"
    lexer.lineno += 1
    t.lexer.begin("INITIAL")
    return t

t_ANY_ignore = " \t"

class LexError(Exception):
    pass

def t_ANY_error(t):
    raise LexError(f"Invalid symbol: {t.value[0]}")

lexer = lex.lex()

if __name__ == "__main__":
    import sys
    text = sys.stdin.read()
    lexer.input(text)
    for tok in lexer:
        print(tok)
