def escape_codepoint(codepoint):
    if codepoint < 32 or codepoint >= 127:
        # unicode escape
        return '\\u{' + format(codepoint, 'x') + '}'
    elif codepoint == 92:
        # escape backslash
        return '\\u{5c}'
    elif codepoint == 34:
        # escape double-quote
        return '\\u{22}'
    else:
        return chr(codepoint)

class ReStr:
    def __init__(self, codepoints):
        self.codepoints = codepoints

    def __str__(self):
        # Encode this as an SMT-LIBv2.6 string constant.
        s = '(str.to_re "'
        for codepoint in self.codepoints:
            s += escape_codepoint(codepoint)
        s += '")'
        return s

class ReConcat:
    def __init__(self, args):
        self.args = args

    def __str__(self):
        s = "(re.++"
        for x in self.args:
            s += " " + str(x)
        s += ")"
        return s

class ReUnion:
    def __init__(self, args):
        self.args = args

    def __str__(self):
        s = "(re.union"
        for x in self.args:
            s += " " + str(x)
        s += ")"
        return s

class ReStar:
    def __init__(self, subexpr):
        self.args = [subexpr]

    def __str__(self):
        return "(re.* " + str(self.args[0]) + ")"

class RePlus:
    def __init__(self, subexpr):
        self.args = [subexpr]

    def __str__(self):
        return "(re.+ " + str(self.args[0]) + ")"

class ReComplement:
    def __init__(self, subexpr):
        self.args = [subexpr]
        
    def __str__(self):
        return "(re.comp " + str(self.args[0]) + ")"

class ReOpt:
    def __init__(self, subexpr):
        self.args = [subexpr]

    def __str__(self):
        return "(re.opt " + str(self.args[0]) + ")"

class ReRange:
    def __init__(self, lo, hi):
        self.args = []
        self.lo = lo
        self.hi = hi

    def __str__(self):
        return "(re.range \"" + escape_codepoint(self.lo) + "\" \"" + escape_codepoint(self.hi) + "\")"

class ReLoop:
    def __init__(self, lo, hi, subexpr):
        self.args = [subexpr]
        self.lo = lo
        self.hi = hi

    def __str__(self):
        return "((_ re.loop " + str(self.lo) + " " + str(self.hi) + ") " + str(self.args[0]) + ")"

class ReAnyChar:
    def __init__(self):
        self.args = []

    def __str__(self):
        return '(re.allchar)'
    
class ReNoOp:
    def __init__(self):
        self.args = []

    def __str__(self):
        return ''
