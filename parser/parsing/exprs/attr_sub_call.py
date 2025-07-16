import typing
from backend import errors
from parser.lexer import Token, TokenType, Tokenizer
import parser.nodes as Nodes

class AttributeSubcriptionCall:
    tokens: Tokenizer
    def advance(
        self, 
        ts: typing.Sequence[TokenType] = [], 
        error: errors.SapphireError | None = None
    ) -> Token: ...
    def peek(self, offset: int = 0) -> Token: ...
    parse_expr: typing.Callable[..., Nodes.ExprNode]
    parse_primary_expr: typing.Callable[..., Nodes.ExprNode]

    def parse_member_subscription_call_expr(self, **context) -> (
            Nodes.CallNode | 
            Nodes.AttributeNode | 
            Nodes.SubscriptionNode | 
            Nodes.ExprNode
        ):
        # $ Parses member access (a.b), subscription access (a[b]) and function call (a(b)) expressions.
        member = self.parse_member_subscription_expr(**context)
        if self.peek() == TokenType.OpenParenthesis:
            return self.parse_call_expr(**context)
        return member

    def parse_member_subscription_expr(self, **context) -> Nodes.AttributeNode | Nodes.SubscriptionNode | Nodes.ExprNode: 
        obj = self.parse_primary_expr(**context)
        while self.peek() in {TokenType.Dot, TokenType.OpenSquareBracket}:
            if self.advance() == TokenType.Dot:
                if self.peek() == TokenType.Identifier:
                    slice = self.advance([TokenType.Identifier])
                    return Nodes.AttributeNode(obj, slice.value)
                raise errors.SyntaxError(
                    "Expecting a identifier after the '.' in an attribute expression"
                )
            else:
                slice = [self.parse_expr(**context)]

                # $ Slicing
                if self.peek().type == TokenType.GDCologne:
                    self.advance([TokenType.GDCologne])
                    slice.append(self.parse_expr(**context))
                    if self.peek().type == TokenType.GDCologne:
                        self.advance([TokenType.GDCologne])
                        slice.append(self.parse_expr(**context))
                
                self.advance([TokenType.CloseSquareBracket])
                return Nodes.SubscriptionNode(obj, tuple(slice))
        return obj

    def parse_call_expr(self, caller: Nodes.ExprNode, **context) -> Nodes.CallNode:
        call_expr = Nodes.CallNode(caller, self.parse_call_args(**context))
        if self.peek() == TokenType.OpenParenthesis:
            call_expr = self.parse_call_expr(caller = call_expr, **context)
        return call_expr
    
    def parse_call_args(self, **context) -> Nodes.CallArgumentList:
        self.advance([TokenType.OpenParenthesis], error = errors.InternalError(
            "MemberSubscriptionCall.parse_call_args() cannot find a '(' token, "
            "even though the only place that call it should've check for it beforehand."
            "This parsing function might be called via other ways."
        ))
        args = []
        kwargs = {}
        while self.peek().type == TokenType.Comma:
            # & Don't you dare delete this >:(
            self.advance([TokenType.Comma], error = errors.InternalError(
                "A redundant check for eating a comma has been tripped.\n"
                "If this is triggered without using a debugger, it could be either:\n"
                " 1. Solar bit flip\n"
                " 2. Trolling gremlins in your computer\n"
                " 3. We're all in a simulation\n"
                " 4. Python is smoking weed\n"
                " 5. (most likely) I mess up somewhere ;-;"
            ))
            if self.peek().type == TokenType.CloseParenthesis:
                break
            arg = self.parse_expr()

            # $ Check for any keyword arguments
            if isinstance(arg, Nodes.IdentifierNode) and self.peek().type == TokenType.AssignOper:
                self.advance([TokenType.AssignOper], errors.InternalError(
                    "A redundant check for eating a '=' has been tripped."
                ))
                kwargs[arg.symbol] = self.parse_expr()
                while self.peek().type == TokenType.Comma:
                    self.advance([TokenType.Comma], error = errors.InternalError(
                        "A redundant check eating a comma has been tripped."
                    ))
                    if self.peek().type == TokenType.CloseParenthesis:
                        break
                    key = self.advance([TokenType.Identifier], error = errors.SyntaxError(
                        "Expecting an identifier as the key for a keyword argument in a call expression"
                    )).value
                    self.advance([TokenType.AssignOper], error = errors.SyntaxError(
                        "Expecting '=' after the key for a keyword argument in a call expression"
                    ))
                    kwargs[key] = self.parse_expr()
            else:
                args.append(arg)
            
            if kwargs:
                break

        self.advance([TokenType.CloseParenthesis], error = errors.SyntaxError(
            "')' for a call expression is not closed"
        ))
        return Nodes.CallArgumentList(args, kwargs)