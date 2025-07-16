import typing
from backend import errors
from parser.lexer import Token, TokenType, Tokenizer
import parser.nodes as Nodes

class Collections:
    tokens: Tokenizer
    def advance(
        self, 
        ts: typing.Sequence[TokenType] = [], 
        error: errors.SapphireError | None = None
    ) -> Token: ...
    def parse_expr(self, **context) -> Nodes.ExprNode: ...
    def parse_stmt(self, **context) -> Nodes.StmtNode: ...
    def peek(self, offset: int = 0) -> Token: ...
    parse_assignment_expr: typing.Callable[..., Nodes.WalrusNode | Nodes.ExprNode]
    def parse_collections_expr(
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
        match self.peek():
            case _ if allow_explicit_tuple and self.peek().type == TokenType.Comma:
                # $ This is a tuple WITH parentheses
                # $ In this case, this function is call from:
                # > parse_primary_expr(), on the branch that parse parenthesis
                # $ The ( is already consumed, so we don't have to remove it now

                # ? Now removing 'in_parentheses'
                # $ The only place that gives 'allow_explicit_tuple' should also gives 'in_parentheses' anyway
                context.pop("in_parentheses")
                elements = [self.parse_expr()]
                while self.peek().type == TokenType.Comma:
                    self.advance()
                    if self.peek().type == TokenType.CloseParenthesis:
                        break
                    elements.append(self.parse_expr(**context))
                # @ DO NOT EAT THE ')' TOKEN
                # $ As of now, the self.parse_primary_expr() function that call this one is still waiting for the expression
                # $ And then it will eat the ')' token
                # ! Eat it now will break everything
                return Nodes.TupleNode(elements)
            case _ if allow_implicit_tuple and self.peek() == TokenType.Comma:
                elements = [self.parse_expr()]
                while self.peek() == TokenType.Comma:
                    self.advance()
                    elements.append(self.parse_expr(**context))
                return Nodes.TupleNode(elements)
            case TokenType.OpenSquareBracket:
                return self.parse_list()
            case TokenType.OpenCurlyBrace:
                key_expr = self.parse_expr(**context)
                if self.peek() == TokenType.GDCologne:
                    # $ A dictionary...is it a comprehension, though?
                    self.advance()
                    val_expr = self.parse_expr(**context)
                    if self.peek() == TokenType.For:
                        # $ This is a dictionary comprehension
                        return self.parse_dict_comprehension(subject = (key_expr, val_expr), **context)
                    # $ This is a normal dictionary
                    return self.parse_dict((key_expr, val_expr), **context)
                else:
                    return self.parse_set(key_expr, **context)
            case _:
                return self.parse_assignment_expr(**context)

    def parse_list(self, **context):
        expr = self.parse_expr(**context)
        if self.peek() == TokenType.For:
            # $ This is a list comprehension
            return self.parse_comprehension(subject = expr, closing_bracket = TokenType.CloseSquareBracket, **context)
        # $ This is a list
        elements = [expr]
        while self.peek() == TokenType.Comma:
            self.advance()
            if self.peek() == TokenType.CloseSquareBracket:
                break
            elements.append(self.parse_expr(**context))
        self.advance([TokenType.CloseSquareBracket], error = errors.SyntaxError("'[' is not closed"))
        return Nodes.ListNode(elements)

    def parse_set(self, key_expr: Nodes.ExprNode, **context):
        if self.peek() == TokenType.For:
            # $ This is a set comprehension
            return self.parse_comprehension(closing_bracket = TokenType.CloseCurlyBrace, **context)
        else:
            # $ This is a set
            items = [key_expr]
            while self.peek() == TokenType.Comma:
                self.advance()
                if self.peek() == TokenType.CloseCurlyBrace:
                    break
                items.append(self.parse_expr(**context))
            self.advance([TokenType.CloseCurlyBrace], error = errors.SyntaxError("'{' is not closed"))
            return Nodes.SetNode(items)

    def parse_dict(self, first_pair: tuple[Nodes.ExprNode, Nodes.ExprNode], **context):
        pairs = [first_pair]
        while self.peek() == TokenType.Comma:
            self.advance()
            if self.peek() == TokenType.CloseCurlyBrace:
                break
            k = self.parse_expr(**context)
            self.advance([TokenType.GDCologne])
            v = self.parse_expr(**context)
            pairs.append((k, v))
        self.advance([TokenType.CloseCurlyBrace], error = errors.SyntaxError("'{' is not closed"))
        return Nodes.DictNode(pairs)

    def parse_comprehension(self, subject: Nodes.ExprNode, closing_bracket: TokenType | None, **context) -> Nodes.ListComprehensionNode | Nodes.GeneratorComprehensionNode | Nodes.SetComprehensionNode:
        self.advance([TokenType.For])
        syntax_expr = self.parse_expr(allow_implicit_tuples = True, **context)
        iter_vars = []
        iterable = None
        condition = None
        otherwise = None

        if isinstance(syntax_expr, Nodes.BinaryNode) and syntax_expr.oper == TokenType.In:
            if isinstance(syntax_expr.left, Nodes.IdentifierNode):
                iter_vars = [syntax_expr.left.symbol]
                iterable = syntax_expr.right
            elif isinstance(syntax_expr.left, Nodes.TupleNode):
                if all(isinstance(i, Nodes.IdentifierNode) for i in syntax_expr.left.value):
                    values = typing.cast(list[Nodes.IdentifierNode], syntax_expr.left.value)
                    iter_vars = [i.symbol for i in values]
                    iterable = syntax_expr.right
                else:
                    raise errors.SyntaxError("Expected only identifiers on the left-hand side of 'in'")
            else:
                raise errors.SyntaxError("Invalid iterable unpacking target before 'in'")

        elif isinstance(syntax_expr, Nodes.TupleNode):
            if not syntax_expr.value:
                raise errors.SyntaxError("Empty tuple is not valid in a for loop")
            
            *left, last = syntax_expr.value
            if (
                isinstance(last, Nodes.BinaryNode) and last.oper == TokenType.In and
                isinstance(last.left, Nodes.IdentifierNode) and
                all(isinstance(i, Nodes.IdentifierNode) for i in left)
            ):
                left = typing.cast(list[Nodes.IdentifierNode], left)
                iter_vars = [i.symbol for i in left] + [last.left.symbol]
                iterable = last.right
            else:
                raise errors.SyntaxError("Could not resolve iterable expression from tuple pattern")

        else:
            raise errors.SyntaxError("Invalid syntax in 'for' loop head")
        
        if self.peek().type == TokenType.If:
            self.advance()
            condition = self.parse_expr()
        
        if self.peek().type == TokenType.Else:
            self.advance()
            if self.peek().type in {TokenType.Break, TokenType.Continue, TokenType.Throw}:
                otherwise = self.parse_stmt(**context)
            else:
                otherwise = self.parse_expr(**context)

        if closing_bracket is not None:
            self.advance([closing_bracket])

        match closing_bracket:
            case TokenType.CloseSquareBracket:
                return Nodes.ListComprehensionNode(subject, iter_vars, iterable, condition, otherwise)
            case TokenType.CloseCurlyBrace:
                return Nodes.SetComprehensionNode(subject, iter_vars, iterable, condition, otherwise)
            case TokenType.CloseParenthesis | None:
                return Nodes.GeneratorComprehensionNode(subject, iter_vars, iterable, condition, otherwise)
            case _:
                raise errors.InternalError(f"Invalid value enter into 'closing_bracket' for Collections.parse_comprehension() ('{closing_bracket}')")

    def parse_dict_comprehension(self, pair: tuple[Nodes.ExprNode, Nodes.ExprNode], **context) -> Nodes.DictComprehensionNode:
        self.advance([TokenType.For])
        syntax_expr = self.parse_expr(allow_implicit_tuples = True, **context)
        iter_vars = []
        iterable = None
        condition = None
        otherwise = None

        if isinstance(syntax_expr, Nodes.BinaryNode) and syntax_expr.oper == TokenType.In:
            if isinstance(syntax_expr.left, Nodes.IdentifierNode):
                iter_vars = [syntax_expr.left.symbol]
                iterable = syntax_expr.right
            elif isinstance(syntax_expr.left, Nodes.TupleNode):
                if all(isinstance(i, Nodes.IdentifierNode) for i in syntax_expr.left.value):
                    values = typing.cast(list[Nodes.IdentifierNode], syntax_expr.left.value)
                    iter_vars = [i.symbol for i in values]
                    iterable = syntax_expr.right
                else:
                    raise errors.SyntaxError("Expected only identifiers on the left-hand side of 'in'")
            else:
                raise errors.SyntaxError("Invalid iterable unpacking target before 'in'")

        elif isinstance(syntax_expr, Nodes.TupleNode):
            if not syntax_expr.value:
                raise errors.SyntaxError("Empty tuple is not valid in a for loop")
            
            *left, last = syntax_expr.value
            if (
                isinstance(last, Nodes.BinaryNode) and last.oper == TokenType.In and
                isinstance(last.left, Nodes.IdentifierNode) and
                all(isinstance(i, Nodes.IdentifierNode) for i in left)
            ):
                left = typing.cast(list[Nodes.IdentifierNode], left)
                iter_vars = [i.symbol for i in left] + [last.left.symbol]
                iterable = last.right
            else:
                raise errors.SyntaxError("Could not resolve iterable expression from tuple pattern")

        else:
            raise errors.SyntaxError("Invalid syntax in 'for' loop head")
        
        if self.peek().type == TokenType.If:
            self.advance()
            condition = self.parse_expr()
        
        if self.peek().type == TokenType.Else:
            self.advance()
            if self.peek().type in {TokenType.Break, TokenType.Continue, TokenType.Throw}:
                otherwise = self.parse_stmt(**context)
            else:
                otherwise = self.parse_expr(**context)

        self.advance([TokenType.CloseCurlyBrace])
        
        return Nodes.DictComprehensionNode(pair, iter_vars, iterable, condition, otherwise)