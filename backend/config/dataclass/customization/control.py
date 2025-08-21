from dataclasses import dataclass
import typing

from backend.config.baseclasses import CustomDataclass, ConfigDescriptor, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class ClassicConditionalSyntaxConfigCls(CustomDataclass):
    conditional: ConfigDescriptor[typing.Literal["if"]] = ConfigDescriptor(_UNFILLED, "if")
    fallback_with_condition: ConfigDescriptor[typing.Literal["elseif", "else if", "elif", "elsif", "perchance", "assuming", "but what about if"]] = ConfigDescriptor(_UNFILLED, "elif")
    fallback: ConfigDescriptor[typing.Literal["else", "otherwise"]] = ConfigDescriptor(_UNFILLED, "else")

@dataclass(frozen=True, kw_only=True)
class ClassicConditionalConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[ClassicConditionalSyntaxConfigCls] = ConfigDescriptor(_UNFILLED, ClassicConditionalSyntaxConfigCls())

@dataclass(frozen=True, kw_only=True)
class MatchCaseSyntaxConfigCls(CustomDataclass):
    default_case_notation: ConfigDescriptor[typing.Literal["default", "_", "*"]] = ConfigDescriptor(_UNFILLED, "_")
    statement: ConfigDescriptor[typing.Literal["switch", "match", "compare"]] = ConfigDescriptor(_UNFILLED, "match")

@dataclass(frozen=True, kw_only=True)
class MatchCasePatternMatchingConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class MatchCaseConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    pattern_matching: ConfigDescriptor[MatchCasePatternMatchingConfigCls] = ConfigDescriptor(_UNFILLED, MatchCasePatternMatchingConfigCls())
    syntax: ConfigDescriptor[MatchCaseSyntaxConfigCls] = ConfigDescriptor(_UNFILLED, MatchCaseSyntaxConfigCls())

@dataclass(frozen=True, kw_only=True)
class TryStatementConfigCls(CustomDataclass):
    syntax: ConfigDescriptor[typing.Literal["try"]] = ConfigDescriptor(_UNFILLED, "try")

@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingClauseConfigCls(CustomDataclass):
    syntax: ConfigDescriptor[typing.Literal["catch", "except", "rescue"]] = ConfigDescriptor(_UNFILLED, "catch")
    optional_error_binding: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseSyntaxConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["else", "otherwise"]] = ConfigDescriptor(_UNFILLED, "else")

@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["else", "otherwise"]] = ConfigDescriptor(_UNFILLED, "else")

@dataclass(frozen=True, kw_only=True)
class FinalCleanupClauseConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["finally", "ensure"]] = ConfigDescriptor(_UNFILLED, "finally")

@dataclass(frozen=True, kw_only=True)
class ThrowErrorConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    syntax: ConfigDescriptor[typing.Literal["die", "throw", "raise", "panic"]] = ConfigDescriptor(_UNFILLED, "throw")

@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)
    try_statement: ConfigDescriptor[TryStatementConfigCls] = ConfigDescriptor(_UNFILLED, TryStatementConfigCls())
    exception_handling: ConfigDescriptor[ExceptionHandlingClauseConfigCls] = ConfigDescriptor(_UNFILLED, ExceptionHandlingClauseConfigCls())
    no_exceptions: ConfigDescriptor[NoExceptionClauseConfigCls] = ConfigDescriptor(_UNFILLED, NoExceptionClauseConfigCls())
    final_cleanup: ConfigDescriptor[FinalCleanupClauseConfigCls] = ConfigDescriptor(_UNFILLED, FinalCleanupClauseConfigCls())
    throw_error: ConfigDescriptor[ThrowErrorConfigCls] = ConfigDescriptor(_UNFILLED, ThrowErrorConfigCls())

@dataclass(frozen=True, kw_only=True)
class JumpingConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class ControlFlowConfigCls(CustomDataclass):
    conditional: ConfigDescriptor[ClassicConditionalConfigCls] = ConfigDescriptor(_UNFILLED, ClassicConditionalConfigCls())
    match_case: ConfigDescriptor[MatchCaseConfigCls] = ConfigDescriptor(_UNFILLED, MatchCaseConfigCls())
    exception_handling: ConfigDescriptor[ExceptionHandlingConfigCls] = ConfigDescriptor(_UNFILLED, ExceptionHandlingConfigCls())
    jumping: ConfigDescriptor[JumpingConfigCls] = ConfigDescriptor(_UNFILLED, JumpingConfigCls())