import re
from enum import Enum
from typing import List

import pymorphy3


class TokenEnum(Enum):
    QUERY = "QUERY"
    SELECT_WORD = "SELECT_WORD"
    COLUMNS = "COLUMNS"
    QUANTIFIER = "QUANTIFIER"
    NAME_COLUMNS = "NAME_COLUMNS"
    COLUMN_NAME = "COLUMN_NAME"
    COLUMN_EXTENSION = "COLUMN_EXTENSION"
    SEPARATOR = "SEPARATOR"
    FROM = "FROM"
    FROM_WORD = "FROM_WORD"
    TABLES = "TABLES"
    TABLE_NAME = "TABLE_NAME"
    TABLE_EXTENSION = "TABLE_EXTENSION"
    JOIN_WORD = "JOIN_WORD"
    AND_CONNECTOR = "AND_CONNECTOR"
    WHERE = "WHERE"
    WHERE_WORD = "WHERE_WORD"
    CONDITIONS = "CONDITIONS"
    COMPARISON = "COMPARISON"
    RIGHT_CONDITION = "RIGHT_CONDITION"
    NUMBER = "NUMBER"
    WORD = "WORD"
    CONDITION_EXTENSION = "CONDITION_EXTENSION"
    CONNECTOR = "CONNECTOR"
    GROUP_BY = "GROUP_BY"
    GROUP_WORD = "GROUP_WORD"
    GROUP_COLUMN = "GROUP_COLUMN"
    GROUP_EXTENSION = "GROUP_EXTENSION"
    ORDER = "ORDER"
    ORDER_WORD = "ORDER_WORD"
    ORDER_COLUMNS = "ORDER_COLUMNS"
    INDICATOR = "INDICATOR"
    ORDER_POINTER = "ORDER_POINTER"
    DESC_ANY = "DESC_ANY"
    ORDER_EXTENSION = "ORDER_EXTENSION"
    LIMIT = "LIMIT"
    LIMIT_WORD = "LIMIT_WORD"
    UNKNOWN = "UNKNOWN"

class Token:
    def __init__(self, text: str, lemma: str, token_type: TokenEnum = TokenEnum.UNKNOWN) -> None:
        self.text = text
        self.lemma = lemma
        self.token_type = token_type

    def __repr__(self) -> str:
        return f"{self.text}: ({self.lemma} {self.token_type.value})"



morph = pymorphy3.MorphAnalyzer()

KEYWORD_LEMMAS = {
    TokenEnum.SELECT_WORD: {'найти', 'показать', 'вывести'},
    TokenEnum.QUANTIFIER: {'всё'},
    TokenEnum.FROM_WORD: {'из'},
    TokenEnum.SEPARATOR: {',', ';'},
    TokenEnum.JOIN_WORD: {'соединять с', 'вместе с'},
    TokenEnum.AND_CONNECTOR: {'и'},
    TokenEnum.WHERE_WORD: {'где', 'в который'},
    TokenEnum.COMPARISON: {'<', '>', '<=', '>=', '==', '<>'},
    TokenEnum.CONNECTOR: {'или', 'также'},
    TokenEnum.GROUP_WORD: {'группировать по', 'сгруппировать по'},
    TokenEnum.ORDER_WORD: {'сортировать по'},
    TokenEnum.ORDER_POINTER: {'в порядок'},
    TokenEnum.DESC_ANY: {'возрастание', 'убывание'},
    TokenEnum.LIMIT_WORD: {'ограничиваться', 'первый'},
}

def get_keyword_type(lemma: str) -> TokenEnum:
    for token_type, lemmas in KEYWORD_LEMMAS.items():
        if lemma in lemmas:
            return token_type
    return TokenEnum.UNKNOWN

TWO_WORD_PHRASES_RAW = [
    'сортировать по',
    'в порядок',
    'в который',
    'соединять с',
    'вместе с',
    'сгруппировать по',
    'группировать по'
]

def lemmatize_word(word: str) -> str:
    return morph.parse(word)[0].normal_form

def tokenize(text: str) -> List[Token]:
    pattern = re.compile(r'<=|>=|==|<>|!=|[<>]|,|;|\d+|[а-яА-ЯёЁ0-9_]+')
    pattern_row = pattern.findall(text.lower())

    merged_raw = []
    i = 0
    while i < len(pattern_row):
        if i + 1 < len(pattern_row) and f"{lemmatize_word(pattern_row[i])} {lemmatize_word(pattern_row[i + 1])}" in TWO_WORD_PHRASES_RAW:
            merged_raw.append(f"{pattern_row[i]} {pattern_row[i + 1]}")
            i += 2
        else:
            merged_raw.append(pattern_row[i])
            i += 1

    tokens = []
    for raw in merged_raw:
        if raw.isdigit():
            tokens.append(Token(raw, raw, TokenEnum.NUMBER))
        elif raw in {'<', '>', '<=', '>=', '==', '<>', '!='}:
            tokens.append(Token(raw, raw, TokenEnum.COMPARISON))
        else:
            if ' ' in raw:
                words = raw.split()
                lemmas = [lemmatize_word(w) for w in words]
                lemma_phrase = ' '.join(lemmas)
            else:
                lemma_phrase = lemmatize_word(raw)

            token_type = get_keyword_type(lemma_phrase)
            tokens.append(Token(raw, lemma_phrase, token_type))

    return tokens