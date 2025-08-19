from backend import errors
from backend.config import CONFIG, CustomizationMode

inverted = CONFIG.templates.inverted_comparisons

def eq():
    if inverted.value:
        return ("Templates", "InvertedComparisons", "Equality")
    return ("_SkipPattern",)

def ge():
    if inverted.value:
        return ("Templates", "InvertedComparisons", "GreaterThanOrEqualTo")
    return ("_SkipPattern",)

def le():
    if inverted.value:
        return ("Templates", "InvertedComparisons", "LessThanOrEqualTo")
    return ("_SkipPattern",)

def gt():
    if inverted.value:
        return ("Templates", "InvertedComparisons", "GreaterThan")
    return ("_SkipPattern",)

def lt():
    if inverted.value:
        return ("Templates", "InvertedComparisons", "LessThan")
    return ("_SkipPattern",)