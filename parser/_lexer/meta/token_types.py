"""Meta-programming go brrrrrrrrrrrrrrrrrrrrr"""

import itertools
import pathlib
import sys
import dotenv_vault
import os

from backend import errors
from parser._lexer.data.aliases import ALIASES

CLASS_NAME = "TokenType"

dotenv_vault.load_dotenv()
if not (ROOT_PATH := os.getenv("ROOT_PATH")):
    raise errors.InternalError("ROOT_PATH does not exist in .env")
sys.path.insert(0, ROOT_PATH)
GENERATED_FILE_PATH = (pathlib.Path(ROOT_PATH) / "parser" / "_lexer" / "token_types.py").resolve()

def resolve_enum(node):
    return f"InternalTokenType.{".".join(node)}"

def write_class(name, node, indent = 0):
    lines = []
    pad = " " * indent
    if isinstance(node, dict):
        lines.append("")
        lines.append(f"{pad}class {name}(TokenTypeEnum):")
        for k, v in node.items():
            lines += write_class(k, v, indent + 4)
        if not node:
            lines.append(f"{pad}    pass")
    elif isinstance(node, (tuple, list)):
        lines.append(f"{pad}{name} = {resolve_enum(node)}")
    elif isinstance(node, str):
        lines.append(f"{pad}{name} = InternalTokenType.{node}")
    else:
        raise TypeError(f"Invalid alias node: {node}")
    return lines

def get_shortcut_name(name: str):
    if name in ("Unary", "Binary", "Ternary"):
        return name + "Operators"
    if name in ("Lefty", "Righty"):
        return name + "AugmentedAssignOpers"
    return name

def write_shortcuts(prefix: str = "TokenType", dct: dict = ALIASES, variable_set = None) -> tuple[list[str], set]:
    lines = []
    variable_set = variable_set or set()
    for k, v in dct.items():
        if isinstance(v, dict):
            variable_set.add(get_shortcut_name(k))
            lines.append(f"{get_shortcut_name(k)} = {prefix}.{k}")
            extras, variable_set = write_shortcuts(k, v, variable_set)
            lines.extend(extras)
    return lines, variable_set

def write_all_array(variables) -> list[str]:
    lines = ["__all__ = ["]
    for i in itertools.chain([CLASS_NAME, "TokenTypeEnum"], variables):
        lines.append(f'    "{i}",')
    lines.append("]")
    return lines

def write_file():
    lines = [
        "# Auto-generated token_types.py for IntelliSense",
        "# Beep bop",
        "from parser._lexer.internal_token_types import InternalTokenType",
        "import enum", 
        "",
        "class TokenTypeEnum(enum.Enum):",
        "    pass"
    ]
    
    lines += write_class(CLASS_NAME, ALIASES)
    lines.append("")
    l, variables = write_shortcuts(CLASS_NAME)
    lines += l
    lines.append("")
    lines += write_all_array(variables)

    with open("parser/_lexer/token_types.py", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    write_file()