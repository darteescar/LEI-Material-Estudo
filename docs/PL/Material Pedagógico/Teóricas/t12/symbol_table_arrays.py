class SemanticError(Exception):
    pass

# A simple symbol table, registers whether the variable has been initialized
class SymbolTable():
  def __init__(self):
    self.__table = {}
    self.__label_count = 0

  def __repr__(self):
    return self.__table.__repr__()

  # return all declared variables of the nearest scope (only if positive index, to ignore function arguments)
  def symbols(self):
    return self.__table.keys()

  # return variable info on the closest scope, registering scope
  def lookup(self, id):
    if id in self.__table:
      return self.__table[id]
    raise SemanticError(f"Undeclared variable: {id}")

  def declare(self, id, array=False):
    idx = len(self.__table)
    if id in self.__table:
      raise SemanticError(f"Duplicate declaration: {id}")
    self.__table[id] = { 'index': idx, 'initialized': array, 'array': array }
    print(self.__table)

  # mark a variable as initialized, if already declared
  def initialize(self, id):
    if id in self.__table:
      self.__table[id]['initialized'] = True
      return
    raise SemanticError(f"Undeclared variable: {id}")

  # guarantees unique identifier for labels
  def new_label(self):
    self.__label_count += 1
    return self.__label_count