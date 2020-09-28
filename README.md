# re2smtlib

This package exposes an API that translates regular expressions into [SMT-LIB v2.6](https://smtlib.cs.uiowa.edu) syntax.

## Example usage

    import re2smtlib
    re2smtlib.translate_regex_to_smtlib("a*")
    # '(re.* (str.to_re "a"))'

