from lists_lexer import lexer, next_token, lookahead

class ParseError(Exception):
    pass

class ListNode:
  def __init__(self, elements):
    self.elements = elements

  def __repr__(self):
    return f"ListNode({self.elements})"


class ConsNode:
  def __init__(self, value, rest):
    self.value = value
    self.rest = rest

  def __repr__(self):
    return f"ConsNode({self.value}, {self.rest})"


class NilNode:
  def __repr__(self):
    return "NilNode()"
  

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
    elems = recognize_RestList()
    return ListNode(elems)        # the top-level list node 
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'List': {token_type}")

def recognize_RestList():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p2: RestList     → Elements ']'
    elems = recognize_Elements()
    recognize_terminal("]")
    return elems                  # list with elements, return them
  elif token_type == "]":  #p3:              | ']'
    recognize_terminal("]")
    return NilNode()              # empty list, return nil node
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'RestList': {token_type}")

def recognize_Elements():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p4: Elements     → INT RestElements
    elem = recognize_terminal("INT")
    elems = recognize_RestElements()
    return ConsNode(elem, elems)  # element followed by the rest of the list
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'Elements': {token_type}")

def recognize_RestElements():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == ",":    #p5: RestElements → ',' Elements
    recognize_terminal(",")
    elems = recognize_Elements()
    return elems                  # additional elements, return them
  elif token_type == "]":  #p6:              | ɛ
    return NilNode()              # no more elements, return nil node
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal 'RestElements': {token_type}")
  
def parse(text):
  lexer.input(text)
  next_token()
  result = recognize_List()
  if lookahead()[0] != "$":
    raise ParseError(f"Unexpected extra input: {lookahead()[0]}")
  return result