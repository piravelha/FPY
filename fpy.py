import re
from lark import Lark, Tree, Transformer
from lark.tree import Tree

grammar = r"""

%ignore /\s+/

?program: expression?

?expression: logical_expression
           | let_declaration
           | let_expression
           | lambda_expression

?logical_expression: equality_expression (LOGICAL_OPERATOR equality_expression)*

?equality_expression: relational_expression (EQUALITY_OPERATOR relational_expression)*

?relational_expression: additive_expression (RELATIONAL_OPERATOR additive_expression)*

?additive_expression: multiplicative_expression (ADDITIVE_OPERATOR multiplicative_expression)*

?multiplicative_expression: unary_expression (MULTIPLICATIVE_OPERATOR unary_expression)*

?unary_expression: UNARY_OPERATOR? application_expression

?application_expression: primary_expression ((" " | "\n" | "\t") primary_expression)*

?primary_expression: NUMBER_LITERAL
                   | STRING_LITERAL
                   | IDENTIFIER
                   | "(" expression ")"

?let_declaration: "let" IDENTIFIER "=" expression "\n" expression

?let_expression: "let" IDENTIFIER "=" expression "in" expression

?lambda_expression: "&" IDENTIFIER expression

LOGICAL_OPERATOR: /\|\||\&\&/
EQUALITY_OPERATOR: /\=\=|\!\=/
RELATIONAL_OPERATOR: /\<|\>|\<\=|\>\=/
ADDITIVE_OPERATOR: /\+|\-/
MULTIPLICATIVE_OPERATOR: /\*|\//
UNARY_OPERATOR: /\!|\+|\-/
IDENTIFIER: /[a-zA-Z_][a-zA-Z_0-9]*/
STRING_LITERAL: /"[^"]*"/
NUMBER_LITERAL: /\d+(\.\d+)?/

"""

parser = Lark(grammar, start="program")

class GeneratePY(Transformer):
  identifier_counter = 0

  def highlight(self, code):
    new = ""
    index = 0

    while index < len(code):
      if result := re.findall(r"^&(\w+)", code[index:]):
        result = result[0]
        new += f"\x1b[35m&{result}"
        index += len(result) + 1
        continue
      if result := re.findall(r"^\"([^\"]*)\"", code[index:]):
        result = result[0]
        new += f"\x1b[32m\"{result}\""
        index += len(result) + 2
        continue
      if code[index] in "()[]":
        new += f"\x1b[34m{code[index]}"
        index += 1
        continue
      if code[index:index+3] == "let":
        new += "\x1b[31mlet"
        index += 3
        continue
      if code[index] in "+-/*=:":
        new += f"\x1b[36m{code[index]}"
        index += 1
        continue
      if result := re.findall(r"^[a-zA-Z_][a-zA-Z_0-9]*", code[index:]):
        result = result[0]
        new += f"\x1b[0m{result}"
        index += len(result)
        continue
      if code[index] in "1234567890.":
        new += f"\x1b[33m{code[index]}"
        index += 1
        continue
      new += f"\x1b[0m{code[index]}"
      index += 1
      continue

    return new


  def highlight_py(self, code):
    new = ""
    index = 0

    while index < len(code):
      if code[index:index+5] == "print":
        new += "\x1b[35mprint"
        index += 5
        continue
      if result := re.findall(r"^\"([^\"]*)\"", code[index:]):
        result = result[0]
        new += f"\x1b[32m\"{result}\""
        index += len(result) + 2
        continue
      if code[index] in "()[]":
        new += f"\x1b[34m{code[index]}"
        index += 1
        continue
      if code[index:index+6] == "lambda":
        new += "\x1b[31mlambda"
        index += 6
        continue
      if code[index] in "+-/*:":
        new += f"\x1b[36m{code[index]}"
        index += 1
        continue
      if result := re.findall(r"^[a-zA-Z_][a-zA-Z_0-9]*", code[index:]):
        result = result[0]
        new += f"\x1b[0m{result}"
        index += len(result)
        continue
      if code[index] in "1234567890.":
        new += f"\x1b[33m{code[index]}"
        index += 1
        continue
      new += f"\x1b[0m{code[index]}"
      index += 1
      continue

    new += "\x1b[0m"
    return new
  
        

  def format(self, code):
    return f"print({code})"

  def transform(self, tree):
    if isinstance(tree, Tree):
      return self.format(super().transform(tree))
    else:
      return self.format(f"{tree}")

  def program(self, args):
    return f"{args[0] if args else ""}"

  def let_declaration(self, args):
    name, value, program = args
    return f"(lambda {name}: {program})({value})"

  def let_expression(self, args):
    name, value, body = args
    return f"(lambda {name}: {body})({value})"
  
  def lambda_expression(self, args):
    name, body = args
    return f"lambda {name}: {body}"

  def logical_expression(self, args):
    final = args[0]
    for op, arg in zip(args[1::2], args[2::2]):
      final += f" {op} {arg}"
    return final
  
  def equality_expression(self, args):
    final = args[0]
    for op, arg in zip(args[1::2], args[2::2]):
      final += f" {op} {arg}"
    return final

  def relational_expression(self, args):
    final = args[0]
    for op, arg in zip(args[1::2], args[2::2]):
      final += f" {op} {arg}"
    return final

  def additive_expression(self, args):
    final = args[0]
    for op, arg in zip(args[1::2], args[2::2]):
      final += f" {op} {arg}"
    return final

  def multiplicative_expression(self, args):
    final = args[0]
    for op, arg in zip(args[1::2], args[2::2]):
      final += f" {op} {arg}"
    return final

  def unary_expression(self, args):
    if len(args) == 2:
      op, expr = args
      return f"{op}{expr}"
    return f"{args[0]}"

  def application_expression(self, args):
    final = args[0]
    for arg in args[1:]:
      final += f"({arg})"
    return final

import os
import time

os.system("cls")
time.sleep(0.5)

def print_results(input):
  tree = parser.parse(input.strip())
  py_code = GeneratePY().transform(tree)
  print("\x1b[31;49;1mINPUT:\x1b[0m " + "\n\n" + GeneratePY().highlight(input.strip()) + "\n\n" + "\x1b[33;49;1mGENERATED:\x1b[0m " + "\n\n" + GeneratePY().highlight_py(py_code) + "\n\n\x1b[32;49;1mOUTPUT:\x1b[0m " + "\n")
  exec(py_code)
  print("")