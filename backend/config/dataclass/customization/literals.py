import typing
from dataclasses import dataclass
from backend.config.baseclasses import CustomDataclass

@CustomDataclass
@dataclass(frozen=True, kw_only=True)
class NumberLiterals:
    enabled: bool = True

@dataclass(frozen=True, kw_only=True)
class BooleanLiterals:
    pass

@dataclass(frozen=True, kw_only=True)
class NullLiterals:
    pass

@dataclass(frozen=True, kw_only=True)
class StringLiterals:
    pass

@dataclass(frozen=True, kw_only=True)
class EllipsisLiterals:
    pass

@dataclass(frozen=True, kw_only=True)
class LiteralsCls:
    numbers: NumberLiterals = NumberLiterals()