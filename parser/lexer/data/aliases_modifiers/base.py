from backend.config import CONFIG

cust = CONFIG.customization
operators = cust.operators
objects = cust.objects
literals = cust.literals
control = cust.control_flow
templates = CONFIG.templates

def ne():
    if not operators.comparison.inequality.enabled:
        return ("_SkipPattern",)
    match operators.comparison.inequality.syntax:
        case "!=":
            return ("Symbols", "ExclamationAndEqual")
        case "!==":
            return ("Symbols", "ExclamationAndDoubleEqual")
        case "<>":
            return ("Symbols", "Diamond")
        case "><":
            return ("Symbols", "InvertedDiamond")

def sps():
    if not operators.comparison.spaceship_operator.enabled:
        return ("_SkipPattern",)
    match operators.comparison.spaceship_operator.syntax:
        case "<=>":
            return "Symbols", "SpaceCapsule"
        case ">=<":
            return "Symbols", "QuirkyLookingFace"

def default_case():
    match control.match_case.syntax.default_case_notation:
        case "*":
            return "Symbols", "Asterisk"
        case "_":
            return "Symbols", "Underscore"
        case "default":
            return "Keywords", "Default"

def floordiv():
    if not operators.arithmetic.floor_division.enabled:
        return ("_SkipPattern",)
    match operators.arithmetic.floor_division.syntax.get_value():
        case "//":
            return "Symbols", "DoubleForwardSlash"
        case "div":
            return "Keywords", "Div"
        case None:
            return ("_SkipPattern",)

def modulus():
    if not operators.arithmetic.modulus.enabled:
        return ("_SkipPattern",)
    match operators.arithmetic.modulus.syntax:
        case "%":
            return "Symbols", "Percent"
        case "mod":
            return "Keywords", "Mod"

def null():
    if cust.literals.null.enabled:
        return ("Primitives", "Null")
    return ("_SkipPattern", )

def boolean():
    if cust.literals.booleans.enabled:
        return ("Primitives", "Boolean")
    return ("_SkipPattern", )