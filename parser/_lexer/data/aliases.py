from backend.config import CONFIG
from parser._lexer.data.aliases_modifiers import base, inverted_comparisons
cust = CONFIG.customization
redefine = cust.redefine
templates = CONFIG.templates

ALIASES: dict = {
    "EoF": ("EoF",),
    "Identifier": ("Identifier",),
    "NewLine": ("NewLine",),
    "Arrow": ("Arrow",),
    "GDCologne": ("Symbols", "Colon"),
    "Parentheses": {
        "OpenParenthesis": ("Parentheses", "OpenParenthesis"),
        "OpenParen": ("Parentheses", "OpenParenthesis"),

        "CloseParenthesis": ("Parentheses", "CloseParenthesis"),
        "CloseParen": ("Parentheses", "CloseParenthesis"),

        "OpenSquareBracket": ("Parentheses", "OpenSquareBracket"),
        "OpenBracket": ("Parentheses", "OpenSquareBracket"),

        "CloseSquareBracket": ("Parentheses", "CloseSquareBracket"),
        "CloseBracket": ("Parentheses", "CloseSquareBracket"),

        "OpenCurlyBrace": ("Parentheses", "OpenCurlyBrace"),
        "OpenBrace": ("Parentheses", "OpenCurlyBrace"),

        "CloseCurlyBrace": ("Parentheses", "CloseCurlyBrace"),
        "CloseBrace": ("Parentheses", "CloseCurlyBrace"),
    },
    
    "Symbols": {
        "AugmentedAssignOpers": {
            "Lefty": {
                "Addition": ("Symbols", "PlusAndEqual"),
                "Subtraction": ("Symbols", "DashAndEqual"),
                "Multiplication": ("Symbols", "AsteriskAndEqual"),
                "TrueDivision": ("Symbols", "ForwardSlashAndEqual"),
                "FloorDivision": ("Symbols", "DoubleForwardSlashAndEqual"),
                "Modulus": ("Symbols", "PercentAndEqual"),
                "Exponentation": ("Symbols", "DoubleAsteriskAndEqual"),
                "Concanentation": ("Symbols", "DoubleDotAndEqual"),
                "MatrixMultiplication": ("Symbols", "AtAndEqual"),
                "HybridXor": ("Symbols", "CaretAndEqual"),
                "HybridOr": ("Symbols", "VerticalBarAndEqual"),
                "HybridAnd": ("Symbols", "AndpersandAndEqual"),
                "BinaryXor": ("Symbols", "BAndCaretAndEqual"),
                "BinaryOr": ("Symbols", "BAndVerticalBarAndEqual"),
                "BinaryAnd": ("Symbols", "BAndAndpersandAndEqual"),
            },
            "Righty": {
                "Addition": ("Symbols", "EqualAndPlus"),
                "Subtraction": ("Symbols", "EqualAndDash"),
                "Multiplication": ("Symbols", "EqualAndAsterisk"),
                "TrueDivision": ("Symbols", "EqualAndForwardSlash"),
                "FloorDivision": ("Symbols", "EqualAndDoubleForwardSlash"),
                "Modulus": ("Symbols", "EqualAndPercent"),
                "Exponentation": ("Symbols", "EqualAndDoubleAsterisk"),
                "Concanentation": ("Symbols", "EqualAndDoubleDot"),
                "MatrixMultiplication": ("Symbols", "EqualAndAt"),
                "HybridXor": ("Symbols", "EqualAndCaret"),
                "HybridOr": ("Symbols", "EqualAndVerticalBar"),
                "HybridAnd": ("Symbols", "EqualAndAndpersand"),
                "BinaryXor": ("Symbols", "EqualAndBAndCaret"),
                "BinaryOr": ("Symbols", "EqualAndBAndVerticalBar"),
                "BinaryAnd": ("Symbols", "EqualAndBAndAndpersand"),
            }
        },
        "PositionalArgumentSeparator": ("Symbols", "ForwardSlash"),
        "KeywordArgumentSeparator": ("Symbols", "Asterisk"),
        "AssignOper": ("Symbols", "Equal"),
        "AttributeAccess": ("Symbols", "Dot"),
        "ClassAttributeAccess": ("Symbols", "DoubleColon"),
        "KeyValueSeparatorInDict": ("Symbols", "Colon"),
        "StatementSeparator": ("Symbols", "Semicolon"),
        "ThrowawayVariable": ("Symbols", "Underscore"),
        "KeywordFunctionArgumentAssignment": ("Symbols", "Equal"),
        "FunctionArgumentSeparator": ("Symbols", "Comma"),
        "SequenceElementSeparator": ("Symbols", "Comma"),
        "ForLoopFromCArgumentSeparator": ("Symbols", "Semicolon"),
        "AssignmentPatternSeparator": ("Symbols", "Comma"),
        "WalrusOper": ("Symbols", "ColonAndEqual"),
        "SliceSeparator": ("Symbols", "Colon"),
        "ConditionInComprehension": ("Keywords", "If"),
        "FallbackInComprehension": ("Keywords", "Else")
    },
    "Statements": {
        "ExceptionHandling": {
            "ExceptionTest": ("Keywords", "Try"),
            "HandleException": ("Keywords", redefine.handle_exception_phrase.title()),
            "NoExceptions": ("Keywords", "Else"),
            "FinalCleanup": ("Keywords", redefine.final_cleanup_of_exception_handling.title()),
            "ThrowError": ("Keywords", redefine.throw_error.title()),
            "SourceOfThrowingError": ("Keywords", "From")
        },
        "Declarations": {
            "MutableVariable": ("Keywords", "Let"),
            "ConstantVariable": ("Keywords", "Const"),
            "Function": ("Keywords", redefine.function_def.title()),
            "Class": ("Keywords", redefine.class_def.title()),
            "Enum": ("Keywords", "Enum"),
            "Struct": ("Keywords", "Struct")
        },
        "Loops": {
            "RunWhileCondition": ("Keywords", "While"),
            "ForLoopFromPython": ("Keywords", "For"),
            "IterableVarsAndIterableSeparatorInForLoopFromPython": ("Keywords", "In"),
            "ForLoopFromC": ("Keywords", "Cfor"),
            "StartOfDoWhileLoop": ("Keywords", "Do"),
            "ConditionOfDoWhileLoop": ("Keywords", "While"),
            "UninterruptedLoopExecution": ("Keywords", "Else"),
            "PrematureExit": ("Keywords", "Break"),
            "SkipToNextIteration": ("Keywords", "Continue")
        },
        "Conditional": {
            "Condition": ("Keywords", "If"),
            "FallbackWithCondition": ("Keywords", redefine.else_if.title().replace(" ", "")),
            "Fallback": ("Keywords", "Else")
        },
        "MatchCase": {
            "Match": ("Keywords", redefine.match_case_statement.title()),
            "Case": ("Keywords", "Case"),
            "DefaultCase": base.default_case(),
            "VariableBindingIntoPattern": ("Keywords", "As"),
            "VariableBinding": ("Keywords", "Let"),
            "ConditionGuard": ("Keywords", "If"),
            "PatternSeparator": ("Symbols", "Comma")
        },
        "NewScope": ("Keywords", "Scope"),
        "DirectImport": ("Keywords", "Import"),
        "ImportFrom": ("Keywords", "From"),
        "Return": ("Keywords", "Return"),
        "Delete": ("Keywords", "Del")
    },
    "Operators": {
        "Binary": {
            "Addition": ("Symbols", "Plus"),
            "Subtraction": ("Symbols", "Dash"),
            "Multiplication": ("Symbols", "Asterisk"),
            "TrueDivision": ("Symbols", "ForwardSlash"),
            "FloorDivision": base.floordiv(),
            "Modulus": base.modulus(),
            "LogicalOr": ("Keywords", "Or"),
            "LogicalAnd": ("Keywords", "And"),
            "LogicalXor": ("Keywords", "Xor"),
            "HybridOr": ("Symbols", "VerticalBar"),
            "HybridAnd": ("Symbols", "Andpersand"),
            "HybridXor": ("Symbols", "Caret"),
            "BinaryOr": ("Symbols", "BAndVerticalBar"),
            "BinaryAnd": ("Symbols", "BAndAndpersand"),
            "BinaryXor": ("Symbols", "BAndCaret"),
            "Containing": ("Keywords", "In"),
            "NotContaining": ("Keywords", "NotIn"),
            "Identity": ("Keywords", "Is"),
            "NotIdentity": ("Keywords", "IsNot"),
            "Concanentation": ("Symbols", "DoubleDot"),
            "MatrixMultiplication": ("Symbols", "At"),
            "Exponentiation": ("Symbols", "DoubleAsterisk"),
            "Equality": ("Symbols", "DoubleEqual"),
            "LooseEquality": ("Symbols", "TildaAndEqual"),
            "Inequality": base.ne(),
            "LooseInequality": ("Symbols", "ExclamationAndTildaAndEqual"),
            "LessThan": ("Symbols", "LessThan"),
            "GreaterThan": ("Symbols", "GreaterThan"),
            "LessThanOrEqualTo": ("Symbols", "LessThanAndEqual"),
            "GreaterThanOrEqualTo": ("Symbols", "GreaterThanAndEqual"),
            "LeftShift": ("Symbols", "DoubleLessThan"),
            "RightShift": ("Symbols", "DoubleGreaterThan"),
            "Spaceship": base.sps()
        },

        "Ternary": {
            "ConditionSeparator": ("Symbols", "QuestionMark"),
            "ResultSeparator": ("Symbols", "Colon")
        },
        "Unary": {
            "Positive": ("Symbols", "Plus"),
            "Negative": ("Symbols", "Dash"),
            "PositionalUnpack": ("Symbols", "Asterisk"),
            "KeywordUnpack": ("Symbols", "DoubleAsterisk"),
            "Increment": ("Symbols", "DoublePlus"),
            "Decrement": ("Symbols", "DoubleDash"),
            "BinaryInversion": ("Symbols", "Tilda"),
            "HybridNot": ("Symbols", "Exclamation"),
            "LogicalNot": ("Keywords", "Not"),
            "PositionalVariadic": ("Symbols", "Asterisk"),
            "KeywordVariadic": ("Symbols", "DoubleAsterisk"),
        }
    },
    "Primitives": {
        "Int": ("Primitives", "Int"),
        "Float": ("Primitives", "Float"),
        "String": ("Primitives", "String"),
        "Boolean": base.boolean(),
        "Null": base.null(),
        "Ellipsis": ("Symbols", "TripleDot")
    },
    "Templates": {
        "InvertedComparisons": {
            "Equality": inverted_comparisons.eq(),
            "LessThan": inverted_comparisons.lt(),
            "GreaterThan": inverted_comparisons.gt(),
            "LessThanOrEqualTo": inverted_comparisons.le(),
            "GreaterThanOrEqualTo": inverted_comparisons.ge()
        }
    }
}

def get_all_itt_used(dct: dict = ALIASES) -> set:
    a = set()
    for v in dct.values():
        if isinstance(v, dict):
            a |= get_all_itt_used(v)
        elif isinstance(v, tuple):
            a.add(v)
    return a