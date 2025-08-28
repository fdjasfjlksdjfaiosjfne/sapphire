import typing
from backend import errors
from backend.config import CONFIG
from parser.lexer.data.modifiers.base import _factory as _base_factory

cust = CONFIG.customization
operators = cust.operators
arithmetic = operators.arithmetic
binary = operators.binary
booleans = operators.booleans
comparison = operators.comparison
logical = operators.logical
others = operators.other

def _factory[T: tuple[str, ...]](conf, dct: dict[str, T]) -> T | tuple[typing.Literal["_SkipPattern"]]:
    return _base_factory(conf.enabled, conf.syntax, dct)

OR = {
    "or": ("Keywords", "Or"),
    "b|": ("Symbols", "BAndVerticalBar"),
    "|": ("Symbols", "VerticalBar"),
    "||": ("Symbols", "DoubleVerticalBar")
}

AND = {
    "and": ("Keywords", "And"),
    "b&": ("Symbols", "BAndAndpersand"),
    "&": ("Symbols", "Andpersand"),
    "&&": ("Symbols", "DoubleAndpersand")
}

XOR = {
    "xor": ("Keywords", "Xor"),
    "b^": ("Symbols", "BAndCaret"),
    "^": ("Symbols", "Caret"),
    "^^": ("Symbols", "DoubleCaret")
}

# ^ ========================================================= ARITHMETIC ==========================================================

def addition():
    return _factory(arithmetic.addition, {
        "+": ("Symbols", "Plus")
    })

def subtraction():
    return _factory(arithmetic.subtraction, {
        "-": ("Symbols", "Dash")
    })

def multiplication():
    return _factory(arithmetic.multiplication, {
        "*": ("Symbols", "Asterisk")
    })

def true_division():
    return _factory(arithmetic.true_division, {
        "/": ("Symbols", "ForwardSlash")
    })

def floor_division():
    return _factory(arithmetic.floor_division, {
        "//": ("Symbols", "DoubleForwardSlash"),
        "div": ("Keywords", "Div")
    })

def modulus():
    return _factory(arithmetic.modulus, {
        "%": ("Symbols", "Percent"),
        "mod": ("Keywords", "Mod")
    })

# ^ ========================================================= COMPARISONS =========================================================

def eq():
    return _factory(comparison.equality, {
        "==": ("Symbols", "DoubleEqual"),
        "===": ("Symbols", "TripleEqual"),
    })

def ne():
    return _factory(comparison.inequality, {
        "!=": ("Symbols", "ExclamationAndEqual"),
        "!==": ("Symbols", "ExclamationAndDoubleEqual"),
        "<>": ("Symbols", "Diamond"),
        "><": ("Symbols", "InvertedDiamond")
    })

def loose_eq():
    return _base_factory(
        comparison.loose_equality.enabled,
        comparison.loose_equality.equality_syntax,
        {
            "~=": ("Symbols", "TildaAndEqual"),
            "==": ("Symbols", "DoubleEqual")
        }
    )

def loose_ne():
    return _base_factory(
        comparison.loose_equality.enabled,
        comparison.loose_equality.inequality_syntax,
        {
            "!~=": ("Symbols", "ExclamationAndTildaAndEqual"),
            "~!=": ("Symbols", "TildaAndExclamationAndEqual"),
            "!<>": ("Symbols", "ExclamationAndDiamond"),
            "!><": ("Symbols", "ExclamationAndInvertedDiamond"),
            "!=": ("Symbols", "ExclamationAndEqual")
        }
    )

def sps():
    return _factory(comparison.spaceship_operator, {
        "<=>": ("Symbols", "SpaceCapsule"),
        ">=<": ("Symbols", "QuirkyLookingFace")
    })

# ^ =========================================================== LOGICAL ===========================================================

def logical_or():
    return _factory(logical.inclusive_or, OR)

def logical_and():
    return _factory(logical.and_, AND)

def logical_xor():
    return _factory(logical.exclusive_or, XOR)

# ^ =========================================================== BOOLEANS ==========================================================

def booleans_or():
    return _factory(booleans.inclusive_or, OR)

def booleans_and():
    return _factory(booleans.and_, AND)

def booleans_xor():
    return _factory(booleans.exclusive_or, XOR)

# ^ =========================================================== BINARY ============================================================

def binary_or():
    return _factory(booleans.inclusive_or, OR)

def binary_and():
    return _factory(booleans.and_, AND)

def binary_xor():
    return _factory(booleans.exclusive_or, XOR)

# ^ =========================================================== OTHERS ============================================================

def matrix_multiplication():
    return _factory(others.matrix_multiplication, {
        "@": ("Symbols", "At")
    })

def string_concanentation():
    return _factory(others.string_concanentation, {
        "..": ("Symbols", "DoubleDot")
    })