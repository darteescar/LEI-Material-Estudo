from lists_lexer import lexer, next_token, lookahead

class ParseError(Exception):
    pass

def generate(start,terminals,parse_table,productions):
  def parser(text):
    lexer.input(text)
    next_token()
    stack = ["$", start]

    while stack:
      next_symbol = stack.pop()
      token_type, token_val, token_line, token_pos = lookahead()

      if next_symbol in terminals:
          if next_symbol == token_type:
            next_token()
          else:
            raise ParseError(f"Unexpected token when recognizing terminal {next_symbol}: {token_type}")
      else:
        next_production = parse_table.get((next_symbol,token_type))
        if not next_production:
          raise ParseError(f"Unexpected token when recognizing nonterminal {next_symbol}: {token_type}")
        else:
          rhs = productions[next_production]
          print(f"Applying {next_production}: {next_symbol} → {rhs}")
          stack.extend(rhs[::-1])
  return parser

parse_table = {
    ("List","[") : "p1",
    ("RestList","]") : "p3",
    ("RestList","INT") : "p2",
    ("Elements","INT") : "p4",
    ("RestElements",",") : "p5",
    ("RestElements","]") : "p6"
}

terminals = ("[","]",",","INT","$")

productions = {
    "p1": ["[", "RestList"],
    "p2": ["Elements", "]"],
    "p3": ["]"],
    "p4": ["INT", "RestElements"],
    "p5": [",", "Elements"],
    "p6": []
}

parse = generate("List",terminals,parse_table,productions)