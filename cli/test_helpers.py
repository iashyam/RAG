import pytest
import helpers as mod
import ast

def RUN(function: ast.FunctionDef , test_cases: list[dict]):

    for test_case in test_cases:

        if "kwargs" not in test_case.keys(): test_case["kwargs"]={}
        if "want_error" not in test_case.keys(): test_case["want_error"]=False

        if test_case["want_error"]:
            flag = False
            try: 
                got = function(*test_case["args"], **test_case["kwargs"])
            except:
                flag = True
            assert flag , f"Wanted an error but got none"
            return

        got = function(*test_case["args"], **test_case["kwargs"])
        assert got == test_case["want"], f"{test_case["want"]=}, {got=} "



def test_simplify():

    test_cases = [
        {
            "args": ["Boots the bear!"],
            "want": "boots the bear",
            "want_error": False
        },
        {
            "args": ["The wonderful bear, Boots "],
            "want": "the wonderful bear boots",
            "want_error": False
        },
        {
            "args": [23],
            "kwargs": {},
            "want": "the wonderful bear, boots",
            "want_error": True
        },
    ]

    RUN(mod.simplify, test_cases)


def test_tokenize():

    test_cases = [
        {
            "args": ["The Matrix is a great film!"],
            "kwargs": {},
            "want": ["the", "matrix", "is", "a", "great", "film"],
            "want_error" : False
        }
    ]

    RUN(mod.tokenise, test_cases=test_cases)

def test_add():

    test_cases = [
        {
            "args": [1, 2],
            "want": 3,
            "want_error": False,
        },
        {
            "args": [3, 2],
            "want": 5,
            "want_error": False,
        }, 
        {
            "args": ["1", 3],
            "want": 4,
            "want_error": True
        }
    ]
    
    RUN(mod.add, test_cases=test_cases)

def test_remove_stop_words():
    test_cases = [
        {
            "args": ["the bear", ["the", "a", "an"]],
            "want": "bear",
            "want_error": False,
        },
        {
            "args": ["the hot shot", ["the", "a", "an"]],
            "want": "hot shot",
            "want_error": False,
        },
    ]

    RUN(mod.remove_stop_words, test_cases=test_cases)

def test_stem():
    test_cases = [
        {"args": ["running"], "want": "run"},
        {"args": ["runs"], "want": "run"},
        {"args": ["jumped"], "want": "jump"},
        {"args": ["watched"], "want": "watch"}
    ]    

    RUN(mod.stem, test_cases=test_cases)

if __name__=="__main__":
    test_simplify()
    test_tokenize()
    test_stem()
