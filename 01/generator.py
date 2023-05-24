from io import TextIOWrapper
from typing import List


def filter_lines(
    filename: str | TextIOWrapper, words: List[str], encoding: str = "utf-8"
) -> str:
    words = [word.lower() for word in words]
    if isinstance(filename, str):
        with open(filename, "r", encoding=encoding) as file:
            for line in file:
                line_words = set(line.lower().split())
                if line_words.intersection(words):
                    yield line.strip()
    else:
        for line in filename:
            line_words = set(line.lower().split())
            if line_words.intersection(words):
                yield line.strip()
