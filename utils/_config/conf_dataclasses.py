import typing
import dataclasses
import enum
from utils._config.conf_base_classes import custom_dataclass

from backend import errors

LASTEST_VERSION = (0,0,4)
class CustomizationMode(enum.Enum):
    Disabled = 0
    Enabled = 1
    Forced = 2

@custom_dataclass
@dataclasses.dataclass(frozen = True)
class MultiLineComment:
    start: str = "/*"
    end: str = "*/"

@custom_dataclass
@dataclasses.dataclass(frozen = True)
class RedefineCls:
    floor_division: typing.Literal["//", "div", None] = "//"
    modulus: typing.Literal["%", "mod", None] = "%"
    inequality: typing.Literal["<>", "><", "!="] = "!="
    single_line_comment: typing.Union[str, None] = "#"
    multi_line_comment: typing.Optional[MultiLineComment] = MultiLineComment()
    throw_error: typing.Literal["throw", "raise", "die", "panic"] = "throw"
    match_case_statement: typing.Literal["match", "switch"] = "match"
    handle_exception_phrase: typing.Literal["catch", "except", "rescue"] = "catch"
    final_cleanup_of_exception_handling: typing.Literal["finally", "ensure"] = "finally"
    function_def: typing.Literal["def", "fn", "fun", "func", "function"] = "fn"
    class_def: typing.Literal["class", "cls"] = "class"
    else_if: typing.Literal["else if", "elseif", "elsif", "elif"] = "elif"
    spaceship_operator: typing.Literal["<=>", ">=<", None] = "<=>"
    true: str = "true"
    false: str = "false"
    null: str = "null"

@custom_dataclass
@dataclasses.dataclass(frozen = True)
class IntegerBaseLiterals:
    decimal: bool = True
    binary: bool = True
    octal: bool = True
    hexadecimal: bool = True

@custom_dataclass
@dataclasses.dataclass(frozen = True)
class CustomizationCls:
    redefine: RedefineCls = RedefineCls()
    code_blocks: typing.Literal["braces", "indentation", "end"] = "braces"
    binary_expression_notation: typing.Literal["infix", "prefix", "postfix"] = "infix"
    oop_model: typing.Literal["hybrid", "class", "prototype"] = "class"
    forced_encapsulation: bool = True
    encapsulation_method: typing.Literal["pythonic", "enforced"] = "enforced"
    default_case_notation: typing.Literal["*", "_", "default"] = "_"
    logical_operator_behavior: typing.Literal["boolean_only", "pythonic", "extended_pythonic"] = "extended_pythonic"
    allow_booleans: bool = True
    allow_null: bool = True
    case_insensitive_booleans: bool = True
    case_insensitive_null: bool = True
    mutable_value_assignment_behavior: typing.Literal["copy", "reference"] = "copy"
    mutable_argument_default_value_behavior: typing.Literal["copy", "reference"] = "copy"
    trailing_comma_policy: typing.Literal["always", "never", "single_tuple_only"] = "always"
    soft_keywords: bool = False
    semicolon_required: bool = False
    implicit_return: bool = False
    numeric_separator: bool = False
    integer_base_literals: IntegerBaseLiterals = IntegerBaseLiterals()
    string_delimeters: typing.List[typing.Literal["'", '"', "`"]] = dataclasses.field(default_factory = lambda: ['"', "'", "`"])
    allow_goto: bool = False
    implicit_globals: bool = False
    function_hoisting: bool = False
    type_annotations: bool = False
    multiline_strings: typing.Literal["disabled", "enabled", "default"] = "enabled"
    optional_catch_binding: bool = True
    scientific_notation: bool = True

@custom_dataclass
@dataclasses.dataclass(frozen=True)
class TemplateCls:
    inverted_comparisons: CustomizationMode = CustomizationMode.Disabled
    methify: CustomizationMode = CustomizationMode.Disabled

@custom_dataclass
@dataclasses.dataclass(frozen=True)
class ConfigCls:
    customization: CustomizationCls = CustomizationCls()
    templates: TemplateCls = TemplateCls()
    config_version: typing.Union[tuple[int, int, int], tuple[int, int, int, int]] = LASTEST_VERSION
    custom_options: dict = dataclasses.field(default_factory = dict)