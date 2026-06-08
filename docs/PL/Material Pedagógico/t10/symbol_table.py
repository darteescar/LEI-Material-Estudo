class SemanticError(Exception):
    pass

# A symbol table that registers identifiers, their kind (variable or function), and further attributes
class SymbolTable():
  def __init__(self):
    self.__table = [{}]

  # push a new scope into the stack
  def push(self):
    self.__table.append({})

  # pop the most recent scope from the stack
  def pop(self):
    self.__table.pop()

  # return whether variable initialized, but only if declared
  def lookup_var(self, id):
    # search all the scopes, starting with the most recent one
    for table in self.__table[::-1]:
      if id in table:
        if table.get(id)[0] != "var":
          raise SemanticError(f"Identifier is not a variable: {id}")
        return table.get(id)[1]
    raise SemanticError(f"Undeclared variable: {id}")

  # return the arity of a function, but only if declared
  def lookup_fun(self, id):
    # search all the scopes, starting with the most recent one
    for table in self.__table[::-1]:
      if id in table:
        if table.get(id)[0] != "fun":
          raise SemanticError(f"Identifier is not a function: {id}")
        return table.get(id)[1]
    raise SemanticError(f"Undeclared variable: {id}")

  # declare a variable
  def declare_var(self, id):
    if id in self.__table[-1]:
      raise SemanticError(f"Duplicate declaration: {id}")
    self.__table[-1][id] = ("var", False)

  # declare a function
  def declare_fun(self, id, params):
    if id in self.__table[-1]:
      raise SemanticError(f"Duplicate declaration: {id}")
    self.__table[-1][id] = ("fun", params)

  # mark a variable as initialized, but only if declared
  def initialize(self, id):
    for table in self.__table[::-1]:
      if id in table:
        if table.get(id)[0] != "var":
          raise SemanticError(f"Identifier is not a variable: {id}")
        table[id] = ("var", True)
        return
    raise SemanticError(f"Undeclared variable: {id}")