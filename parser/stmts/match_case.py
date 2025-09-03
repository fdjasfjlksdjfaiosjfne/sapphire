import typing
from backend import errors
import parser.nodes as Nodes
from lexer import TokenType, MatchCase, Parentheses
from parser.core import ParserNamespaceSkeleton

class MatchCaseStatement(ParserNamespaceSkeleton):
    def _parse_match_case_stmt(self, **context) -> Nodes.MatchCaseNode:
        self._advance([MatchCase.Match])
        subject = self._parse_expr(**context)
        self._advance([Parentheses.OpenCurlyBrace])
        cases = []
        while self._peek().type != Parentheses.CloseCurlyBrace:
            cases.append(self.__parse_case_stmt(**context))
        self._advance([Parentheses.CloseCurlyBrace])
        return Nodes.MatchCaseNode(subject, cases)

    def __parse_case_stmt(self, **context) -> Nodes.CaseNode:
        if self._peek().type == MatchCase.DefaultCase and self._peek().value == "default":
            self._advance([MatchCase.DefaultCase])
            pattern = Nodes.WildcardPatternNode()
        else:
            self._advance([MatchCase.Case])
            pattern = self.__parse_match_pattern(**context)
        
        guard = None
        if self._peek().type == MatchCase.ConditionGuard:
            self._advance([MatchCase.ConditionGuard], error = errors.InternalError(
                "A redundant check for the 'if' token has been tripped\n"
                f"Location: {self.__parse_case_stmt.__qualname__}"
            ))
            guard = self._parse_expr(**context)

        body = self._parse_attached_code_block(
            opening_token = TokenType.GDCologne,
            closing_token = MatchCase.Case,
            eat_closing_token = False,
            allow_single_line_code_blocks = True,
            **context
        )
        return Nodes.CaseNode(pattern, guard, body)

    def __parse_match_pattern(self, **context) -> Nodes.MatchPatternNode:
        pattern = self.__parse_or_pattern(**context)
        if self._peek().type == MatchCase.VariableBindingIntoPattern:
            self._advance([MatchCase.VariableBindingIntoPattern])
            name = self._advance(
                [TokenType.Identifier],
                errors.SyntaxError(
                    "Expecting an identifier"
                )
            ).value
            return Nodes.VariablePatternNode(pattern, name)
        return pattern

    def __parse_or_pattern(self, **context) -> (
            Nodes.MatchPatternNode | Nodes.MultipleChoicePatternNode
        ):
        patterns = [self.__parse_class_pattern(**context)]
        if self._peek().type == MatchCase.PatternSeparator:
            while self._peek().type == MatchCase.PatternSeparator:
                self._advance([MatchCase.PatternSeparator])
                patterns.append(self.__parse_class_pattern(**context))
            if len(patterns) > 1:
                return Nodes.MultipleChoicePatternNode(patterns)
        return patterns[0]

    def __parse_class_pattern(self, **context) -> (
            Nodes.MatchPatternNode | Nodes.ClassPatternNode):

        if self._peek().type == TokenType.Identifier and self._peek().type == Parentheses.OpenParen:
            name = self._advance([TokenType.Identifier])
            self._advance([Parentheses.OpenParen])
            args, kwargs = self.__parse_class_args(**context)
            return Nodes.ClassPatternNode(name.value, args, kwargs)
        return self.__parse_structural_match_patterns()

    def __parse_class_args(self, **context) -> (
            tuple[list[Nodes.MatchPatternNode], dict[str, Nodes.MatchPatternNode]]): # type: ignore
        self._advance([Parentheses.OpenParen], error = errors.InternalError(
            "MemberSubscriptionCall.parse_call_args() cannot find a '(' token, "
            "even though the only place that call it should've check for it beforehand."
            "This parsing function might be called via other ways."
        ))
        args = []
        kwargs = {}
        while self._peek().type == TokenType.Symbols.FunctionArgumentSeparator:
            # & Don't you dare delete this >:(
            self._advance([TokenType.Symbols.FunctionArgumentSeparator], error = errors.InternalError(
                "A redundant check for eating a comma has been tripped.\n"
                "If this is triggered without using a debugger, it could be either:\n"
                " 1. Solar bit flip\n"
                " 2. Trolling gremlins in your computer\n"
                " 3. We're all in a simulation\n"
                " 4. Python is smoking weed\n"
                " 5. (most likely) I mess up somewhere ;-;"
            ))
            if self._peek().type == Parentheses.CloseParen:
                break
            arg = self.__parse_match_pattern(**context)

            # $ Check for any keyword arguments
            if isinstance(arg, Nodes.IdentifierNode) and self._peek().type == TokenType.Symbols.KeywordFunctionArgumentAssignment:
                self._advance([TokenType.Symbols.KeywordFunctionArgumentAssignment], errors.InternalError(
                    "A redundant check for eating a '=' has been tripped."
                ))
                kwargs[arg.symbol] = self.__parse_match_pattern(**context)
                while self._peek().type == TokenType.Symbols.FunctionArgumentSeparator:
                    self._advance([TokenType.Symbols.FunctionArgumentSeparator], error = errors.InternalError(
                        "A redundant check eating a comma has been tripped."
                    ))
                    if self._peek().type == Parentheses.CloseParen:
                        break
                    key = self._advance([TokenType.Identifier], error = errors.SyntaxError(
                        "Expecting an identifier as the key for a keyword argument in a call expression"
                    )).value
                    self._advance([TokenType.Symbols.KeywordFunctionArgumentAssignment], error = errors.SyntaxError(
                        "Expecting '=' after the key for a keyword argument in a call expression"
                    ))
                    kwargs[key] = self.__parse_match_pattern(**context)
            else:
                args.append(arg)
            
            if kwargs:
                break

        self._advance([Parentheses.CloseParen], error = errors.SyntaxError(
            "')' for a call expression is not closed"
        ))
        return args, kwargs

    def __parse_structural_match_patterns(self, **context) -> (
            Nodes.MatchPatternNode
            | Nodes.SequencePatternNode
            | Nodes.MappingPatternNode):
        # > Code copied and modified from exprs/collections.py
        match self._peek():
            case Parentheses.OpenParen:
                self._advance([Parentheses.OpenParen])
                expr = self.__parse_match_pattern(**context)
                elements = [expr]
                while self._peek() == TokenType.Symbols.SequenceElementSeparator:
                    self._advance()
                    if self._peek() == Parentheses.CloseParen:
                        break
                    elements.append(self.__parse_match_pattern(**context))
                self._advance([Parentheses.CloseParen], error = errors.SyntaxError("'(' is not closed"))
                return Nodes.SequencePatternNode(
                        Nodes.SequencePatternType.Tuple, elements
                    )
            case Parentheses.OpenSquareBracket:
                self._advance([Parentheses.OpenSquareBracket])
                expr = self.__parse_match_pattern(**context)
                # $ This is a list
                elements = [expr]
                while self._peek() == TokenType.Symbols.SequenceElementSeparator:
                    self._advance()
                    if self._peek() == Parentheses.CloseSquareBracket:
                        break
                    elements.append(self.__parse_match_pattern(**context))
                self._advance([Parentheses.CloseSquareBracket], error = errors.SyntaxError("'[' is not closed"))
                return Nodes.SequencePatternNode(
                        Nodes.SequencePatternType.List, elements
                    )
            case Parentheses.OpenCurlyBrace:
                key_expr = self.__parse_match_pattern(**context)
                if self._peek() == TokenType.Symbols.KeyValueSeparatorInDict:
                    # $ Dict
                    self._advance()
                    val_expr = self.__parse_match_pattern(**context)
                    pairs = [(key_expr, val_expr)]
                    while self._peek() == TokenType.Symbols.SequenceElementSeparator:
                        self._advance()
                        if self._peek() == Parentheses.CloseCurlyBrace:
                            break
                        k = self.__parse_match_pattern(**context)
                        self._advance([TokenType.Symbols.SequenceElementSeparator])
                        v = self.__parse_match_pattern(**context)
                        pairs.append((k, v))
                    self._advance([Parentheses.CloseCurlyBrace], error = errors.SyntaxError("'{' is not closed"))
                    return Nodes.MappingPatternNode(pairs)
                else:
                    # $ Set
                    items = [key_expr]
                    while self._peek() == TokenType.Symbols.SequenceElementSeparator:
                        self._advance()
                        if self._peek() == Parentheses.CloseCurlyBrace:
                            break
                        items.append(self.__parse_match_pattern(**context))
                    self._advance([Parentheses.CloseCurlyBrace], error = errors.SyntaxError("'{' is not closed"))
                    return Nodes.SequencePatternNode(
                        Nodes.SequencePatternType.Set, items
                    )
            case _:
                return self.__parse_simple_match_patterns()

    def __parse_simple_match_patterns(self, **context) -> (
            Nodes.LiteralPatternNode 
            | Nodes.WildcardPatternNode
            | Nodes.VariablePatternNode
    ):
        match self._peek().type:
            case TokenType.Identifier:
                val = Nodes.IdentifierNode(self._advance().value)
            # You can't do MatchCase.attr for whatever reason
            case TokenType.Statements.MatchCase.DefaultCase if self._peek().value != "default":
                return Nodes.WildcardPatternNode()
            case TokenType.Statements.MatchCase.VariableBinding:
                name = self._advance(
                    [TokenType.Identifier], 
                    errors.SyntaxError(
                        "Expecting an identifier after 'let'"
                    )
                ).value
                return Nodes.VariablePatternNode(
                    pattern = Nodes.WildcardPatternNode(),
                    ident_name = name
                )

            case TokenType.Primitives.Int:
                val = Nodes.IntNode(int(self._advance().value))
            case TokenType.Primitives.Float:
                val = Nodes.FloatNode(float(self._advance().value))
            case TokenType.Primitives.String:
                val = Nodes.StrNode(self._advance().value)
            case TokenType.Primitives.Null:
                self._advance()
                val = Nodes.NullNode()
            case TokenType.Primitives.Boolean:
                val = Nodes.BoolNode(self._advance().value == "true")
            case _:
                raise errors.SyntaxError("Invalid expression in 'case' expression")
        return Nodes.LiteralPatternNode(val)