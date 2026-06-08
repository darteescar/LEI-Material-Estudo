class SemanticError(Exception):
    pass

# A simple symbol table, registers whether the variable has been initialized
class SymbolTable():
  def __init__(self):
    self.__table = [{}]
    # only top-level functions
    self.__funs = {}
    self.__label_count = 0

  def __repr__(self):
    return self.__table.__repr__()

  # create a new context for variables
  def push(self):
    self.__table.append({})

  # pop a context for variables
  def pop(self):
    self.__table.pop()

  # test if in a local or global context
  def local(self):
    return len(self.__table) > 1

  # return all declared variables of the nearest scope (only if positive index, to ignore function arguments)
  def symbols(self):
    return {k for k in self.__table[-1] if self.__table[-1][k].get("index",-1) >= 0}

  # return all declared functions
  def funs(self):
    return self.__funs.values()

  # return variable info on the closest scope, registering scope
  def lookup(self, id):
    for t in self.__table[::-1]:
      if id in t:
        return t[id] | { "global" : t == self.__table[0] }
    raise SemanticError(f"Undeclared variable: {id}")

  # return function info
  def lookup_fun(self, id):
    if id in self.__funs:
      return self.__funs[id]
    raise SemanticError(f"Undeclared function: {id}")

  # declare a global identifier, set it as uninitialized and assign an index, do not allow duplicate declarations
  def declare_global(self, id):
    return self.__declare(id,0)

  # declare a local identifier, set it as uninitialized and assign an index, do not allow duplicate declarations
  def declare_local(self, id):
    return self.__declare(id,-1)

  def __declare(self, id, frm):
    idx = len([k for k in self.__table[frm] if self.__table[frm][k].get("index",-1) >= 0])
    if id in self.__table[frm]:
      raise SemanticError(f"Duplicate declaration: {id}")
    self.__table[frm][id] = { 'index': idx, 'initialized': False }

  # define a new function, push new context with arguments with negative indices, create distinguished key for return value
  def define(self, id, args):
    if id in self.__funs:
      raise SemanticError(f"Duplicate definition: {id}")
    self.__funs[id] = { 'args': args }
    self.push()
    for i, arg in enumerate(args):
      self.__table[-1][arg] = { 'index': -(i+1), 'initialized': True }
    self.__table[-1][None] = { 'index': -(len(args)+1), 'initialized': True }

  # register the code for a given function
  def register(self, id, code):
    if id in self.__funs:
      self.__funs[id]['code'] = code
      return
    raise SemanticError(f"Undeclared function: {id}")

  # mark a variable as initialized, if already declared
  def initialize(self, id):
    for t in self.__table[::-1]:
      if id in t:
        t[id]['initialized'] = True
        return
    raise SemanticError(f"Undeclared variable: {id}")

  # guarantees unique identifier for labels
  def new_label(self):
    self.__label_count += 1
    return self.__label_count