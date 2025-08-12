class BaseSapphireError(Exception):
    _default_msg: str
    def __new__(cls, *args):
        if len(args) == 0 and hasattr(cls, "_default_msg"):
            args = [cls._default_msg]
        return super().__new__(cls, *args)

class SapphireBaseExceptionGroup(ExceptionGroup):
    pass

class SapphireExceptionGroup(SapphireBaseExceptionGroup):
    pass

class InternalError(BaseSapphireError):
    """
    Thrown when an error has been determined as a internal issue in the interpreter.
    """
    pass

class InProgress(InternalError):
    _default_msg = "TBA"

class SapphireError(BaseSapphireError):
    pass

class ValueError(SapphireError):
    pass

class AttributeError(SapphireError):
    pass

class SyntaxError(SapphireError):
    _default_msg = "Invalid syntax"

class VariableError(SapphireError):
    pass

class TypeError(SapphireError):
    _default_msg = "Default type"

class DivisionByZeroError(SapphireError):
    pass

class ArgumentError(SapphireError):
    pass

class BreakLoop(SapphireError):
    pass

class ContinueLoop(SapphireError):
    pass

class ReturnValue(SapphireError):
    pass

class ConfigError(SapphireError):
    pass

class _Backtrack(SapphireError):
    """Signal that parsing should be backtrack to a previous state"""
    _default_msg = (
        "If you see this error getting thrown in the wild, the parser is fucked. "
        "Completely fucked. Fucked to the point that it's not even 'InternalError'"
        "anymore. That's all I can say. Translation: i suck at making langs"
    )

class StopIteration(SapphireError):
    _default_msg = "StopIteration"