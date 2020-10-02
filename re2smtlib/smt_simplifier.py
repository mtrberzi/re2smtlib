from .ast import *

class SmtSimplifier:
    def __init__(self):
        pass

    def simplify(self, ast):
        if isinstance(ast, ReStr):
            return ast
        simplified_args = [self.simplify(x) for x in ast.args]
        if isinstance(ast, ReConcat):
            # flatten adjacent ReStr terms into a single term;
            # flatten inner ReConcat terms into this one
            flattened_args = []
            flattened_codepoints = []
            worklist = []
            worklist.extend(simplified_args)
            while worklist:
                term = worklist.pop(0)
                if isinstance(term, ReStr):
                    flattened_codepoints.extend(term.codepoints)
                elif isinstance(term, ReNoOp):
                    continue
                else:
                    if isinstance(term, ReConcat):
                        worklist.extend(term.args)
                    else:
                        # discharge codepoints into a new ReStr term
                        if flattened_codepoints:
                            flattened_args.append(ReStr(flattened_codepoints))
                            flattened_codepoints = []
                        flattened_args.append(term)
            # if there are codepoints left over, flatten them at the end
            if flattened_codepoints:
                flattened_args.append(ReStr(flattened_codepoints))
            # concatenation of 1 term is just that term, so discharge the concatenation
            if len(flattened_args) == 0:
                return ReNoOp()
            elif len(flattened_args) == 1:
                return flattened_args[0]
            else:
                return ReConcat(flattened_args)
        elif isinstance(ast, ReUnion):
            # TODO deduplicate args
            flattened_args = []
            worklist = []
            worklist.extend(simplified_args)
            while worklist:
                term = worklist.pop(0)
                if isinstance(term, ReUnion):
                    worklist.extend(term.args)
                elif isinstance(term, ReNoOp):
                    continue
                else:
                    flattened_args.append(term)
            if len(flattened_args) == 0:
                return ReNoOp()
            elif len(flattened_args) == 1:
                return flattened_args[0]
            else:
                return ReUnion(flattened_args)
        elif isinstance(ast, ReStar):
            return ReStar(simplified_args[0])
        elif isinstance(ast, RePlus):
            return RePlus(simplified_args[0])
        elif isinstance(ast, ReComplement):
            return ReComplement(simplified_args[0])
        elif isinstance(ast, ReOpt):
            return ReOpt(simplified_args[0])
        elif isinstance(ast, ReRange):
            return ast
        elif isinstance(ast, ReLoop):
            return ReLoop(ast.lo, ast.hi, simplified_args[0])
        elif isinstance(ast, ReAnyChar):
            return ast
        elif isinstance(ast, ReNoOp):
            return ast
        else:
            raise ValueError(f"simplifier doesn't know about {ast}")
