class SemanticError(Exception):
    pass

# A simple symbol table, registers whether the variable has been initialized
class SymbolTable():
  def __init__(self):
    self.__table = {}
    self.__label_count = 0

  def __repr__(self):
    return self.__table.__repr__()

  # return all declared symbols
  def symbols(self):
    return self.__table.keys()

  # return whether variable info, but only if declared
  def lookup(self, id):
    if id not in self.__table:
      raise SemanticError(f"Undeclared variable: {id}")
    else:
      return self.__table.get(id)

  # declare an identifier, set it as uninitialized and assign an index, do not allow duplicate declarations
  def declare(self, id):
    idx = len(self.__table)
    if id in self.__table:
      raise SemanticError(f"Duplicate declaration: {id}")
    self.__table[id] = { 'index': idx, 'initialized': False }

  # mark a variable as initialized, but only if declared
  def initialize(self, id):
    if id not in self.__table:
      raise SemanticError(f"Undeclared variable: {id}")
    self.__table[id]['initialized'] = True

  # guarantees unique identifier for labels
  def new_label(self):
    self.__label_count += 1
    return self.__label_count
