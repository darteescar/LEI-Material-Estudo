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
    recognize_terminal("[")
    total = recognize_RestList() 
    return total         # return the total of the actual list
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'List': {token_type}")

def recognize_RestList():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p2: RestList     → Elements ']'
    total = recognize_Elements()
    recognize_terminal("]")
    return total         # has elements, return their total
  elif token_type == "]":  #p3:              | ']'
    recognize_terminal("]")
    return 0             # no elements, total is 0
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'RestList': {token_type}")

def recognize_Elements():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p4: Elements     → INT RestElements
    elem = recognize_terminal("INT")
    elems = recognize_RestElements()
    return elem + elems  # an element plus the rest of the list
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'Elements': {token_type}")

def recognize_RestElements():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == ",":    #p5: RestElements → ',' Elements
    recognize_terminal(",")
    elems = recognize_Elements()
    return elems         # more elements, return their total
  elif token_type == "]":  #p6:              | ɛ
    return 0             # end of the list, total is 0
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'RestElements': {token_type}")
  
def parse(text):
  lexer.input(text)
  next_token()
  result = recognize_List()
  if lookahead()[0] != "$":
    raise ParseError(f"Unexpected extra input: {lookahead()[0]}")
  return result