"""A module containing constant path variables, representing the files in the repository."""

import pathlib

from backend import errors

current_path = pathlib.Path(__file__)
ROOT = current_path.parent.parent

# ^ Root folders
INTERPRETER_FOLDER = current_path / "interpreter"
TESTS_FOLDER = current_path / "tests"
MAIN_FILE = current_path / "main.py"
REPL_FILE = current_path / "repl.py"

# ^ Backend and subfolders
BACKEND_FOLDER = current_path / "backend"
CONFIG_FOLDER = BACKEND_FOLDER / "config"
MAIN_CONFIG_FILE = CONFIG_FOLDER / "__init__.py"
CHECKS_CONFIG_FILE = CONFIG_FOLDER / "checks"
DATACLASSES_CONFIG_FILE = CONFIG_FOLDER / "dataclass"

CONFIG_SCHEMAS = CONFIG_FOLDER / "schemas"

LOCALES_FOLDER = BACKEND_FOLDER / "locales"

INTERNAL_COVERAGE_FOLDER = BACKEND_FOLDER / "coverage"
MAIN_INTERNAL_COVERAGE_FILE = INTERNAL_COVERAGE_FOLDER / "__init__.py"

ERRORS = BACKEND_FOLDER / "errors.py"
PATHS = BACKEND_FOLDER / "paths.py"

# ^ Parser and subfolders
PARSER_FOLDER = current_path / "parser"
PARSE_EXPRS_FOLDER = PARSER_FOLDER / "exprs"

LEXER_FOLDER = PARSER_FOLDER / "lexer"
INTERNAL_TOKEN_TYPES = LEXER_FOLDER / "internal_token_types.py"
TOKEN_TYPES = LEXER_FOLDER / "token_types.py"

PARSE_STMTS_FOLDER = PARSER_FOLDER / "stmts"
PARSER = PARSER_FOLDER / "parser.py"

# ^ Extra coverage
for v in globals().values():
    if not isinstance(v, pathlib.Path):
        continue

    # ! If the path does not exist...
    if not v.exists():
        raise errors.InternalError(
            f"It seems that {v!s} does not exist. Did you forgot to modify the paths database "
            "after changing the folder structure again?"
        )