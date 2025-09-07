from dataclasses import dataclass
import typing

from backend.config.dataclass.bases import CustomConfDatacls, ConfOptWrapper, _UNFILLED

@dataclass(frozen=True, kw_only=True)
class ClassicConditionalSyntaxConfigCls(CustomConfDatacls):
    conditional: ConfOptWrapper[typing.Literal["if"]] = ConfOptWrapper(_UNFILLED, "if")
    unless: ConfOptWrapper[typing.Literal["unless", "if not"]] = ConfOptWrapper(_UNFILLED, "unless")
    fallback_with_condition: ConfOptWrapper[typing.Literal["elseif", "else if", "elif", "elsif", "perchance", "assuming", "but what about if"]] = ConfOptWrapper(_UNFILLED, "elif")
    fallback: ConfOptWrapper[typing.Literal["else", "otherwise"]] = ConfOptWrapper(_UNFILLED, "else")

@dataclass(frozen=True, kw_only=True)
class ClassicConditionalConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    enable_inverted_if: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, False)
    syntax: ClassicConditionalSyntaxConfigCls = ClassicConditionalSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class MatchCaseSyntaxConfigCls(CustomConfDatacls):
    default_case_notation: ConfOptWrapper[typing.Literal["default", "_", "*"]] = ConfOptWrapper(_UNFILLED, "_")
    statement: ConfOptWrapper[typing.Literal["switch", "match", "compare"]] = ConfOptWrapper(_UNFILLED, "match")

@dataclass(frozen=True, kw_only=True)
class MatchCasePatternMatchingConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class MatchCaseConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    pattern_matching: MatchCasePatternMatchingConfigCls = MatchCasePatternMatchingConfigCls()
    syntax: MatchCaseSyntaxConfigCls = MatchCaseSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class SwitchCasePatternMatchingConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class SwitchCaseConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    pattern_matching: MatchCasePatternMatchingConfigCls = MatchCasePatternMatchingConfigCls()
    syntax: MatchCaseSyntaxConfigCls = MatchCaseSyntaxConfigCls()

@dataclass(frozen=True, kw_only=True)
class ConditionalConfigCls(CustomConfDatacls):
    classic: ClassicConditionalConfigCls = ClassicConditionalConfigCls()
    match_case: MatchCaseConfigCls = MatchCaseConfigCls()
    switch_case: SwitchCaseConfigCls = SwitchCaseConfigCls()

@dataclass(frozen=True, kw_only=True)
class TryStatementConfigCls(CustomConfDatacls):
    syntax: ConfOptWrapper[typing.Literal["try"]] = ConfOptWrapper(_UNFILLED, "try")

@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingClauseConfigCls(CustomConfDatacls):
    syntax: ConfOptWrapper[typing.Literal["catch", "except", "rescue"]] = ConfOptWrapper(_UNFILLED, "catch")
    optional_error_binding: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseSyntaxConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    syntax: ConfOptWrapper[typing.Literal["else", "otherwise"]] = ConfOptWrapper(_UNFILLED, "else")

@dataclass(frozen=True, kw_only=True)
class NoExceptionClauseConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    syntax: ConfOptWrapper[typing.Literal["else", "otherwise"]] = ConfOptWrapper(_UNFILLED, "else")

@dataclass(frozen=True, kw_only=True)
class FinalCleanupClauseConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    syntax: ConfOptWrapper[typing.Literal["finally", "ensure"]] = ConfOptWrapper(_UNFILLED, "finally")

@dataclass(frozen=True, kw_only=True)
class ThrowErrorConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    syntax: ConfOptWrapper[typing.Literal["die", "throw", "raise", "panic"]] = ConfOptWrapper(_UNFILLED, "throw")

@dataclass(frozen=True, kw_only=True)
class ExceptionHandlingConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)
    try_statement: TryStatementConfigCls = TryStatementConfigCls()
    exception_handling: ExceptionHandlingClauseConfigCls = ExceptionHandlingClauseConfigCls()
    no_exceptions: NoExceptionClauseConfigCls = NoExceptionClauseConfigCls()
    final_cleanup: FinalCleanupClauseConfigCls = FinalCleanupClauseConfigCls()
    throw_error: ThrowErrorConfigCls = ThrowErrorConfigCls()

@dataclass(frozen=True, kw_only=True)
class JumpingConfigCls(CustomConfDatacls):
    enabled: ConfOptWrapper[bool] = ConfOptWrapper(_UNFILLED, True)

@dataclass(frozen=True, kw_only=True)
class ControlFlowConfigCls(CustomConfDatacls):
    conditional: ConditionalConfigCls = ConditionalConfigCls()
    match_case: MatchCaseConfigCls = MatchCaseConfigCls()
    exception_handling: ExceptionHandlingConfigCls = ExceptionHandlingConfigCls()
    jumping: JumpingConfigCls = JumpingConfigCls()