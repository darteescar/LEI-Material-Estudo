from arithmetic_lexer import lexer, next_token, lookahead

# ----------------------------
# Parser
# ----------------------------

class ParseError(Exception):
    pass

def recognize_terminal(expected_type):
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == expected_type:
    next_token()
    return token_val
  else:
    raise ParseError(f"Unexpected token when recognizing terminal {expected_type}: {token_type}")

def recognize_E():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":    #p1: E  → T ERest
    left = recognize_T()
    rest = recognize_ERest()
    return left + rest
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal E: {token_type}")

def recognize_ERest():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "+":  #p2: ERest → + T ERest
    recognize_terminal("+")
    right = recognize_T()
    rest = recognize_ERest()
    return right + rest
  elif token_type == "$":  #p3:    → ε
    return 0
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal E': {token_type}")

def recognize_T():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p4: T  → F TRest
    left = recognize_F()
    rest = recognize_TRest()
    return left * rest
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal T: {token_type}")

def recognize_TRest():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == "*":    #p5: TRest → * F TRest
    recognize_terminal("*")
    right = recognize_F()
    rest = recognize_TRest()
    return right * rest
  elif token_type in ("+", "$"):  #p6:    → ε
    return 1
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal T': {token_type}")

def recognize_F():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == "INT":    #p7: F  → INT
    val = recognize_terminal("INT")
    return val
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal F: {token_type}")

def parse(text):
  lexer.input(text)
  next_token()
  tree = recognize_E()
  if lookahead()[0] != "$":
    raise ParseError(f"Unexpected extra input: {lookahead()[0]}")
  return tree