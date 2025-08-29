"""A module containing constant path variables, representing the files in the repository."""

from logging.handlers import RotatingFileHandler
import pathlib

from backend import errors
from backend.config import CONFIG

current_path = pathlib.Path(__file__)
ROOT = current_path.parent.parent

# ^ Root folders
INTERPRETER_FOLDER = ROOT / "interpreter"
TESTS_FOLDER = ROOT / "tests"
MAIN_FILE = ROOT / "main.py"
REPL_FILE = ROOT / "repl.py"

# ^ Backend and subfolders
BACKEND_FOLDER = ROOT / "backend"
CONFIG_FOLDER = BACKEND_FOLDER / "config"
MAIN_CONFIG_FILE = CONFIG_FOLDER / "__init__.py"
CHECKS_CONFIG_FILE = CONFIG_FOLDER / "checks"
DATACLASSES_CONFIG_FILE = CONFIG_FOLDER / "dataclass"
MAIN_CONFIG_SCHEMA = CONFIG_FOLDER / "sapconfig.schema.json"

CONFIG_SUBSCHEMAS = CONFIG_FOLDER / "subschemas"


LOCALES_FOLDER = BACKEND_FOLDER / "locales"

INTERNAL_COVERAGE_FOLDER = BACKEND_FOLDER / "coverage"
MAIN_INTERNAL_COVERAGE_FILE = INTERNAL_COVERAGE_FOLDER / "__init__.py"

ERRORS = BACKEND_FOLDER / "errors.py"
PATHS = BACKEND_FOLDER / "paths.py"

# ^ Parser and subfolders
PARSER_FOLDER = ROOT / "parser"
PARSE_EXPRS_FOLDER = PARSER_FOLDER / "exprs"

LEXER_FOLDER = PARSER_FOLDER / "lexer"
INTERNAL_TOKEN_TYPES = LEXER_FOLDER / "internal_token_types.py"
TOKEN_TYPES = LEXER_FOLDER / "token_types.py"

PARSE_STMTS_FOLDER = PARSER_FOLDER / "stmts"
PARSER = PARSER_FOLDER / "parser.py"