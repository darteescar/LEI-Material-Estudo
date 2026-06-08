from lists_lexer import lexer, next_token, lookahead

class ParseError(Exception):
    pass

# generic function to recognize terminals
def recognize_terminal(expected_type):
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == expected_type:
    next_token()
    return token_val
  else:
    raise ParseError(f"Unexpected token when recognizing terminal {expected_type}: {token_type}")
  
def recognize_List():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "[":    #p1: List         → '[' RestList
    print("Applying p1: List         → '[' RestList")
    recognize_terminal("[")
    recognize_RestList()
    print("Recognized p1: List         → '[' RestList")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'List': {token_type}")

def recognize_RestList():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p2: RestList     → Elements ']'
    print("Applying p2: RestList     → Elements ']'")
    recognize_Elements()
    recognize_terminal("]")
    print("Recognized p2: RestList     → Elements ']'")
  elif token_type == "]":  #p3:              | ']'
    print("Applying p3:              | ']'")
    recognize_terminal("]")
    print("Recognized p3:              | ']'")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'RestList': {token_type}")

def recognize_Elements():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p4: Elements     → INT RestElements
    print("Applying p4: Elements     → INT RestElements")
    recognize_terminal("INT")
    recognize_RestElements()
    print("Recognized p4: Elements     → INT RestElements")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'Elements': {token_type}")

def recognize_RestElements():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == ",":    #p5: RestElements → ',' Elements
    print("Applying p5: RestElements → ',' Elements")
    recognize_terminal(",")
    recognize_Elements()
    print("Recognized p5: RestElements → ',' Elements")
  elif token_type == "]":  #p6:              | ɛ
    print("Applying p6:              | ɛ")
    pass
    print("Recognized p6:              | ɛ")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'RestElements': {token_type}")

def parse(text):
  lexer.input(text)
  next_token()
  recognize_List()
  if lookahead()[0] != "$":
    raise ParseError(f"Unexpected extra input: {lookahead()[0]}")