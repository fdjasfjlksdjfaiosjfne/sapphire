from backend.config import CONFIG

cust = CONFIG.customization
redefine = cust.redefine
templates = CONFIG.templates

def ne():
    match redefine.inequality:
        case "!=":
            return "Symbols", "ExclamationAndEqual"
        case "!==":
            return ("Symbols", "ExclamationAndDoubleEqual")
        case "<>":
            return "Symbols", "Diamond"
        case "><":
            return "Symbols", "InvertedDiamond"

def sps():
    match redefine.spaceship_operator:
        case "<=>":
            return "Symbols", "SpaceCapsule"
        case ">=<":
            return "Symbols", "QuirkyLookingFace"
        case None:
            return ("_SkipPattern",)

def default_case():
    match cust.default_case_notation:
        case "*":
            return "Symbols", "Asterisk"
        case "_":
            return "Symbols", "Underscore"
        case "default":
            return "Keywords", "Default"

def floordiv():
    match redefine.floor_division:
        case "//":
            return "Symbols", "DoubleForwardSlash"
        case "div":
            return "Keywords", "Div"
        case None:
            return ("_SkipPattern",)

def modulus():
    match redefine.modulus:
        case "%":
            return "Symbols", "Percent"
        case "mod":
            return "Keywords", "Mod"
        case None:
            return ("_SkipPattern",)

def null():
    if cust.allow_null:
        return ("Primitives", "Null")
    return ("_SkipPattern", )

def boolean():
    if cust.allow_null:
        return ("Primitives", "Boolean")
    return ("_SkipPattern", )