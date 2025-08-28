from backend.config import CONFIG
import parser.lexer.data.modifiers.operators as operators
import parser.lexer.data.modifiers.statements as stmts
import parser.lexer.data.modifiers.base as base
cust = CONFIG.customization
objects = cust.objects
operators_conf = cust.operators
control_flow = cust.control_flow
classic_conditional = cust.control_flow.conditional.classic
match_conditional = cust.control_flow.conditional.match_case
switch_conditional = cust.control_flow.conditional.switch_case
exception_handling = control_flow.exception_handling
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
            "ExceptionTest": stmts.try_(),
            "HandleException": stmts.catch_expections(),
            "NoExceptions": stmts.no_exceptions(),
            "FinalCleanup": stmts.final_cleanup(),
            "ThrowError": stmts.throw_error(),
            "SourceOfThrowingError": ("Keywords", "From")
        },
        "Declarations": {
            "MutableVariable": ("Keywords", "Let"),
            "ConstantVariable": ("Keywords", "Const"),
            "Function": stmts.function_decl(),
            "Class": stmts.class_decl(),
            "Enum": stmts.enum_decl(),
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
            "Condition": stmts.if_(),
            "FallbackWithCondition": stmts.elif_(),
            "Fallback": stmts.else_()
        },
        "MatchCase": {
            "Match": stmts.match(),
            "Case": ("Keywords", "Case"),
            "DefaultCase": stmts.match_default_case(),
            "VariableBindingIntoPattern": ("Keywords", "As"),
            "VariableBinding": ("Keywords", "Let"),
            "ConditionGuard": ("Keywords", "If"),
            "PatternSeparator": ("Symbols", "Comma")
        },
        "SwitchCase": {
            "Switch": stmts.switch(),
            "Case": ("Keywords", "Case"),
            "DefaultCase": stmts.switch_default_case(),
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
            "Addition": operators.addition(),
            "Subtraction": operators.subtraction(),
            "Multiplication": operators.multiplication(),
            "TrueDivision": operators.true_division(),
            "FloorDivision": operators.floor_division(),
            "Modulus": operators.modulus(),
            "LogicalOr": operators.logical_or(),
            "LogicalAnd": operators.logical_and(),
            "LogicalXor": operators.logical_xor(),
            "HybridOr": operators.booleans_or(),
            "HybridAnd": operators.booleans_and(),
            "HybridXor": operators.booleans_xor(),
            "BinaryOr": operators.binary_or(),
            "BinaryAnd": operators.binary_and(),
            "BinaryXor": operators.binary_xor(),
            "Containing": ("Keywords", "In"),
            "NotContaining": ("Keywords", "NotIn"),
            "Identity": ("Keywords", "Is"),
            "NotIdentity": ("Keywords", "IsNot"),
            "Concanentation": operators.string_concanentation(),
            "MatrixMultiplication": operators.matrix_multiplication(),
            "Exponentiation": ("Symbols", "DoubleAsterisk"),
            "Equality": operators.eq(),
            "LooseEquality": operators.loose_eq(),
            "Inequality": operators.ne(),
            "LooseInequality": operators.loose_ne(),
            "LessThan": ("Symbols", "LessThan"),
            "GreaterThan": ("Symbols", "GreaterThan"),
            "LessThanOrEqualTo": ("Symbols", "LessThanAndEqual"),
            "GreaterThanOrEqualTo": ("Symbols", "GreaterThanAndEqual"),
            "LeftShift": ("Symbols", "DoubleLessThan"),
            "RightShift": ("Symbols", "DoubleGreaterThan"),
            "Spaceship": operators.sps()
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