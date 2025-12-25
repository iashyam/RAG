import string
from nltk.stem import PorterStemmer
from pathlib import Path

def get_stop_words(file: Path) -> list[str]:
    ''' you know what it does'''
    if not file.exists():
        raise FileNotFoundError(f"file {file} doesn't exists")
    
    with open(file, "r", encoding="utf-8") as f:
        stop_words = []
        for line in f:
            stop_words.append(line.strip())
        return stop_words

STOP_WORDS = get_stop_words(Path("data/stop_words.txt"))

def simplify(s: str):
    '''remove punctuations and make lowercase for a string'''
    punctuations = '''!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~''' #string.punctuation #get all the punctuation makrs
    trans_map = s.maketrans({p:"" for p in punctuations})

    return s.translate(trans_map).lower().strip()

def stem(s: str)->str:
    ''' reduces words to their root forms'''
    stemmer = PorterStemmer()
    return stemmer.stem(s)

def tokenise(s: str) -> list[str]:
    ''' breaks the string into chuncks of test '''
    simple_string = simplify(s)
    tokens = simple_string.split()
    tokens = [stem(token) for token in tokens if token not in STOP_WORDS]
    return tokens

def add(a: int, b: int) -> int:
    ''' adds to numbers of returns the sum'''
    return a+b

def remove_stop_words(s: str, stop_words: list[str]) -> str:
    ''' remove the stop words (commonly occuring words)'''

    tokens = tokenise(s)
    
    return " ".join(token for token in tokens if token not in stop_words)
