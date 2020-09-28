from sre_constants import *
from .ast import *

class ReTranslator:
    def __init__(self):
        pass

    def visit(self, re):
        # Top-level expressions are always a list of (opcode, args) elements
        objs = [self.visit_one(x) for x in re]
        if len(objs) == 1:
            return objs[0]
        else:
            return ReConcat(objs)

    def visit_one(self, re_term):
        opcode = re_term[0]
        arguments = re_term[1]
        if opcode == LITERAL:
            return self.visit_literal(arguments)
        else:
            raise ValueError(f"sre opcode {opcode} has no SMT-LIB translation")

    def visit_literal(self, codepoint):
        return ReStr([codepoint])
        
