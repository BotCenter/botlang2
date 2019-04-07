import re
from functools import reduce
from urllib.parse import quote

import textdistance
from unidecode import unidecode

from botlang.environment.primitives.strings.stopwords_es import STOPWORDS_ES
from botlang.evaluation.values import Nil


def simplify_text(text):

    return unidecode(text)\
        .lower()\
        .replace("'", '')\
        .replace('&', '')


def pattern_match(pattern, message, group=0):
    match = re.match(pattern, message)
    if match:
        return match.group(group)
    return Nil


def divide_text(max_chars, text):

    if len(text) <= max_chars:
        return [text]

    texts = []
    for p in re.split('\n', text):
        stripped_p = p.strip()
        if len(stripped_p) > 0:
            texts.append(stripped_p)

    return texts


def string_similarity(string1, string2):

    str1 = simplify_text(string1)
    str2 = simplify_text(string2)

    sequence_based_distance = textdistance.lcsstr.normalized_similarity(
        str1, str2
    )
    edit_based_distance = textdistance.smith_waterman.normalized_similarity(
        str1, str2
    )
    token_based_distance = textdistance.cosine.normalized_similarity(
        str1.split(' '), str2.split(' ')
    )
    return sum([
        sequence_based_distance, edit_based_distance, token_based_distance
    ]) / 3


def remove_stop_words(string, stop_words):

    clean_string = string
    for word in string.split(' '):
        if word.lower() in stop_words:
            clean_string = re.sub(r'\s+', ' ', clean_string.replace(word, ''))
    return clean_string


def remove_same_words(strings_list):

    length = len(strings_list)
    if length > 1:
        words_to_remove = set()
        for i in range(0, length - 1):
            tokens1 = strings_list[i].split(' ')
            for j in range(i + 1, length):
                tokens2 = strings_list[j].split(' ')
                for token in tokens1:
                    if token in tokens2:
                        words_to_remove.add(token)

        return [
            reduce(
                lambda acc, n: acc.replace(n, ''), words_to_remove, string
            ).strip()
            for string in strings_list
        ]
    else:
        return strings_list


def string_find_similar(string, list_of_strings, threshold=0.3, lang='ES'):

    if lang == 'ES':
        stop_words = STOPWORDS_ES
    else:
        raise Exception('Language not supported')

    clean_strings = remove_same_words([
        remove_stop_words(s, stop_words) for s in list_of_strings
    ])
    comparison_string = remove_stop_words(string.lower(), stop_words)
    similarities = [
        (original, string_similarity(comparison_string, clean))
        for original, clean in zip(list_of_strings, clean_strings)
    ]
    similarities.sort(key=lambda s: s[1], reverse=True)
    most_similar = similarities[0]
    if most_similar[1] >= threshold:
        return most_similar[0]
    else:
        return Nil


STRING_OPS = {
    'split': str.split,
    'join': str.join,
    'plain': simplify_text,
    'uppercase': str.upper,
    'lowercase': str.lower,
    'capitalize': str.capitalize,
    'replace': str.replace,
    'trim': str.strip,
    'match': pattern_match,
    'match?': lambda p, s: pattern_match(p, s) is not Nil,
    'string-find-similar': string_find_similar,
    'divide-text': divide_text,
    'url-quote': quote
}

