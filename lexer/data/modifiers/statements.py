from backend import errors
from backend.config import CONFIG
from backend.config.dataclass.bases import ConfOptWrapper
from backend.config.dataclass import control
from lexer.data.modifiers.base import _factory

cust = CONFIG.customization

# ! ===============================================================================================================================
# ! ======================================================== CONDITIONALS =========================================================
# ! ===============================================================================================================================

control_flow = cust.control_flow

SWITCH_MATCH = {
    "match": ("Keywords", "Match"),
    "switch": ("Keywords", "Switch")
}

# @ ==================================================== CLASSIC CONDITIONALS =====================================================

classic_cond = control_flow.conditional.classic

def if_():
    return _factory(
        classic_cond.enabled,
        classic_cond.syntax.conditional,
        {
            "if": ("Keywords", "If")
        }
    )

def unless():
    return _factory(
        classic_cond.enable_inverted_if,
        classic_cond.syntax.unless,
        {
            "unless": ("Keywords", "Unless"),
            "if not": ("Keywords", "IfNot")
        }
    )

def elif_():
    return _factory(
        classic_cond.enabled,
        classic_cond.syntax.fallback_with_condition,
        {
            "elif": ("Keywords", "Elif"),
            "elsif": ("Keywords", "Elsif"),
            "else if": ("Keywords", "ElseIf"),
            "elseif": ("Keywords", "Elseif"),
            "perchance": ("Keywords", "Perchance"),
            "assuming": ("Keywords", "Assuming"),
            "but what about if": ("Keywords", "ButWhatAboutIf")
        }
    )

def else_():
    return _factory(
        classic_cond.enabled,
        classic_cond.syntax.fallback,
        {
            "else": ("Keywords", "Else"),
            "otherwise": ("Keywords", "Otherwise")
        }
    )

# @ =================================================== MATCH-CASE CONDITIONALS ===================================================

match_conditional = control_flow.conditional.match_case

def match():
    return _factory(
        match_conditional.enabled,
        match_conditional.syntax.statement,
        SWITCH_MATCH
    )

def match_default_case():
    return _factory(
        match_conditional.enabled,
        match_conditional.syntax.default_case_notation,
        {
            "*": ("Symbols", "Asterisk"),
            "_": ("Symbols", "Underscore"),
            "default": ("Symbols", "Default")
        }
    )

# @ ================================================== SWITCH-CASE CONDITIONALS ===================================================

switch_conditional = control_flow.conditional.switch_case

def switch():
    return _factory(
        switch_conditional.enabled,
        switch_conditional.syntax.statement,
        SWITCH_MATCH
    )

def switch_default_case():
    return _factory(
        switch_conditional.enabled,
        switch_conditional.syntax.default_case_notation,
        {
            "*": ("Symbols", "Asterisk"),
            "_": ("Symbols", "Underscore"),
            "default": ("Symbols", "Default")
        }
    )

# ! ===============================================================================================================================
# ! ===================================================== EXCEPTION HANDLING ======================================================
# ! ===============================================================================================================================

eh = control_flow.exception_handling

def try_():
    return _factory(
        eh.enabled,
        eh.try_statement.syntax,
        {
            "try": ("Keywords", "Try")
        }
    )

def catch_expections():
    return _factory(
        eh.enabled,
        eh.exception_handling.syntax,
        {
            "except": ("Keywords", "Except"),
            "catch": ("Keywords", "Catch"),
            "rescue": ("Keywords", "Rescue"),
        }
    )

def no_exceptions():
    return _factory(
        # & The False here is just a placebo
        ConfOptWrapper(eh.enabled and eh.no_exceptions.enabled, False),
        eh.no_exceptions.syntax,
        {
            "else": ("Keywords", "Else")
        }
    )

def final_cleanup():
    return _factory(
        # & The False here is just a placebo
        ConfOptWrapper(eh.enabled.get() and eh.final_cleanup.enabled.get(), False),
        eh.final_cleanup.syntax,
        {
            "finally": ("Keywords", "Finally"),
            "ensure": ("Keywords", "Ensure")
        }
    )

def throw_error():
    return _factory(
        # & The False here is just a placebo
        ConfOptWrapper(eh.enabled.get() and eh.throw_error.enabled.get(), False),
        eh.throw_error.syntax,
        {
            "throw": ("Keywords", "Throw"),
            "raise": ("Keywords", "Raise")
        }
    )

# ! ===============================================================================================================================
# ! ======================================================== DECLARATIONS =========================================================
# ! ===============================================================================================================================

objs = cust.objects

def function_decl():
    return _factory(
        # There isn't a enable config for this, use a placebo
        ConfOptWrapper(True, True),
        objs.functions.syntax.keyword,
        {
            "fn": ("Keywords", "Fn"),
            "fun": ("Keywords", "Fun"),
            "func": ("Keywords", "Func"),
            "function": ("Keywords", "Function"),
            "def": ("Keywords", "Def")
        }
    )

def class_decl():
    return _factory(
        # There isn't a enable config for this, use a placebo
        ConfOptWrapper(True, True),
        objs.classes.syntax,
        {
            "class": ("Keywords", "Class"),
            "cls": ("Keywords", "Cls")
        }
    )

def enum_decl():
    return _factory(
        # There isn't a enable config for this, use a placebo
        ConfOptWrapper(True, True),
        objs.enums.syntax,
        {
            "enum": ("Keywords", "Enum")
        }
    )