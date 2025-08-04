from utils.config import CONFIG
redefine = CONFIG.language_customization.redefine

ALIASES: dict = {
    "EoF": "EoF",
    "Identifier": "Identifier",
    "NewLine": "NewLine",
    "Arrow": "Arrow",
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
            "HandleException": ("Keywords", "Catch"),
            "NoExceptions": ("Keywords", "Else"),
            "FinalCleanup": ("Keywords", "Finally"),
            "ThrowError": ("Keywords", "Throw"),
            "SourceOfThrowingError": ("Keywords", "From")
        },
        "Declarations": {
            "MutableVariable": ("Keywords", "Let"),
            "ConstantVariable": ("Keywords", "Const"),
            "Function": ("Keywords", "Fn"),
            "Class": ("Keywords", "Class"),
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
            "FallbackWithCondition": ("Keywords", "Elif"),
            "Fallback": ("Keywords", "Else")
        },
        "MatchCase": {
            "Match": ("Keywords", "Match"),
            "Case": ("Keywords", "Case"),
            "DefaultCase": ("Symbols", "Underscore"),
            "VariableBindingIntoPattern": ("Keywords", "As"),
            "VariableBinding": ("Keywords", "Let"),
            "ConditionGuard": ("Keywords", "If"),
            "PatternSeparator": ("Symbols", "Comma")
        },
        "NewScope": ("Keywords", "Scope"),
        "DirectImport": ("Keywords", "Import"),
        "ImportFrom": ("Keywords", "From"),
        "Return": ("Keywords", "Return"),
    },
    "Operators": {
        "Binary": {
            "Addition": ("Symbols", "Plus"),
            "Subtraction": ("Symbols", "Dash"),
            "Multiplication": ("Symbols", "Asterisk"),
            "TrueDivision": ("Symbols", "ForwardSlash"),
            "FloorDivision": ("Symbols", "DoubleForwardSlash"),
            "Modulus": ("Symbols", "Percent"),
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
            "Inequality": ("Symbols", "ExclamationAndEqual"),
            "LessThan": ("Symbols", "LessThan"),
            "GreaterThan": ("Symbols", "GreaterThan"),
            "LessThanOrEqualTo": ("Symbols", "LessThanAndEqual"),
            "GreaterThanOrEqualTo": ("Symbols", "GreaterThanAndEqual"),
            "LeftShift": ("Symbols", "DoubleLessThan"),
            "RightShift": ("Symbols", "DoubleGreaterThan")
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
        "Boolean": ("Primitives", "Boolean"),
        "Null": ("Primitives", "Null"),
        "Ellipsis": ("Symbols", "TripleDot")
    }
}



def ineq():
    match redefine.inequality:
        case "!=":
            return "Symbols", "ExclamationAndEqual"
        case "<>":
            return "Symbols", "Diamond"
        case "><":
            return "Symbols", "InvertedDiamond"

def sps():
    match redefine.spaceship_operator:
        case "<=>":
            return "Symbols", "SpaceCapsule"
        case ">=<":
            return "Symbols", "QuirkyLookingFace"


# & You can't stop me from editing the uneditable >:)
ALIASES["Statements"]["Declarations"].update({
    "Class": ("Keywords", redefine.class_def.title()),
    "Function": ("Keywords", redefine.function_def.title())
})

ALIASES["Statements"]["Conditional"].update({
    "FallbackWithCondition": ("Keywords", redefine.else_if.title().replace(" ", ""))
})

ALIASES["Operators"]["Binary"].update({
    "Inequality": ineq(),
    "Spaceship": sps()
})