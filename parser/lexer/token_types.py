# Auto-generated token_types.py for IntelliSense
# Beep bop
from parser.lexer.internal_token_types import InternalTokenType
import enum

class TokenTypeEnum(enum.Enum):
    pass

class TokenType(TokenTypeEnum):
    EoF = InternalTokenType.EoF
    Identifier = InternalTokenType.Identifier
    NewLine = InternalTokenType.NewLine
    Arrow = InternalTokenType.Arrow
    GDCologne = InternalTokenType.Symbols.Colon

    class Parentheses(TokenTypeEnum):
        OpenParenthesis = InternalTokenType.Parentheses.OpenParenthesis
        OpenParen = InternalTokenType.Parentheses.OpenParenthesis
        CloseParenthesis = InternalTokenType.Parentheses.CloseParenthesis
        CloseParen = InternalTokenType.Parentheses.CloseParenthesis
        OpenSquareBracket = InternalTokenType.Parentheses.OpenSquareBracket
        OpenBracket = InternalTokenType.Parentheses.OpenSquareBracket
        CloseSquareBracket = InternalTokenType.Parentheses.CloseSquareBracket
        CloseBracket = InternalTokenType.Parentheses.CloseSquareBracket
        OpenCurlyBrace = InternalTokenType.Parentheses.OpenCurlyBrace
        OpenBrace = InternalTokenType.Parentheses.OpenCurlyBrace
        CloseCurlyBrace = InternalTokenType.Parentheses.CloseCurlyBrace
        CloseBrace = InternalTokenType.Parentheses.CloseCurlyBrace

    class Symbols(TokenTypeEnum):

        class AugmentedAssignOpers(TokenTypeEnum):

            class Lefty(TokenTypeEnum):
                Addition = InternalTokenType.Symbols.PlusAndEqual
                Subtraction = InternalTokenType.Symbols.DashAndEqual
                Multiplication = InternalTokenType.Symbols.AsteriskAndEqual
                TrueDivision = InternalTokenType.Symbols.ForwardSlashAndEqual
                FloorDivision = InternalTokenType.Symbols.DoubleForwardSlashAndEqual
                Modulus = InternalTokenType.Symbols.PercentAndEqual
                Exponentation = InternalTokenType.Symbols.DoubleAsteriskAndEqual
                Concanentation = InternalTokenType.Symbols.DoubleDotAndEqual
                MatrixMultiplication = InternalTokenType.Symbols.AtAndEqual
                HybridXor = InternalTokenType.Symbols.CaretAndEqual
                HybridOr = InternalTokenType.Symbols.VerticalBarAndEqual
                HybridAnd = InternalTokenType.Symbols.AndpersandAndEqual
                BinaryXor = InternalTokenType.Symbols.BAndCaretAndEqual
                BinaryOr = InternalTokenType.Symbols.BAndVerticalBarAndEqual
                BinaryAnd = InternalTokenType.Symbols.BAndAndpersandAndEqual

            class Righty(TokenTypeEnum):
                Addition = InternalTokenType.Symbols.EqualAndPlus
                Subtraction = InternalTokenType.Symbols.EqualAndDash
                Multiplication = InternalTokenType.Symbols.EqualAndAsterisk
                TrueDivision = InternalTokenType.Symbols.EqualAndForwardSlash
                FloorDivision = InternalTokenType.Symbols.EqualAndDoubleForwardSlash
                Modulus = InternalTokenType.Symbols.EqualAndPercent
                Exponentation = InternalTokenType.Symbols.EqualAndDoubleAsterisk
                Concanentation = InternalTokenType.Symbols.EqualAndDoubleDot
                MatrixMultiplication = InternalTokenType.Symbols.EqualAndAt
                HybridXor = InternalTokenType.Symbols.EqualAndCaret
                HybridOr = InternalTokenType.Symbols.EqualAndVerticalBar
                HybridAnd = InternalTokenType.Symbols.EqualAndAndpersand
                BinaryXor = InternalTokenType.Symbols.EqualAndBAndCaret
                BinaryOr = InternalTokenType.Symbols.EqualAndBAndVerticalBar
                BinaryAnd = InternalTokenType.Symbols.EqualAndBAndAndpersand
        PositionalArgumentSeparator = InternalTokenType.Symbols.ForwardSlash
        KeywordArgumentSeparator = InternalTokenType.Symbols.Asterisk
        AssignOper = InternalTokenType.Symbols.Equal
        AttributeAccess = InternalTokenType.Symbols.Dot
        ClassAttributeAccess = InternalTokenType.Symbols.DoubleColon
        KeyValueSeparatorInDict = InternalTokenType.Symbols.Colon
        StatementSeparator = InternalTokenType.Symbols.Semicolon
        ThrowawayVariable = InternalTokenType.Symbols.Underscore
        KeywordFunctionArgumentAssignment = InternalTokenType.Symbols.Equal
        FunctionArgumentSeparator = InternalTokenType.Symbols.Comma
        SequenceElementSeparator = InternalTokenType.Symbols.Comma
        ForLoopFromCArgumentSeparator = InternalTokenType.Symbols.Semicolon
        AssignmentPatternSeparator = InternalTokenType.Symbols.Comma
        WalrusOper = InternalTokenType.Symbols.ColonAndEqual
        SliceSeparator = InternalTokenType.Symbols.Colon
        ConditionInComprehension = InternalTokenType.Keywords.If
        FallbackInComprehension = InternalTokenType.Keywords.Else

    class Statements(TokenTypeEnum):

        class ExceptionHandling(TokenTypeEnum):
            ExceptionTest = InternalTokenType.Keywords.Try
            HandleException = InternalTokenType.Keywords.Catch
            NoExceptions = InternalTokenType.Keywords.Else
            FinalCleanup = InternalTokenType.Keywords.Finally
            ThrowError = InternalTokenType.Keywords.Throw
            SourceOfThrowingError = InternalTokenType.Keywords.From

        class Declarations(TokenTypeEnum):
            MutableVariable = InternalTokenType.Keywords.Let
            ConstantVariable = InternalTokenType.Keywords.Const
            Function = InternalTokenType.Keywords.Fn
            Class = InternalTokenType.Keywords.Class
            Enum = InternalTokenType.Keywords.Enum
            Struct = InternalTokenType.Keywords.Struct

        class Loops(TokenTypeEnum):
            RunWhileCondition = InternalTokenType.Keywords.While
            ForLoopFromPython = InternalTokenType.Keywords.For
            IterableVarsAndIterableSeparatorInForLoopFromPython = InternalTokenType.Keywords.In
            ForLoopFromC = InternalTokenType.Keywords.Cfor
            StartOfDoWhileLoop = InternalTokenType.Keywords.Do
            ConditionOfDoWhileLoop = InternalTokenType.Keywords.While
            UninterruptedLoopExecution = InternalTokenType.Keywords.Else
            PrematureExit = InternalTokenType.Keywords.Break
            SkipToNextIteration = InternalTokenType.Keywords.Continue

        class Conditional(TokenTypeEnum):
            Condition = InternalTokenType.Keywords.If
            FallbackWithCondition = InternalTokenType.Keywords.Elif
            Fallback = InternalTokenType.Keywords.Else

        class MatchCase(TokenTypeEnum):
            Match = InternalTokenType.Keywords.Match
            Case = InternalTokenType.Keywords.Case
            DefaultCase = InternalTokenType.Symbols.Underscore
            VariableBindingIntoPattern = InternalTokenType.Keywords.As
            VariableBinding = InternalTokenType.Keywords.Let
            ConditionGuard = InternalTokenType.Keywords.If
            PatternSeparator = InternalTokenType.Symbols.Comma

        class SwitchCase(TokenTypeEnum):
            Switch = InternalTokenType.Keywords.Match
            Case = InternalTokenType.Keywords.Case
            DefaultCase = InternalTokenType.Symbols.Underscore
            VariableBindingIntoPattern = InternalTokenType.Keywords.As
            VariableBinding = InternalTokenType.Keywords.Let
            ConditionGuard = InternalTokenType.Keywords.If
            PatternSeparator = InternalTokenType.Symbols.Comma
        NewScope = InternalTokenType.Keywords.Scope
        DirectImport = InternalTokenType.Keywords.Import
        ImportFrom = InternalTokenType.Keywords.From
        Return = InternalTokenType.Keywords.Return
        Delete = InternalTokenType.Keywords.Del

    class Operators(TokenTypeEnum):

        class Binary(TokenTypeEnum):
            Addition = InternalTokenType.Symbols.Plus
            Subtraction = InternalTokenType.Symbols.Dash
            Multiplication = InternalTokenType.Symbols.Asterisk
            TrueDivision = InternalTokenType.Symbols.ForwardSlash
            FloorDivision = InternalTokenType.Symbols.DoubleForwardSlash
            Modulus = InternalTokenType.Symbols.Percent
            LogicalOr = InternalTokenType.Keywords.Or
            LogicalAnd = InternalTokenType.Keywords.And
            LogicalXor = InternalTokenType.Keywords.Xor
            HybridOr = InternalTokenType.Symbols.VerticalBar
            HybridAnd = InternalTokenType.Symbols.Andpersand
            HybridXor = InternalTokenType.Symbols.Caret
            BinaryOr = InternalTokenType.Symbols.VerticalBar
            BinaryAnd = InternalTokenType.Symbols.Andpersand
            BinaryXor = InternalTokenType.Symbols.Caret
            Containing = InternalTokenType.Keywords.In
            NotContaining = InternalTokenType.Keywords.NotIn
            Identity = InternalTokenType.Keywords.Is
            NotIdentity = InternalTokenType.Keywords.IsNot
            Concanentation = InternalTokenType.Symbols.DoubleDot
            MatrixMultiplication = InternalTokenType.Symbols.At
            Exponentiation = InternalTokenType.Symbols.DoubleAsterisk
            Equality = InternalTokenType.Symbols.DoubleEqual
            LooseEquality = InternalTokenType.Symbols.TildaAndEqual
            Inequality = InternalTokenType.Symbols.ExclamationAndEqual
            LooseInequality = InternalTokenType.Symbols.ExclamationAndTildaAndEqual
            LessThan = InternalTokenType.Symbols.LessThan
            GreaterThan = InternalTokenType.Symbols.GreaterThan
            LessThanOrEqualTo = InternalTokenType.Symbols.LessThanAndEqual
            GreaterThanOrEqualTo = InternalTokenType.Symbols.GreaterThanAndEqual
            LeftShift = InternalTokenType.Symbols.DoubleLessThan
            RightShift = InternalTokenType.Symbols.DoubleGreaterThan
            Spaceship = InternalTokenType.Symbols.SpaceCapsule

        class Ternary(TokenTypeEnum):
            ConditionSeparator = InternalTokenType.Symbols.QuestionMark
            ResultSeparator = InternalTokenType.Symbols.Colon

        class Unary(TokenTypeEnum):
            Positive = InternalTokenType.Symbols.Plus
            Negative = InternalTokenType.Symbols.Dash
            PositionalUnpack = InternalTokenType.Symbols.Asterisk
            KeywordUnpack = InternalTokenType.Symbols.DoubleAsterisk
            Increment = InternalTokenType.Symbols.DoublePlus
            Decrement = InternalTokenType.Symbols.DoubleDash
            BinaryInversion = InternalTokenType.Symbols.Tilda
            HybridNot = InternalTokenType.Symbols.Exclamation
            LogicalNot = InternalTokenType.Keywords.Not
            PositionalVariadic = InternalTokenType.Symbols.Asterisk
            KeywordVariadic = InternalTokenType.Symbols.DoubleAsterisk

    class Primitives(TokenTypeEnum):
        Int = InternalTokenType.Primitives.Int
        Float = InternalTokenType.Primitives.Float
        String = InternalTokenType.Primitives.String
        Boolean = InternalTokenType.Primitives.Boolean
        Null = InternalTokenType.Primitives.Null
        Ellipsis = InternalTokenType.Symbols.TripleDot

Parentheses = TokenType.Parentheses
Symbols = TokenType.Symbols
AugmentedAssignOpers = Symbols.AugmentedAssignOpers
LeftyAugmentedAssignOpers = AugmentedAssignOpers.Lefty
RightyAugmentedAssignOpers = AugmentedAssignOpers.Righty
Statements = TokenType.Statements
ExceptionHandling = Statements.ExceptionHandling
Declarations = Statements.Declarations
Loops = Statements.Loops
Conditional = Statements.Conditional
MatchCase = Statements.MatchCase
SwitchCase = Statements.SwitchCase
Operators = TokenType.Operators
BinaryOperators = Operators.Binary
TernaryOperators = Operators.Ternary
UnaryOperators = Operators.Unary
Primitives = TokenType.Primitives

__all__ = [
    "TokenType",
    "TokenTypeEnum",
    "Symbols",
    "Statements",
    "UnaryOperators",
    "AugmentedAssignOpers",
    "Loops",
    "Parentheses",
    "MatchCase",
    "Conditional",
    "Primitives",
    "BinaryOperators",
    "Operators",
    "LeftyAugmentedAssignOpers",
    "TernaryOperators",
    "ExceptionHandling",
    "SwitchCase",
    "Declarations",
    "RightyAugmentedAssignOpers",
]