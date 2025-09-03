from backend import errors
from backend.config import CONFIG

inverted = CONFIG.templates.inverted_comparisons

def eq():
    if inverted != "disabled":
        return ("Templates", "InvertedComparisons", "Equality")
    return ("_SkipPattern",)

def ge():
    if inverted != "disabled":
        return ("Templates", "InvertedComparisons", "GreaterThanOrEqualTo")
    return ("_SkipPattern",)

def le():
    if inverted != "disabled":
        return ("Templates", "InvertedComparisons", "LessThanOrEqualTo")
    return ("_SkipPattern",)

def gt():
    if inverted != "disabled":
        return ("Templates", "InvertedComparisons", "GreaterThan")
    return ("_SkipPattern",)

def lt():
    if inverted != "disabled":
        return ("Templates", "InvertedComparisons", "LessThan")
    return ("_SkipPattern",)