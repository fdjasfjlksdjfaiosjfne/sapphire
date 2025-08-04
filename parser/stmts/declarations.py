import typing

from backend import errors
from parser.lexer import TokenType, Declarations, Parentheses, TokenTypeSequence
import parser.nodes as Nodes
from parser.core import ParserNamespaceSkeleton

class DeclarationStatements(ParserNamespaceSkeleton):
    def _parse_fn_declaration(self) -> Nodes.FunctionDeclarationNode:
        self._advance(Declarations.Function)
        name = self._advance(TokenType.Identifier).value
        self._advance(Parentheses.OpenParenthesis)
        args = [self._parse_fn_declaration_args()]
        while self._peek().type == TokenType.Symbols.FunctionArgumentSeparator:
            self._advance(TokenType.Symbols.FunctionArgumentSeparator)
            if self._peek().type == Parentheses.CloseParenthesis:
                break
            args.append(self._parse_fn_declaration_args())
        self._advance(Parentheses.CloseParenthesis)
        code_block = self._parse_attached_code_block()
        return Nodes.FunctionDeclarationNode(
            name, args, code_block
        )

    def _parse_fn_declaration_args(self) -> Nodes.DeclaredArgumentNode:
        # TODO This needs a makeover to fully support customization
        match self._peek().type:
            case TokenType.Identifier:
                return Nodes.DeclaredArgumentNode(
                    Nodes.DeclaredArgumentType.Normal,
                    self._advance().value
                )
            case TokenType.Symbols.PositionalArgumentSeparator:
                return Nodes.DeclaredArgumentNode(
                    Nodes.DeclaredArgumentType.PositionalSeparator
                )
            case TokenType.Symbols.KeywordArgumentSeparator:
                self._advance(TokenType.Symbols.KeywordArgumentSeparator)
                if self._peek().type == TokenType.Identifier:
                    return Nodes.DeclaredArgumentNode(
                        Nodes.DeclaredArgumentType.PositionalVariadic,
                        self._advance().value
                    )
                return Nodes.DeclaredArgumentNode(
                    Nodes.DeclaredArgumentType.KeywordSeparator
                )
            case TokenType.Operators.Unary.KeywordVariadic:
                self._advance( TokenType.Operators.Unary.KeywordVariadic)
                if self._peek().type == TokenType.Identifier:
                    return Nodes.DeclaredArgumentNode(
                        Nodes.DeclaredArgumentType.KeywordVariadic,
                        self._advance().value
                    )
                raise errors.SyntaxError(
                    "Expected identifier after '**'"
                )
            case _:
                raise errors.SyntaxError(
                    "Invalid syntax"
                )

    def _parse_var_declaration(self, **context) -> Nodes.VarDeclarationNode:
        constant = self._advance() == Declarations.ConstantVariable
        assign = self._parse_assignment_stmt(**context)
        if isinstance(assign, Nodes.AssignmentNode):
            return Nodes.VarDeclarationNode(assign.targets, assign.value, constant)
        raise errors.SyntaxError(
            "Augmented assignment node not allowed in variable declaration"
        )

    def _parse_assignment_stmt(self, **context) -> (
            Nodes.AssignmentNode | Nodes.ModifierAssignmentNode | Nodes.ExprNode
            ):
        start_pos = self.tokens.save()
        list_of_assignment_tokens = [
            TokenType.Symbols.AssignOper, 
            *TokenType.Symbols.AugmentedAssignOpers.Lefty.__members__,
            *TokenType.Symbols.AugmentedAssignOpers.Righty.__members__
        ]
        try:
            # Try parsing LHS with backtracking support
            target_start_pos = self.tokens.save()
            try:
                target = self._parse_assignment_pattern(
                    ending_tokens = list_of_assignment_tokens
                )
            except errors.SapphireError:
                self.tokens.load(target_start_pos)
                raise errors._Backtrack

            # Check assignment type
            next_tok = self._peek()
            if next_tok.type == TokenType.Symbols.AssignOper:
                self._advance()  # Consume '='
                
                # Handle chained assignments
                targets = [target]
                while True:
                    chain_pos = self.tokens.save()
                    try:
                        next_target = self._parse_assignment_pattern(
                            ending_tokens = list_of_assignment_tokens
                        )
                        if self._peek().type != TokenType.Symbols.AssignOper:
                            self.tokens.load(chain_pos)
                            break
                        self._advance()  # Consume '='
                        targets.append(next_target)
                    except errors.SapphireError:
                        self.tokens.load(chain_pos)
                        break
                
                value = self._parse_expr(**context)
                return Nodes.AssignmentNode(targets, value)
            
            elif next_tok.type in [*TokenType.Symbols.AugmentedAssignOpers.Lefty.__members__,
                                   *TokenType.Symbols.AugmentedAssignOpers.Righty.__members__]:
                op = self._advance()
                value = self._parse_expr(**context)
                return Nodes.ModifierAssignmentNode(target[0], op, value)
            
            raise errors._Backtrack
        
        except errors._Backtrack:
            self.tokens.load(start_pos)
            return self._parse_expr(**context)
    
    def _parse_assignment_pattern(self, ending_tokens: TokenTypeSequence, **context) -> list[Nodes.ExprNode]:
        save_point = self.tokens.save()
        try:
            if isinstance(ending_tokens, TokenType):
                ending_tokens = (ending_tokens,)
            elements = []
            self._parse_assignment_pattern_element(elements, **context)
            while self._peek().type == TokenType.Symbols.AssignmentPatternSeparator:
                self._advance(TokenType.Symbols.AssignmentPatternSeparator)
                if self._peek().type in ending_tokens:
                    break
                self._parse_assignment_pattern_element(elements, **context)
            return elements
        except errors.SapphireError as e:
            self.tokens.load(save_point)
            raise errors._Backtrack from e
    
    def _parse_assignment_pattern_element(self, elements: list, **context):
        match self._peek().type:
            case TokenType.Identifier:
                elements.append(self._advance([TokenType.Identifier]))
            case TokenType.Operators.Unary.PositionalUnpack:
                a = self._advance()
                if self._peek().type == TokenType.Identifier:
                    elements.append(
                            Nodes.UnaryNode(
                                expr = Nodes.IdentifierNode(self._advance(TokenType.Identifier).value),
                                attachment = a,
                                position = "Prefix"
                            )
                    )
            case Parentheses.OpenParenthesis:
                self._advance(Parentheses.OpenParenthesis)
                elmts = self._parse_assignment_pattern(Parentheses.CloseParenthesis)
                return Nodes.TupleNode(elmts)