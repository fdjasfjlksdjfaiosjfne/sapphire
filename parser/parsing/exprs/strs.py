import string
import typing

from backend import errors
import parser.nodes as Nodes

class Strings:
    def process_string(self, value: str) -> Nodes.StrNode | Nodes.FormattedStrNode:
        types, content, multi_line = self.extract_str_content(value)
        if "r" not in types:
            content = self.process_escapes(content)
        
        if "f" in types:
            return self.parse_fstring_content(content)
        else:
            return Nodes.StrNode(content)
    
    @staticmethod
    def extract_str_content(value: str) -> tuple[str, str, bool]:
        quote_used = value[-1]
        prefix_end = value.find(quote_used)
        prefixes = value[:prefix_end].lower()

        if value[prefix_end:prefix_end+3] == quote_used*3:
            multi_str = True
            content = value[prefix_end+3:-3]
        else:
            multi_str = False
            content = value[prefix_end+1:-1]
        
        return prefixes, content, multi_str

    @staticmethod
    def process_escapes(content: str) -> str:
        escape_map = {
            '"': "\"", "'": "\'", "`": "`",
            "n": "\n", "t": "\t", "r": "\r",
            "b": "\b", "f": "\f", "v": "\v",
            "a": "\a", "\\": "\\", "\n": ""
        }
        res = []
        i = 0
        while i < len(content):
            if content[i] == "\\":
                esc = content[i + 1]
                i += 2

                if esc == "x":
                    # ^ Hexadecimal escape sequence
                    ## \xHH
                    hex_digits = content[i : i + 2]
                    if (
                        len(hex_digits) != 2 or
                        not all(
                            c in string.hexdigits for c in hex_digits
                        )):
                        raise errors.SyntaxError(f"Invalid '\\x' escape (\\x{hex_digits})")
                    res.append(chr(int(hex_digits, 16)))
                    i += 2
                
                elif esc in string.octdigits:
                    # ^ Octal escape sequence
                    ## \o | \oo | \ooo
                    i += 1
                    if content[i] in string.octdigits:
                        esc += content[i]
                        i += 1
                        if content[i] in string.octdigits:
                            esc += content[i]
                            i += 1
                    res.append(chr(int(esc, 8)))
                
                elif esc.lower() == "u":
                    # ^ Unicode hex code
                    ## \uXXXX (4 digits)
                    expected_len = 4 if esc == "u" else 8
                    unicode_code = content[i : i + expected_len]
                    if (
                        len(unicode_code) != expected_len or
                        not all(
                        c in string.hexdigits for c in unicode_code
                    )):
                        raise errors.SyntaxError(f"Invalid Unicode escape sequence ({unicode_code})")
                    res.append(chr(int(unicode_code, 16)))
                    i += 4
                
                elif esc == "N":
                    # ^ Unicode name thing
                    ## \N{...}
                    import unicodedata
                    end_pos = content.find("}", i)
                    name = content[i + 3 : end_pos]
                    i += len(name) + 3
                    try:
                        res.append(unicodedata.lookup(name))
                    except KeyError:
                        raise errors.SyntaxError(fr"Unable to found the name type in \N (name being ({name}))")
                
                elif content[i] in escape_map:
                    res.append(escape_map[content[i]])
                    i += len(content[i])
                
                else:
                    raise errors.SyntaxError(fr"Invalid escape character ('\{content[i]}')")
            else:
                res.append(content[i])
                i += 1
        return ''.join(res)

    @staticmethod
    def scan_fstring_expr(content: str, start: int) -> tuple[str, int]:
        """Scan for f-string expression from `content[start:]`, accounting for nested braces.

Returns: A tuple of (inner_expression_text, index_after_closing_brace)
"""
        brace_depth = 0
        i = start
        while i < len(content):
            match content[i]:
                case "{":
                    brace_depth += 1
                case "}":
                    brace_depth -= 1
                    if brace_depth == 0:
                        return content[start + 1 : i], i + 1
            i += 1
        raise errors.SyntaxError("Unclosed '{' in f-string exprssion")

    def parse_fstring_content(self, content: str) -> Nodes.FormattedStrNode:
        contents = []
        cur = 0
        
        def append_new_str(val: str):
            nonlocal cur
            if content[cur : cur + len(val)] != val:
                raise errors.InternalError(
                    "'val' doesn't match the content of the string"
                )
            if isinstance(contents[-1], Nodes.StrNode):
                contents[-1].value += val
            else:
                contents.append(Nodes.StrNode(val))
            cur += len(val)

        while cur < len(content):
            if content[cur] == "{":
                if content[cur + 1] == "{":
                    # Escaped '{{'
                    append_new_str(content[cur : cur + 2])
                    continue

                # $ Formatted value
                conversion = -1
                formatting = None

                inner, cur = self.scan_fstring_expr(content, cur)

                from parser.parser import Parser
                parser = Parser(inner)
                expr = parser.parse_expr()
                remaining = parser.tokens.remaining()
                cur += len(parser.tokens.consumed())
                if remaining.startswith("!"):
                    conversion = ord(remaining[1])
                    remaining = remaining[2:]

                if remaining.startswith(":"):
                    # ~ This may or may not be a good idea...
                    formatting = self.parse_fstring_content(remaining)
                    if not formatting.values:
                        formatting = None
                
                if remaining:
                    # TODO
                    raise errors.SyntaxError("<insert msg here>")

                contents.append(Nodes.FormattedValue(expr, conversion, formatting))
            elif content[cur] == "}":
                if cur + 1 < len(content) and content[cur + 1] == "}":
                    # Escaped '}}'
                    append_new_str(content[cur : cur + 2])
                else:
                    print("WARNING: stray '}' found in f-string")
                    cur += 1
            else:
                next_start = content.find("{", cur)
                next_end = content.find("}", cur)
                next_stop = min(
                    x for x in (next_start, next_end, len(content)) if x != -1
                )
                append_new_str(content[cur:next_stop])
        return Nodes.FormattedStrNode(contents)