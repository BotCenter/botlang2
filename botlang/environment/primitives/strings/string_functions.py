import json
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

    # Some of the algorithms below misbehave in the presence of empty strings. So we treat these cases beforehand.
    if str1 == "" and str2 == "":
        return 1.0
    elif str1 == "" or str2 == "":
        return 0.0

    sequence_based_distance = textdistance.lcsstr.normalized_similarity(
        str1, str2
    )
    edit_based_distance = textdistance.jaro.normalized_similarity(
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

    # If the string is made up of stop words, we don't remove anything.

    if all(x in stop_words for x in string.lower().split(' ')):
        return string

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
                        # Add to words_to_remove set.
                        words_to_remove.add(token)
                        # Remove some variations too
                        if len(token) > 6:
                            words_to_remove.add(token[:-1])

        # Remove longest words first.
        words_to_remove = sorted(list(words_to_remove), reverse=True)
        return [
            reduce(
                lambda acc, n: acc.replace(n, ''), words_to_remove, string
            ).strip()
            for string in strings_list
        ], words_to_remove
    else:
        return strings_list, []


def get_stop_words(lang):
    if lang == 'ES':
        return STOPWORDS_ES
    else:
        raise Exception('Language not supported')


def get_exact_match(string, list_of_strings):
    for option in list_of_strings:
        if option.strip() == string.strip():
            return string


def string_find_similar(string, list_of_strings, threshold=0.3, lang='ES'):

    stop_words = get_stop_words(lang)

    exact_match = get_exact_match(string, list_of_strings)
    if exact_match is not None:
        return exact_match

    clean_strings, words_removed = remove_same_words([
        remove_stop_words(s, stop_words) for s in list_of_strings
    ])
    words_to_remove = [unidecode(s.lower()) for s in words_removed]

    comparison_string = remove_stop_words(string, stop_words)
    for to_remove in words_to_remove:
        comparison_string = comparison_string.replace(to_remove, '')
    comparison_string = ' '.join(w for w in comparison_string.split(' ') if w)

    if len(comparison_string) == 0:
        return Nil

    simple_strings = [unidecode(s.lower()) for s in clean_strings]
    similarities = [
        (original, string_similarity(comparison_string, clean))
        for original, clean in zip(list_of_strings, simple_strings)
    ]
    similarities.sort(key=lambda s: s[1], reverse=True)
    most_similar = similarities[0]
    if most_similar[1] >= threshold:
        return most_similar[0]
    else:
        return Nil


STRING_OPS = {
    'capitalize': str.capitalize,
    'divide-text': divide_text,
    'format': str.format,
    'from-json': lambda s: json.loads(s),
    'join': str.join,
    'lowercase': str.lower,
    'match': pattern_match,
    'match?': lambda p, s: pattern_match(p, s) is not Nil,
    'plain': simplify_text,
    'replace': str.replace,
    'split': str.split,
    'string-find-similar': string_find_similar,
    'trim': str.strip,
    'uppercase': str.upper,
    'url-quote': quote
}
