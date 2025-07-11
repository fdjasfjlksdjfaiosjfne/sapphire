"""Check for any common oversights that may or may not appear in any of the files here.
"""

import ast, typing, inspect, sys, types
from rich import print

class BaseBugChecker(ast.NodeVisitor):
    def __init__(self, file: str, source: types.ModuleType):
        self.file = file
        self.source = inspect.getsource(source)
        self.bugs = 0
        self.warnings = 0
        self.function_stack: list[str] = []
    
    def visit(self, node = None):
        if node is None:
            return super().visit(ast.parse(self.source))
        return super().visit(node)

    def print_error_msg(self, type, lineno, end_lineno, msg):
        line_range = f"{lineno}" if end_lineno == lineno else f"{lineno}-{end_lineno}"
        fn_stack = ""
        if len(self.function_stack) != 0:
            fn_stack = ", function "
            for i in self.function_stack:
                fn_stack += f"{i} >"
                fn_stack.removesuffix(" >")
        print(f"[red]{type} in line {line_range}, file '{self.file}'\nMessage: {msg}[/]")
    
    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        self.generic_visit(node)
        self.function_stack.pop()

class LexerBugChecker(BaseBugChecker):
    def __init__(self, source: types.ModuleType):
        super().__init__("parser/lexer.py", source)
        self.token_types: list[str] = []
    
    def visit_ClassDef(self, node):
        if node.name == "TokenType" and node.bases == [ast.Name("Enum", ast.Load())]:
            # $ TokenType enum class spotted
            for i in node.body:
                if isinstance(i, ast.Assign):
                    self.token_types.append(i.targets[0].id)
                    if not (isinstance(i.value, ast.Call) and isinstance(i.value.func, ast.Name) and i.value.func.id == "auto"):
                        warnings += 1
                        self.print_error_msg(
                            "Warning", i.lineno, i.end_lineno,
                            f"auto() not used in enum value {i.targets[0].id}"
                        )
        else:
            self.generic_visit(node)
    
    def visit_Assign(self, node):
        if node.targets[0] == "regex_patterns" and isinstance(node.value, ast.Dict):
            token_types_in_keys = []
            for key in node.value.keys:
                if (
                        isinstance(key, ast.Attribute) and 
                        isinstance(key.value, ast.Name) and 
                        isinstance(key.value, ast.Name) and key.value.id == "TokenType"
                   ):
                    token_types_in_keys.append(key.attr)
                else:
                    self.bugs += 1
                    self.print_error_msg(
                        "Bugs", key.lineno, key.end_lineno,
                        "Invalid key in regex_patterns"
                    )
            # ! If any of the token types on the enum does not have a
            # ! dedicated key in regex_patterns
            for type in self.token_types:
                if type not in token_types_in_keys:
                    self.bugs += 1
                    self.print_error_msg(
                        "Bugs", node.lineno, node.end_lineno,
                        f"TokenType.{type} does not have a dedicated key in 'regex_patterns'"
                    )
        else:
            self.generic_visit(node)

class ParserBugChecker(BaseBugChecker):
    def visit_FunctionDef(self, node: ast.FunctionDef):
        self.function_stack.append(node.name)

        # ^ Check whether 'tokens, ..., /'
        if not (len(node.args.posonlyargs) > 0 and node.args.posonlyargs[0].arg == "tokens"):
            self.bugs += 1
            self.print_error_msg(
                "Bug", 
                node.args.posonlyargs[0].lineno if len(node.args.posonlyargs) > 0 else node.lineno, 
                node.args.posonlyargs[0].end_lineno if len(node.args.posonlyargs) > 0 else node.end_lineno,
                "'tokens' is not the first positional-only argument"
            )
        # ^ Check whether there is a keyword variadic argument named **context
        if node.args.kwarg is None or node.args.kwarg.arg != "context":
            self.bugs += 1
            self.print_error_msg(
                "Bug", 
                node.args.kwarg.lineno if node.args.kwarg is not None else node.lineno,
                node.args.kwarg.end_lineno if node.args.kwarg is not None else node.end_lineno,
                f"There's no '**context' in function declaration of {node.name}"
            )

        self.generic_visit(node)
        self.function_stack.pop()
    
    def visit_Call(self, node):
        def get_func_name(func) -> str:
            if isinstance(func, ast.Attribute):
                return func.attr
            elif isinstance(func, ast.Name):
                return func.id

        func = node.func
        name = get_func_name(func)
        is_parse_fn = name.startswith("parse_")
        # ^ Check for the 'tokens' arg
        if is_parse_fn or name == "eat":
            if not (isinstance(node.args[0], ast.Name) and node.args[0].id == "tokens"):
                self.bugs += 1
                self.print_error_msg(
                    "Bug", node.lineno, node.end_lineno,
                    f"'tokens' not found in a parse call expresion"
                )
        
        # ^ Check for '**context' arg
        if is_parse_fn:
            for kwarg in node.keywords:
                if kwarg.arg is None and isinstance(kwarg.value, ast.Name) and kwarg.value.id == "context":
                    break
            else:
                self.bugs += 1
                self.print_error_msg(
                    "Bug", node.lineno, node.end_lineno, 
                    f"'**context' not added as an argument in a parsing function call ('{name}')"
                    )
        self.generic_visit(node)

class InterpreterBugChecker(BaseBugChecker):
    
    def visit_FunctionDef(self, node):
        self.function_stack.append(node.name)
        if len(node.args.posonlyargs) < 2 or node.args.posonlyargs[1].arg != "env":
            self.bugs += 1
            self.print_error_msg(
                "Bug",
                node.lineno if len(node.args.posonlyargs) < 2 else node.args.posonlyargs[1].lineno,
                node.end_lineno if len(node.args.posonlyargs) < 2 else node.args.posonlyargs[1].end_lineno,
                "There's no 'env' argument as the second, positional-only argument"
            )
        self.generic_visit(node)
        self.function_stack.pop()
    
    def visit_Call(self, node):
        def get_func_name(func) -> str:
            if isinstance(func, ast.Attribute):
                return func.attr
            elif isinstance(func, ast.Name):
                return func.id
            else:
                raise Exception(func)
        
        def is_eval_func(func) -> bool:
            if isinstance(func, ast.Attribute):
                if isinstance(func.value, ast.Name) and func.value.id in ("opers", "iops"):
                    return False
            return get_func_name(func).startswith("eval_")
        
        func = node.func
        name = get_func_name(func)
        # ^ Check for the 'tokens' arg
        if is_eval_func(func):
            if not (isinstance(node.args[1], ast.Name) and node.args[1].id == "env"):
                self.bugs += 1
                self.print_error_msg(
                    "Bug", node.args[0].lineno, node.args[0].end_lineno,
                    f"'env' is not passed to a eval call"
                )
        self.generic_visit(node)

def check():
    # ^ Lexer
    from parser import lexer
    lbc = LexerBugChecker(lexer)
    lbc.visit()

    # ^ Parser
    from parser.parsing import exprs, stmts, mem_sub_call
    for mod, path in {exprs: "parser/parsing/exprs.py", stmts: "parser/parsing/stmts.py", mem_sub_call: "parser/parsing/mem_sub_call.py"}.items():
        pbc = ParserBugChecker(path, mod)
        pbc.visit()
    
    # ^ Interperter
    from runtime.eval import exprs, stmts
    for mod, path in {exprs: "runtime/eval/exprs.py", stmts: "runtime/eval/stmts.py"}.items():
        ibc = InterpreterBugChecker(path, mod)
        ibc.visit()

    # ^ Total amount of bugs found
    if lbc.bugs or lbc.warnings or pbc.bugs or pbc.warnings or ibc.bugs or ibc.warnings:
        print(
            # & Multistringn't
            # & Why exactly does this work though?
            "[blue]In this codebase, there are a total of: [/]\n"
            f" - {lbc.bugs + pbc.bugs + ibc.bugs} [red]common bugs[/]\n"
            f"  + {lbc.bugs} from lexer\n"
            f"  + {pbc.bugs} from parser\n"
            f"  + {ibc.bugs} from interpreter\n"
            f" - {lbc.warnings + pbc.warnings + ibc.warnings} [yellow]common warnings[/]\n"
            f"  + {lbc.warnings} from lexer\n"
            f"  + {pbc.warnings} from parser\n"
            f"  + {ibc.warnings} from interpreter"
        )
    if pbc.bugs or lbc.bugs or ibc.bugs:
        print(f"[yellow]The program will now close.[/]")
        sys.exit(1)