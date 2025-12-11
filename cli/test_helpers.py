import pytest
import helpers as mod
from helpers import *
from dataclasses import dataclass, field
from typing import Any, Callable, Type, Tuple
import ast

@dataclass
class Case:
    #inputs
    args: Tuple[Any, ...]
    want: Any | Tuple[Any] | None = None

    kwargs: dict[str, Any] | None = field(default_factory=dict)
    exception: Type[Exception] | Tuple[Type[Exception], ...] = Exception
    want_error: bool = False
    name: str | None = None

def RUN(function: Callable, test_cases: list[Case]):

    for test_case in test_cases:
        if test_case.want_error:
            with pytest.raises(test_case.exception):
                function(*test_case.args, **test_case.kwargs)
        else:
            got = function(*test_case.args, **test_case.kwargs)
            assert got == test_case.want, f"{test_case.want=}, {got=} "


def test_simplify():

    test_cases = [
        {
            "args": ["Boots the bear!"],
            "want": "boots the bear",
        },
        {
            "args": ["The wonderful bear, Boots "],
            "want": "the wonderful bear boots",
        },
        {
            "args": [23],
            "kwargs": {},
            "want": "the wonderful bear, boots",
            "want_error": True,
            "exception": AttributeError
        },
    ]

    test_cases = [Case(**things) for things in test_cases]
    RUN(mod.simplify, test_cases)


def test_tokenize():

    test_cases = [
        {
            "args": ["The Matrix is a great film!"],
            "want": ["the", "matrix", "is", "a", "great", "film"],
        }
    ]

    test_cases = [Case(**things) for things in test_cases]
    RUN(mod.tokenise, test_cases=test_cases)

def test_add():

    test_cases = [
        {
            "args": [1, 2],
            "want": 3,
        },
        {
            "args": [3, 2],
            "want": 5,
        }, 
        {
            "args": ["1", 3],
            "want": 4,
            "want_error": True,
            "exception": TypeError
        }
    ]
    
    test_cases = [Case(**things) for things in test_cases]
    RUN(mod.add, test_cases=test_cases)

def test_remove_stop_words():
    test_cases = [
        {
            "args": ["the bear", ["the", "a", "an"]],
            "want": "bear",
        },
        {
            "args": ["the hot shot", ["the", "a", "an"]],
            "want": "hot shot",
        },
    ]

    test_cases = [Case(**things) for things in test_cases]
    RUN(mod.remove_stop_words, test_cases=test_cases)

def test_stem():
    test_cases = [
        {"args": ["running"], "want": "run"},
        {"args": ["runs"], "want": "run"},
        {"args": ["jumped"], "want": "jump"},
        {"args": ["watched"], "want": "watch"}
    ]    

    test_cases = [Case(**things) for things in test_cases]
    RUN(mod.stem, test_cases=test_cases)

if __name__=="__main__":
    test_simplify()
    test_tokenize()
    test_stem()
