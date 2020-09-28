__all__ = ["translate_regex_to_smtlib"]

from sre_parse import parse
from sre_constants import *

from .re_translator import ReTranslator
from .smt_simplifier import SmtSimplifier

def translate_regex_to_smtlib(re_str):
    re_parse_tree = parse(re_str)
    translator = ReTranslator()
    smt_ast = translator.visit(re_parse_tree)
    simplifier = SmtSimplifier()
    simplified_ast = simplifier.simplify(smt_ast)
    return str(simplified_ast)
