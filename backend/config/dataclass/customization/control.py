from dataclasses import dataclass
import typing

from backend.config.baseclasses import CustomDataclass

@dataclass(frozen=True, kw_only=True)
class ConditionalSyntaxConfigCls(CustomDataclass):
    conditional: typing.Literal["if"] = "if"
    fallback_with_condition: typing.Literal["elseif", "else if",
                                            "elif", "elsif",
                                            "perchance", "assuming",
                                            "but what about if"] = "elif"
    fallback: typing.Literal["else", "otherwise"] = "else"


@dataclass(frozen=True, kw_only=True)
class ConditionalConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: ConditionalSyntaxConfigCls = ConditionalSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class MatchCaseConfigCls(CustomDataclass):
    enabled: bool = True

@dataclass(frozen=True, kw_only=True)
class TryStatementConfigCls(CustomDataclass):
    syntax: typing.Literal["try"] = "try"

@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingClauseConfigCls(CustomDataclass):
    syntax: typing.Literal["catch", "except", "rescue"] = "catch"
    optional_error_binding: bool = True

@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseSyntaxConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["else", "otherwise"] = "else"

@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["else", "otherwise"] = "else"

@dataclass(frozen=True, kw_only=True)
class FinalCleanupClauseConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["finally", "ensure"] = "finally"

@dataclass(frozen=True, kw_only=True)
class ThrowErrorConfigCls(CustomDataclass):
    enabled: bool = True
    syntax: typing.Literal["die", "throw", "raise", "panic"] = "throw"

@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingConfigCls(CustomDataclass):
    enabled: bool = True
    try_statement: TryStatementConfigCls = TryStatementConfigCls()
    exception_handling: ExceptionHandlingClauseConfigCls = ExceptionHandlingClauseConfigCls()
    no_exceptions: NoExceptionClauseConfigCls = NoExceptionClauseConfigCls()
    final_cleanup: FinalCleanupClauseConfigCls = FinalCleanupClauseConfigCls()
    throw_error: ThrowErrorConfigCls = ThrowErrorConfigCls()

@dataclass(frozen=True, kw_only=True)
class JumpingConfigCls(CustomDataclass):
    enabled: bool = True

@dataclass(frozen=True, kw_only=True)
class ControlFlowConfigCls(CustomDataclass):
    conditional: ConditionalConfigCls = ConditionalConfigCls()
    match_case: MatchCaseConfigCls = MatchCaseConfigCls()
    exception_handling: ExceptionHandlingConfigCls = ExceptionHandlingConfigCls()
    jumping: JumpingConfigCls = JumpingConfigCls()