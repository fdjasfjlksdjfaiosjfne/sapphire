import typing
from backend import errors
from parser.core import ParserNamespaceSkeleton
from lexer import TokenType, TokenTypeSequence, Parentheses
import parser.nodes as Nodes
class Collections(ParserNamespaceSkeleton):
    def _parse_collections_expr(
            self, 
            allow_explicit_tuple = False,
            allow_implicit_tuple = False,
            **context
            ) -> (
            Nodes.ListNode |
            Nodes.TupleNode |
            Nodes.SetNode |
            Nodes.ListComprehensionNode |
            Nodes.GeneratorComprehensionNode |
            Nodes.SetComprehensionNode |
            Nodes.DictComprehensionNode |
            Nodes.ExprNode
        ):
        match self._peek().type:
            case _ if allow_explicit_tuple and self._peek(1).type == TokenType.Symbols.SequenceElementSeparator:
                # $ This is a tuple WITH parentheses
                # $ In this case, this function is call from:
                # > parse_primary_expr(), on the branch that parse parenthesis
                # $ The ( is already consumed, so we don't have to remove it now

                # ? Now removing 'in_parentheses'
                # $ The only place that gives 'allow_explicit_tuple' should also gives 'in_parentheses' anyway
                context.pop("in_parentheses", None)
                elements = [self._parse_expr()]
                while self._peek().type == TokenType.Symbols.SequenceElementSeparator:
                    self._advance()
                    if self._peek().type == Parentheses.CloseParenthesis:
                        break
                    elements.append(self._parse_expr(**context))
                # @ DO NOT EAT THE ')' TOKEN
                # $ As of now, the self.parse_primary_expr() function that call this one is still waiting for the expression
                # $ And then it will eat the ')' token
                # ! Eat it now will break everything
                return Nodes.TupleNode(elements)
            case _ if allow_implicit_tuple and self._peek(1) == TokenType.Symbols.SequenceElementSeparator:
                elements = [self._parse_expr()]
                while self._peek() == TokenType.Symbols.SequenceElementSeparator:
                    self._advance()
                    elements.append(self._parse_expr(**context))
                return Nodes.TupleNode(elements)
            case Parentheses.OpenSquareBracket:
                return self._parse_comma_separated_values(
                    Parentheses.OpenSquareBracket,
                    Parentheses.CloseSquareBracket,
                    normal_wrapper = Nodes.ListNode,
                    comprehension_wrapper = Nodes.ListComprehensionNode,
                    not_closing_error = errors.SyntaxError(
                            "'[' is not closed"
                    )
                )
            case Parentheses.OpenCurlyBrace:
                self._advance([Parentheses.OpenCurlyBrace])
                key_expr = self._parse_expr(**context)
                if self._peek() == TokenType.Symbols.KeyValueSeparatorInDict:
                    # $ A dictionary...is it a comprehension, though?
                    self._advance()
                    val_expr = self._parse_expr(**context)
                    def _():
                        k = self._parse_expr(**context)
                        self._advance(TokenType.Symbols.KeyValueSeparatorInDict)
                        return k, self._parse_expr(**context)

                    return self._parse_comma_separated_values(
                        Parentheses.OpenCurlyBrace,
                        Parentheses.CloseCurlyBrace,
                        parsing_fn = _,
                        normal_wrapper = Nodes.DictNode,
                        comprehension_wrapper = Nodes.DictComprehensionNode,
                        not_closing_error = errors.SyntaxError(
                            "'{' is not closed"
                        ),
                        elements = [(key_expr, val_expr)]
                    )
                else:
                    return self._parse_comma_separated_values(
                        Parentheses.OpenCurlyBrace,
                        Parentheses.CloseCurlyBrace,
                        normal_wrapper = Nodes.SetNode,
                        comprehension_wrapper = Nodes.SetComprehensionNode,
                        not_closing_error = errors.SyntaxError(
                            "'{' is not closed"
                        ),
                        elements = [key_expr]
                    )
            case _:
                return self._parse_walrus_assignment_expr(**context)

    def _parse_comma_separated_values[
            NormalWrapper: Nodes.ListNode | Nodes.TupleNode | Nodes.SetNode | Nodes.DictNode, 
            ComprehensionWrapper: (
                Nodes.SequenceComprehensionNode 
                | Nodes.DictComprehensionNode
            )](
                self,
                opening_token_types: TokenTypeSequence,
                closing_token_types: TokenTypeSequence,
                parsing_fn: typing.Callable[[], typing.Any] | None = None, *, 
                normal_wrapper: type[NormalWrapper],
                comprehension_wrapper: type[ComprehensionWrapper],
                allow_comprehension: bool = True,
                not_closing_error: errors.BaseSapphireError = errors.InternalError("Placeholder error"),
                elements: list = [],
                **context) -> NormalWrapper | ComprehensionWrapper:
        
        supported_loop_tokens = [TokenType.Statements.Loops.ForLoopFromPython]
        def condition_to_break_loop():
            if isinstance(closing_token_types, TokenType):
                return (closing_token_types, *supported_loop_tokens)
            if isinstance(closing_token_types, list):
                return closing_token_types + supported_loop_tokens
            if isinstance(closing_token_types, tuple):
                return closing_token_types + tuple(supported_loop_tokens)
            if isinstance(closing_token_types, set):
                return closing_token_types | set(supported_loop_tokens)
            else:
                raise errors.InternalError(f"{type(closing_token_types)} not supported")

        if parsing_fn is None:
            parsing_fn = lambda: self._parse_expr(**context)
        
        self._advance(opening_token_types)
        if len(elements) != 0:
            elements.append(parsing_fn())
        while self._peek() == TokenType.Symbols.SequenceElementSeparator:
            self._advance()
            if self._peek().type in condition_to_break_loop():
                break
            elements.append(parsing_fn())
        if allow_comprehension and self._peek().type == TokenType.Statements.Loops.ForLoopFromPython:
            return self._parse_comprehension(
                elements, 
                closing_token_types,
                comprehension_wrapper,
                **context
            )
        self._advance(closing_token_types, not_closing_error)
        return normal_wrapper(elements)

    def _parse_comprehension[
                T: Nodes.SequenceComprehensionNode 
                | Nodes.DictComprehensionNode
            ](
            self,
            subjects: list,
            closing_bracket: TokenTypeSequence, 
            Wrapper: type[T],
            **context
            ) -> T:
        closing_bracket = self._to_token_sequence(closing_bracket)

        generators = []
        while self._peek().type in closing_bracket:
            conditions = []
            fallbacks = []
            # TODO Support other loop types
            loop_type = self._advance([
                TokenType.Statements.Loops.ForLoopFromPython
            ])
            var_list = self._parse_assignment_pattern(TokenType.Statements.Loops.IterableVarsAndIterableSeparatorInForLoopFromPython)
            self._advance(TokenType.Statements.Loops.IterableVarsAndIterableSeparatorInForLoopFromPython)
            iterable = self._parse_expr(**context)
            if self._peek().type == TokenType.Symbols.ConditionInComprehension:
                while self._peek().type == TokenType.Symbols.ConditionInComprehension:
                    self._advance(TokenType.Symbols.ConditionInComprehension)
                    conditions.append(self._parse_expr(**context))
                    if self._peek().type == TokenType.Symbols.FallbackInComprehension:
                        self._advance(TokenType.Symbols.FallbackInComprehension)
                        fallbacks.append(self._parse_expr())
                    else:
                        fallbacks.append(None)
            generators.append(
                Nodes.ForLoopInComprehension(
                    var_list,
                    iterable,
                    conditions,
                    fallbacks
                )
            )
        return Wrapper(subjects, generators)