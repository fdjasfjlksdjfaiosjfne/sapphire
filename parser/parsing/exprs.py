import sys; sys.dont_write_bytecode = True
from typing import *
from lexer.tokens import TokenType, Token
from ..ast import *

# TODO
#^ Orders Of Precedence:
# @ PARENTHESES ()
# * PrimaryExpr
## Call()
## Subscription[], member.access
## Unary Operators (!, not, ~, -, +, ++, --)
## "**"
## "*" / "/" / "%"
## "+" / "-"
## "|>"
## "<" / ">" / ">=" / "<=" / "==" / "!="
## "<<" / ">>"
## "b&"
## "b^"
## "b|"
## "&" and
## "|" or
## "^" xor
## Ternary Operator (a ? b : c)
## [1, 2, 3, 4] {1, 2, 3, 4} {"a": "b"} {a: "b"}
## Assignment Operator (:=)

