import typing
from backend import errors
from backend.config import CONFIG
from backend.config.baseclasses import ConfOptWrapper

cust = CONFIG.customization
objects = cust.objects
literals = cust.literals
classic_conditional = cust.control_flow.conditional.classic
match_conditional = cust.control_flow.conditional.match_case
switch_conditional = cust.control_flow.conditional.switch_case
templates = CONFIG.templates

def _factory[ITTTuple: tuple[str, ...], Value: str](
                enable_flag: ConfOptWrapper[bool],
                syntax_flag: ConfOptWrapper[Value],
                dct: dict[Value, ITTTuple]) -> ITTTuple | tuple[typing.Literal["_SkipPattern"]]:
    if not enable_flag.get():
        return ("_SkipPattern",)
    try:
        return dct[syntax_flag.get()]
    except IndexError:
        raise errors.InternalError("Fill this later")

def null():
    if cust.literals.null.enabled:
        return ("Primitives", "Null")
    return ("_SkipPattern", )

def boolean():
    if cust.literals.booleans.enabled:
        return ("Primitives", "Boolean")
    return ("_SkipPattern", )