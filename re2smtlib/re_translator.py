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
        elif opcode == MAX_REPEAT or opcode == MIN_REPEAT:
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
                return ReLoop(min_count, max_count, self.visit(subexpr))
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
        elif opcode == RANGE:
            (lo, hi) = arguments
            return ReRange(lo, hi)
        elif opcode == NEGATE:
            if arguments is None:
                return ReNoOp()
            subexpr = arguments
            return ReComplement(self.visit(subexpr))
        elif opcode == AT:
            if arguments == AT_BEGINNING or arguments == AT_END or arguments == AT_BOUNDARY or arguments == AT_NON_BOUNDARY or arguments == AT_BEGINNING_STRING or arguments == AT_END_STRING:
                return ReNoOp()
            else:
                raise ValueError(f"AT opcode with argument {arguments} not handled")
        elif opcode == CATEGORY:
            space_characters = ReUnion([ReStr([32]), ReStr([9]), ReStr([10]), ReStr([12]), ReStr([13])])
            digits = ReRange(48, 57)
            # TODO we assume ASCII here, but this isn't correct
            words = ReUnion([digits, ReRange(65, 90), ReRange(97, 122), ReStr([95])])
            if arguments == CATEGORY_NOT_SPACE:
                return ReComplement(space_characters)
            elif arguments == CATEGORY_SPACE:
                return space_characters
            elif arguments == CATEGORY_DIGIT:
                return digits
            elif arguments == CATEGORY_NOT_DIGIT:
                return ReComplement(digits)
            elif arguments == CATEGORY_WORD:
                return words
            elif arguments == CATEGORY_NOT_WORD:
                return ReComplement(words)
            else:
                raise ValueError(f"unhandled category {arguments}")
        elif opcode == ANY:
            return ReAnyChar()
        else:
            raise ValueError(f"sre opcode {opcode} with arguments {arguments} has no SMT-LIB translation")

    def visit_literal(self, codepoint):
        return ReStr([codepoint])
        
