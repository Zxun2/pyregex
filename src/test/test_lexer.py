import pytest

from regex.tokens import *
from regex.lexer import Lexer 

def transform(token: Token) -> str:
    return str(token).split(":")[1].lstrip()

@pytest.fixture
def lexer():
    return Lexer()

def test_simple_re_lexing(lexer: Lexer):
    tokens = lexer.scan('a')
    assert tokens[0].char == 'a'


def test_escaping_char(lexer: Lexer):
    tokens = lexer.scan(r'a\\a\\t\.')
    assert transform(tokens[1]) == ElementToken.__name__ and tokens[1].char == '\\'


def test_escaping_get_tab(lexer: Lexer):
    tokens = lexer.scan(r'a\h\t')
    assert transform(tokens[2]) == ElementToken.__name__ and tokens[2].char == '\t'


def test_escaping_wildcard(lexer: Lexer):
    tokens = lexer.scan(r'\.')
    assert transform(tokens[0]) == ElementToken.__name__ and tokens[0].char == '.'


def test_get_comma(lexer: Lexer):
    tokens = lexer.scan('a{3,5}')
    assert transform(tokens[3]) == Comma.__name__


def test_comma_is_element(lexer: Lexer):
    tokens = lexer.scan('a,')
    assert transform(tokens[1]) == ElementToken.__name__


def test_match_start(lexer: Lexer):
    tokens = lexer.scan('^a')
    assert transform(tokens[0]) == Start.__name__


def test_match_end(lexer: Lexer):
    tokens = lexer.scan(r'fdsad\$cs$')
    assert transform(tokens[len(tokens) - 1]) == End.__name__


def test_fail_curly(lexer: Lexer):
    with pytest.raises(Exception):
        lexer.scan('advfe{a}')


def test_lexer_1(lexer: Lexer):
    tokens = lexer.scan(r'-\\\/\s~')
    assert len(tokens) == 5
    assert transform(tokens[0]) == Dash.__name__
    assert transform(tokens[1]) == ElementToken.__name__
    assert transform(tokens[2]) == ElementToken.__name__
    assert transform(tokens[3]) == SpaceToken.__name__
    assert transform(tokens[4]) == ElementToken.__name__