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
    syntax: ClassicConditionalSyntaxConfigCls = ClassicConditionalSyntaxConfigCls()

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
    pattern_matching: MatchCasePatternMatchingConfigCls = MatchCasePatternMatchingConfigCls()
    syntax: MatchCaseSyntaxConfigCls = MatchCaseSyntaxConfigCls()

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
    try_statement: TryStatementConfigCls = TryStatementConfigCls()
    exception_handling: ExceptionHandlingClauseConfigCls = ExceptionHandlingClauseConfigCls()
    no_exceptions: NoExceptionClauseConfigCls = NoExceptionClauseConfigCls()
    final_cleanup: FinalCleanupClauseConfigCls = FinalCleanupClauseConfigCls()
    throw_error: ThrowErrorConfigCls = ThrowErrorConfigCls()

@dataclass(frozen=True, kw_only=True)
class JumpingConfigCls(CustomDataclass):
    enabled: ConfigDescriptor[bool] = ConfigDescriptor(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class ControlFlowConfigCls(CustomDataclass):
    conditional: ClassicConditionalConfigCls = ClassicConditionalConfigCls()
    match_case: MatchCaseConfigCls = MatchCaseConfigCls()
    exception_handling: ExceptionHandlingConfigCls = ExceptionHandlingConfigCls()
    jumping: JumpingConfigCls = JumpingConfigCls()