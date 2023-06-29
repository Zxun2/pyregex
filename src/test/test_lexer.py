import pytest

from ..regex.tokens import *
from ..regex.lexer import Lexer 


@pytest.fixture
def lexer():
    return Lexer()

def test_simple_re_lexing(lexer: Lexer):
    tokens = lexer.scan('a')
    assert tokens[0].char == 'a'


def test_escaping_char(lexer: Lexer):
    tokens = lexer.scan(r'a\\a\\t\.')
    assert str(tokens[1]).split(":")[1].lstrip() == ElementToken.__name__ and tokens[1].char == '\\'


def test_escaping_get_tab(lexer: Lexer):
    tokens = lexer.scan(r'a\h\t')
    assert str(tokens[2]).split(":")[1].lstrip() == ElementToken.__name__ and tokens[2].char == '\t'


def test_escaping_wildcard(lexer: Lexer):
    tokens = lexer.scan(r'\.')
    assert str(tokens[0]).split(":")[1].lstrip() == ElementToken.__name__ and tokens[0].char == '.'


def test_get_comma(lexer: Lexer):
    tokens = lexer.scan('a{3,5}')
    assert str(tokens[3]).split(":")[1].lstrip() == Comma.__name__


def test_comma_is_element(lexer: Lexer):
    tokens = lexer.scan('a,')
    assert str(tokens[1]).split(":")[1].lstrip() == ElementToken.__name__


def test_match_start(lexer: Lexer):
    tokens = lexer.scan('^a')
    assert str(tokens[0]).split(":")[1].lstrip() == Start.__name__


def test_match_end(lexer: Lexer):
    tokens = lexer.scan(r'fdsad\$cs$')
    assert str(tokens[len(tokens) - 1]).split(":")[1].lstrip() == End.__name__


def test_fail_curly(lexer: Lexer):
    with pytest.raises(Exception):
        lexer.scan('advfe{a}')


def test_lexer_1(lexer: Lexer):
    tokens = lexer.scan(r'-\\\/\s~')
    assert len(tokens) == 5
    assert str(tokens[0]).split(":")[1].lstrip() == Dash.__name__
    assert str(tokens[1]).split(":")[1].lstrip() == ElementToken.__name__
    assert str(tokens[2]).split(":")[1].lstrip() == ElementToken.__name__
    assert str(tokens[3]).split(":")[1].lstrip() == SpaceToken.__name__
    assert str(tokens[4]).split(":")[1].lstrip() == ElementToken.__name__