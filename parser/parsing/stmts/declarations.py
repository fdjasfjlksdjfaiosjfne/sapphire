import typing

from backend import errors
from parser.lexer.lexer import Token, TokenType, TokenTypeSequence
import parser.nodes as Nodes
from parser.core import ParserNamespaceSkeleton

class Declarations(ParserNamespaceSkeleton):
    def _parse_fn_declaration(self) -> Nodes.FunctionDeclarationNode:
        self._advance(TokenType.KW_FunctionDeclaration)
        name = self._advance(TokenType.Identifier)
        self._advance(TokenType.PR_OpenParenthesis)
        args = [self._parse_fn_declaration_args()]
        while self._peek().type == TokenType.SY_Comma:
            self._advance(TokenType.SY_Comma)
            if self._peek().type == TokenType.PR_CloseParenthesis:
                break
            args.append(self._parse_fn_declaration_args())
        self._advance(TokenType.PR_CloseParenthesis)
        code_block = self._parse_attached_code_block()
        return Nodes.FunctionDeclarationNode(
            name, args, code_block
        )

    def _parse_fn_declaration_args(self):
        match self._peek().type:
            case TokenType.Identifier:
                return self._advance()
            case TokenType.SY_TrueDivision:
                return self._advance().type
            case TokenType.SY_Asterisk:
                self._advance(TokenType.SY_Asterisk)
                if self._peek().type == TokenType.Identifier:
                    return Nodes.UnaryNode(
                        expr = self._advance(),
                        attachment = TokenType.SY_Asterisk,
                        position = "Prefix"
                    )
                return TokenType.SY_Asterisk
            case TokenType.SY_Exponentiation:
                self._advance(TokenType.SY_Exponentiation)
                if self._peek().type == TokenType.Identifier:
                    return Nodes.UnaryNode(
                        expr = self._advance(),
                        attachment = TokenType.SY_Exponentiation,
                        position = "Prefix"
                    )
                raise errors.SyntaxError(
                    "Expected identifier after '**'"
                )
            case _:
                raise errors.SyntaxError(
                    "Invalid syntax"
                )

    def _parse_var_declaration(self, **context) -> Nodes.VarDeclarationNode:
        constant = self._advance() == TokenType.KW_Const
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
        
        try:
            # Try parsing LHS with backtracking support
            target_start_pos = self.tokens.save()
            try:
                target = self._parse_assignment_pattern([
                    TokenType.SY_AssignOper, 
                    TokenType.SY_ModifierAssignOper
                ])
            except errors.SapphireError:
                self.tokens.load(target_start_pos)
                raise errors._Backtrack

            # Check assignment type
            next_tok = self._peek()
            if next_tok.type == TokenType.SY_AssignOper:
                self._advance()  # Consume '='
                
                # Handle chained assignments
                targets = [target]
                while True:
                    chain_pos = self.tokens.save()
                    try:
                        next_target = self._parse_assignment_pattern([
                            TokenType.SY_AssignOper,
                            TokenType.SY_ModifierAssignOper
                        ])
                        if self._peek().type != TokenType.SY_AssignOper:
                            self.tokens.load(chain_pos)
                            break
                        self._advance()  # Consume '='
                        targets.append(next_target)
                    except errors.SapphireError:
                        self.tokens.load(chain_pos)
                        break
                
                value = self._parse_expr(**context)
                return Nodes.AssignmentNode(targets, value)
            
            elif next_tok.type == TokenType.SY_ModifierAssignOper:
                op = self._advance().value
                value = self._parse_expr(**context)
                return Nodes.ModifierAssignmentNode(target, op, value)
            
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
            self._parse_element(elements, **context)
            while self._peek().type == TokenType.SY_Comma:
                self._advance(TokenType.SY_Comma)
                if self._peek().type in ending_tokens:
                    break
                self._parse_element(elements, **context)
            return elements
        except errors.SapphireError as e:
            self.tokens.load(save_point)
            raise errors._Backtrack from e
    
    def _parse_element(self, elements: list, **context):
        match self._peek().type:
            case TokenType.Identifier:
                elements.append(self._advance([TokenType.Identifier]))
            case TokenType.SY_Asterisk:
                self._advance()
                if self._peek().type == TokenType.Identifier:
                    elements.append(
                            Nodes.UnaryNode(
                                expr = self._advance(TokenType.Identifier),
                                attachment = TokenType.SY_Asterisk,
                                position = "Prefix"
                            )
                    )
            case TokenType.PR_OpenParenthesis:
                self._advance(TokenType.PR_OpenParenthesis)
                elmts = self._parse_assignment_pattern(TokenType.PR_CloseParenthesis)
                return Nodes.TupleNode(elmts)