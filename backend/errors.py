class SapphireError(BaseException):
    pass

class ValueError(SapphireError):
    pass

class AttributeError(SapphireError):
    pass

class InternalError(SapphireError):
    pass

class SyntaxError(SapphireError):
    pass

class VariableError(SapphireError):
    pass

class TypeError(SapphireError):
    pass

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

class StopIteration(SapphireError):
    pass