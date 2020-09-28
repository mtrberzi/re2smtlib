class ReStr:
    def __init__(self, codepoints):
        self.codepoints = codepoints

    def __str__(self):
        # Encode this as an SMT-LIBv2.6 string constant.
        s = '(str.to_re "'
        for codepoint in self.codepoints:
            if codepoint < 32 or codepoint >= 127:
                # unicode escape
                s += '\\u{' + format(codepoint, 'x') + '}'
            elif codepoint == 92:
                # escape backslash
                s += '\\u{5c}'
            else:
                s += chr(codepoint)
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
