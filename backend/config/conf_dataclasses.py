import typing
import dataclasses
import enum
from backend.config.conf_base_classes import custom_dataclass
from backend import errors


class CustomizationMode(enum.Enum):
    Disabled = 0
    Enabled = 1
    Forced = 2

# @custom_dataclass
# @dataclasses.dataclass(frozen = True)
# class MultiLineComment:
#     start: str = "/*"
#     end: str = "*/"

# @custom_dataclass
# @dataclasses.dataclass(frozen = True, kw_only = True)
# class CommentRedefineCls:
#     single_line_comment: typing.Optional[str] = "#"
#     multi_line_comment: typing.Optional[MultiLineComment] = MultiLineComment()

# @custom_dataclass
# @dataclasses.dataclass(frozen = True, kw_only = True)
# class OperatorRedefineCls:
#     floor_division: typing.Literal["//", "div", None] = "//"
#     modulus: typing.Literal["%", "mod", None] = "%"
#     equality: typing.Literal["==", "==="] = "=="
#     loose_equality: typing.Literal["~=", "=="] = "~="
#     inequality: typing.Literal["<>", "><", "!=", "!=="] = "!="
#     spaceship_operator: typing.Literal["<=>", ">=<", None] = "<=>"


# @custom_dataclass
# @dataclasses.dataclass(frozen = True, kw_only = True)
# class ControlRedefineCls:
#     throw_error: typing.Literal["throw", "raise", "die", "panic"] = "throw"
#     match_case_statement: typing.Literal["match", "switch"] = "match"
#     handle_exception_phrase: typing.Literal["catch", "except", "rescue"] = "catch"
#     final_cleanup_of_exception_handling: typing.Literal["finally", "ensure"] = "finally"
#     function_def: typing.Literal["def", "fn", "fun", "func", "function"] = "fn"
#     class_def: typing.Literal["class", "cls"] = "class"
#     else_if: typing.Literal["else if", "elseif", "elsif", "elif"] = "elif"

# @custom_dataclass
# @dataclasses.dataclass(frozen = True, kw_only = True)
# class RedefineCls:
#     true: str = "true"
#     false: str = "false"
#     null: str = "null"
#     operators: OperatorRedefineCls = OperatorRedefineCls()

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class IntegerBaseLiterals:
    decimal: bool = True
    binary: bool = True
    octal: bool = True
    hexadecimal: bool = True

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class SyntaxCustomizationCls:
    trailing_comma_policy: typing.Literal["always", "never", "single_tuple_only"] = "always"
    code_blocks: typing.Literal["braces", "indentation", "end"] = "braces"
    binary_expression_notation: typing.Literal["infix", "prefix", "postfix"] = "infix"
    multiline_strings: typing.Literal["disabled", "enabled", "default"] = "enabled"
    implicit_return: bool = False
    string_delimeters: list[typing.Literal["'", '"', "`"]] = dataclasses.field(default_factory = lambda: ['"', "'", "`"])
    semicolon_required: bool = False
    soft_keywords: bool = False

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class OOPCustomizationCls:
    oop_model: typing.Literal["hybrid", "class", "prototype"] = "class"
    forced_encapsulation: bool = True
    encapsulation_method: typing.Literal["pythonic", "enforced"] = "enforced"

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class AnnotationCustomizationCls:
    type_annotations: bool = True

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class ControlFlowCustomizationCls:
    allow_goto: bool = False
    allow_pattern_matching_in_match_case_statement: bool = False
    optional_catch_binding: bool = True

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class VariableCustomizationCls:
    implicit_globals: bool = False
    function_hoisting: bool = False

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class LiteralCustomizationCls:
    numeric_separator: bool = False
    integer_base_literals: IntegerBaseLiterals = IntegerBaseLiterals()
    allow_booleans: bool = True
    allow_null: bool = True
    case_insensitive_booleans: bool = True
    case_insensitive_null: bool = True
    scientific_notation: bool = True

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class AssignmentCustomizationCls:
    mutable_value_assignment_behavior: typing.Literal["copy", "reference"] = "copy"
    mutable_argument_default_value_behavior: typing.Literal["copy", "reference"] = "copy"

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class OperatorCustomizationCls:
    logical_operator_behavior: typing.Literal["boolean_only", "pythonic", "extended_pythonic"] = "extended_pythonic"
    loose_equality: bool = False

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class UncategorizedCustomizationCls:
    pass

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class CustomizationCls:
    syntax: SyntaxCustomizationCls = SyntaxCustomizationCls()
    annotations: AnnotationCustomizationCls = AnnotationCustomizationCls()
    assignments: AssignmentCustomizationCls = AssignmentCustomizationCls()
    literals: LiteralCustomizationCls = LiteralCustomizationCls()
    oop: OOPCustomizationCls = OOPCustomizationCls()
    operators: OperatorCustomizationCls = OperatorCustomizationCls()
    syntax: SyntaxCustomizationCls = SyntaxCustomizationCls()
    uncategorized: UncategorizedCustomizationCls = UncategorizedCustomizationCls()

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class TemplateCls:
    inverted_comparisons: CustomizationMode = CustomizationMode.Disabled
    methify: CustomizationMode = CustomizationMode.Disabled

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class ConfigVersionCls:
    major: int = 0
    minor: int = 0
    patch: int = 0
    phase: typing.Literal["indev", "alpha", "beta", "release"] = "indev"

@custom_dataclass
@dataclasses.dataclass(frozen = True, kw_only = True)
class ConfigCls:
    customization: CustomizationCls = CustomizationCls()
    templates: TemplateCls = TemplateCls()
    config_version: ConfigVersionCls = ConfigVersionCls()
    custom_options: dict = dataclasses.field(default_factory = dict)

