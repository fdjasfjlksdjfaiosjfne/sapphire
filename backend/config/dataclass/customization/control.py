from dataclasses import dataclass
import typing

from backend.config.baseclasses import custom_dataclass

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ConditionalSyntaxConfigCls:
    conditional: typing.Literal["if"] = "if"
    fallback_with_condition: typing.Literal["elseif", "else if",
                                            "elif", "elsif",
                                            "perchance", "assuming",
                                            "but what about if"] = "elif"
    fallback: typing.Literal["else", "otherwise"] = "else"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ConditionalConfigCls:
    enabled: bool = True
    syntax: ConditionalSyntaxConfigCls = ConditionalSyntaxConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class MatchCaseConfigCls:
    enabled: bool = True

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class TryStatementConfigCls:
    syntax: typing.Literal["try"] = "try"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingClauseConfigCls:
    syntax: typing.Literal["catch", "except", "rescue"] = "catch"
    optional_error_binding: bool = True

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseConfigCls:
    enabled: bool = True
    syntax: typing.Literal["else", "otherwise"] = "else"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class FinalCleanupClauseConfigCls:
    enabled: bool = True
    syntax: typing.Literal["finally", "ensure"] = "finally"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ThrowErrorConfigCls:
    enabled: bool = True
    syntax: typing.Literal["die", "throw", "raise", "panic"] = "throw"

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingConfigCls:
    enabled: bool = True
    try_statement: TryStatementConfigCls = TryStatementConfigCls()
    exception_handling: ExceptionHandlingClauseConfigCls = ExceptionHandlingClauseConfigCls()
    no_exceptions: NoExceptionClauseConfigCls = NoExceptionClauseConfigCls()
    final_cleanup: FinalCleanupClauseConfigCls = FinalCleanupClauseConfigCls()
    throw_error: ThrowErrorConfigCls = ThrowErrorConfigCls()

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class JumpingConfigCls:
    enabled: bool = True

@custom_dataclass
@dataclass(frozen=True, kw_only=True)
class ControlFlowConfigCls:
    conditional: ConditionalConfigCls = ConditionalConfigCls()
    match_case: MatchCaseConfigCls = MatchCaseConfigCls()
    exception_handling: ExceptionHandlingConfigCls = ExceptionHandlingConfigCls()
    jumping: JumpingConfigCls = JumpingConfigCls()