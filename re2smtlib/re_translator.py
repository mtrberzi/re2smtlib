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
        elif opcode == MAX_REPEAT:
            (min_count, max_count, subexpr) = arguments
            if min_count == 0 and max_count == MAXREPEAT:
                # Kleene star
                return ReStar(self.visit(subexpr))
            elif min_count == 1 and max_count == MAXREPEAT:
                # plus
                return RePlus(self.visit(subexpr))
            elif min_count == 0 and max_count == 1:
                # opt
                return ReOpt(self.visit(subexpr))
            else:
                raise ValueError(f"don't know how to handle MAX_REPEAT with {min_count} {max_count} {subexpr}")
        elif opcode == SUBPATTERN:
            (group, add_flags, del_flags, subexpr) = arguments
            return self.visit(subexpr)
        elif opcode == IN:
            exprs = [self.visit_one(x) for x in arguments]
            return ReUnion(exprs)
        elif opcode == BRANCH:
            (unused, subexprs) = arguments
            exprs = [self.visit(x) for x in subexprs]
            return ReUnion(exprs)
        elif opcode == NOT_LITERAL:
            codepoint = arguments
            return ReComplement(ReStr([codepoint]))
        else:
            raise ValueError(f"sre opcode {opcode} with arguments {arguments} has no SMT-LIB translation")

    def visit_literal(self, codepoint):
        return ReStr([codepoint])
        
