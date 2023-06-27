from typing import List
from re_tokens import *

class Lexer:
    """ Lexer class.

    This class contains the method to scan a regular expression string producing the corresponding tokens.
    """

    def __init__(self) -> None:
        self.__digits__ = '0123456789'

    def __is_digit__(self, ch: str) -> bool:
        return self.__digits__.find(ch) > -1
    
    # Taken from https://stackoverflow.com/a/21605790/17661870
    def str_to_raw(self, s):
        raw_map = {8:r'\b', 7:r'\a', 12:r'\f', 10:r'\n', 13:r'\r', 9:r'\t', 11:r'\v', 92:r'\\'}
        return r''.join(i if ord(i) > 32 else raw_map.get(ord(i), i) for i in s)

    def scan(self, re: str) -> List[Token]:
        """ Regular expressions scanner.

        Scans the regular expression in input and produces the list of recognized Tokens in output.
        It raises an Exception if there are errors in the regular expression.

        Args:
            re (str): the regular expression to scan

        Returns:
            List[Token]: the list of tokens recognized in the passed regex
        """
        re = self.str_to_raw(re)
        tokens = []

        def append(elem: Token) -> None:
            nonlocal tokens
            tokens.append(elem)

        i = 0
        escape_found = False
        while i < len(re):
            ch = re[i]
            match ch:
                case _ if escape_found:
                    if ch == 't':
                        append(ElementToken(char='\t'))
                    if ch == 's':
                        # \s matches a space character
                        append(SpaceToken(char="")) # doesn't matter what is passed in
                    else:
                        append(ElementToken(char=ch))
                case '\\':
                    escape_found = True
                    i += 1  # otherwise i won't be incremented bc of continue
                    continue
                case '.':
                    append(Wildcard())
                case '(':
                    append(LeftParenthesis())
                case ')':
                    append(RightParenthesis())
                case '[':
                    append(LeftBracket())
                case '-':
                    append(Dash())
                case ']':
                    append(RightBracket())
                case '{':
                    '''
                    {n} matches exactly n occurrences of the preceding element.
                    {n,} matches n or more occurrences of the preceding element.
                    {n,m} matches at least n and at most m occurrences of the preceding element.
                    '''
                    append(LeftCurlyBrace())
                    i += 1
                    while i < len(re):
                        ch = re[i]
                        match ch:
                            case ',':
                                append(Comma())
                            case _ if self.__is_digit__(ch):
                                append(ElementToken(char=ch))
                            case '}':
                                append(RightCurlyBrace())
                                break
                            case _:
                                raise Exception("Bad token at index ${}.".format(i))
                        i += 1
                case '^' if i == 0:
                    append(Start())
                case '$':
                    append(End())
                case '?':
                    append(QuestionMark())
                case '*':
                    append(Asterisk())
                case '+':
                    append(Plus())
                case '|':
                    append(VerticalBar())
                case '}':
                    append(RightCurlyBrace())
                case _:
                    append(ElementToken(char=ch))

            escape_found = False
            i += 1

        return tokens