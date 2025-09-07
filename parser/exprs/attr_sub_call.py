import typing
from backend import errors
from parser.core import ParserNamespaceSkeleton
from lexer import TokenType, Parentheses
import parser.nodes as Nodes

class AttributeSubcriptionCall(ParserNamespaceSkeleton):
    def _parse_member_subscription_call_expr(self, **context) -> (
            Nodes.CallNode | 
            Nodes.AttributeNode | 
            Nodes.SubscriptionNode | 
            Nodes.ExprNode
        ):
        """Parses member access (a.b), subscription access (a[b]) and function call (a(b)) expressions."""
        member = self._parse_member_subscription_expr(**context)
        if self._peek() == TokenType.Parentheses.OpenParenthesis:
            return self._parse_call_expr(member, **context)
        return member

    def _parse_member_subscription_expr(self, **context) -> Nodes.AttributeNode | Nodes.SubscriptionNode | Nodes.ExprNode: 
        obj = self._parse_primary_expr(**context)
        while self._peek() in (TokenType.Symbols.AttributeAccess,
                               TokenType.Symbols.ClassAttributeAccess,
                               TokenType.Parentheses.OpenSquareBracket):
            if self._advance() == TokenType.Symbols.AttributeAccess:
                attr = typing.cast(Nodes.ExprNode | None, None)
                if self._peek() == TokenType.Identifier:
                    attr = self._advance([TokenType.Identifier]).value
                    return Nodes.AttributeNode(obj, attr)
                raise errors.SyntaxError(
                    "Expecting a identifier after the '.' in an attribute expression"
                )
            elif self._advance() == TokenType.Symbols.ClassAttributeAccess:
                attr = typing.cast(Nodes.ExprNode | None, None)
                if self._peek() == TokenType.Identifier:
                    attr = self._advance([TokenType.Identifier]).value
                    return Nodes.ClassAttributeNode(obj, attr)
                raise errors.SyntaxError(
                    "Expecting a identifier after the '::' in an class attribute expression"
                )
            else:
                slice: (
                    list[Nodes.ExprNode | None]
                ) = [self._parse_expr(**context)]

                # $ Slicing
                if self._peek().type == TokenType.Symbols.SliceSeparator:
                    self._advance([TokenType.Symbols.SliceSeparator])
                    slice.append(self._parse_expr(**context))
                    if self._peek().type == TokenType.Symbols.SliceSeparator:
                        self._advance([TokenType.Symbols.SliceSeparator])
                        slice.append(self._parse_expr(**context))
                    else:
                        slice.append(None)
                else:
                    slice.append(None)

                
                self._advance([Parentheses.CloseSquareBracket])
                return Nodes.SubscriptionNode(
                    obj, 
                    typing.cast(
                        tuple[
                            Nodes.ExprNode, 
                            Nodes.ExprNode | None, 
                            Nodes.ExprNode | None
                        ], 
                        tuple(slice)
                    )
                )
        return obj

    def _parse_call_expr(self, caller: Nodes.ExprNode, **context) -> Nodes.CallNode:
        call_expr = Nodes.CallNode(
            caller, 
            Nodes.CallArgumentList(*self._parse_call_args(**context))
        )
        if self._peek() == TokenType.Parentheses.OpenParenthesis:
            call_expr = self._parse_call_expr(caller = call_expr, **context)
        return call_expr
    
    def _parse_call_args(self, **context) -> tuple[list[Nodes.ExprNode], dict[str, Nodes.ExprNode]]:
        self._advance([TokenType.Parentheses.OpenParenthesis], error = errors.InternalError(
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
            if self._peek().type == TokenType.Parentheses.CloseParenthesis:
                break
            arg = self._parse_expr()

            # $ Check for any keyword arguments
            if isinstance(arg, Nodes.IdentifierNode) and self._peek().type == TokenType.Symbols.KeywordFunctionArgumentAssignment:
                self._advance([TokenType.Symbols.KeywordFunctionArgumentAssignment], errors.InternalError(
                    "A redundant check for eating a '=' has been tripped."
                ))
                kwargs[arg.symbol] = self._parse_expr()
                while self._peek().type == TokenType.Symbols.FunctionArgumentSeparator:
                    self._advance([TokenType.Symbols.FunctionArgumentSeparator], error = errors.InternalError(
                        "A redundant check eating a comma has been tripped."
                    ))
                    if self._peek().type == TokenType.Parentheses.CloseParenthesis:
                        break
                    key = self._advance([TokenType.Identifier], error = errors.SyntaxError(
                        "Expecting an identifier as the key for a keyword argument in a call expression"
                    )).value
                    self._advance([TokenType.Symbols.FunctionArgumentSeparator], error = errors.SyntaxError(
                        "Expecting '=' after the key for a keyword argument in a call expression"
                    ))
                    kwargs[key] = self._parse_expr()
            else:
                args.append(arg)
            
            if kwargs:
                break

        self._advance([Parentheses.CloseParenthesis], error = errors.SyntaxError(
            "')' for a call expression is not closed"
        ))
        return args, kwargs