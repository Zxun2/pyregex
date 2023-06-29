from ..regex.tokens import *


def test_Asterisk():
    assert issubclass(Asterisk, ZeroOrMore)

    a = Asterisk()
    assert a is not None

    assert type(a) == Asterisk


def test_NotToken():
    assert issubclass(NotToken, Token) == True

    nt = NotToken(char='^')
    assert nt is not None
    assert nt.char == '^'


def test_Bracket():
    br = Bracket()
    assert br is not None
    br = LeftSquareBracket()
    assert br is not None
    br = RightSquareBracket()
    assert br is not None


def test_Escape():
    escape = Escape()
    assert escape is not None