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
    print("Applying p1: E  → T ERest")
    recognize_T()
    recognize_ERest()
    print("Recognized p1: E  → T ERest")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal E: {token_type}")

def recognize_ERest():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "+":  #p2: ERest → + T ERest
    print("Applying p2: ERest → + T ERest")
    recognize_terminal("+")
    recognize_T()
    recognize_ERest()
    print("Recognized p2: ERest → + T ERest")
  elif token_type == "$":  #p3:    → ε
    print("Applying p3:    → ε")
    pass
    print("Recognized p3:    → ε")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal E': {token_type}")

def recognize_T():
  token_type, token_val, token_line, token_pos = lookahead()
  if token_type == "INT":  #p4: T  → F TRest
    print("Applying p4: T  → F TRest")
    recognize_F()
    recognize_TRest()
    print("Recognized p4: T  → F TRest")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal T: {token_type}")

def recognize_TRest():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == "*":    #p5: TRest → * F TRest
    print("Applying p5: TRest → * F TRest")
    recognize_terminal("*")
    recognize_F()
    recognize_TRest()
    print("Recognized p5: TRest → * F TRest")
  elif token_type in ("+", "$"):  #p6:    → ε
    print("Applying p6:    → ε")
    pass
    print("Recognized p6:    → ε")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal T': {token_type}")

def recognize_F():
  token_type, token_val, token_line, token_col = lookahead()
  if token_type == "INT":    #p7: F  → INT
    print("Applying p7: F  → INT")
    recognize_terminal("INT")
    print("Applying p7: F  → INT")
  else:
    raise ParseError(f"Unexpected token when recognizing nonterminal F: {token_type}")

def parse(text):
  lexer.input(text)
  next_token()
  recognize_E()
  if lookahead()[0] != "$":
    raise ParseError(f"Unexpected extra input: {lookahead()[0]}")