"""Несколько методов со строками"""
from constants import MatchingLines


def split_line(line, alphabet):
    """Разбивает строку по символам, не входящим в алфавит,
        если алфавит пустой, разбивается по символам, не
            являющимися буквами"""
    def is_char_in_alphabet(ch):
        if len(alphabet) == 0:
            return ch.isalpha()
        return ch in alphabet

    start_word_pos = -1
    line = line.rstrip()
    for pos, char in enumerate(line):
        if is_char_in_alphabet(char):
            if start_word_pos == -1:
                start_word_pos = pos
        else:
            if start_word_pos != -1:
                if line[start_word_pos:pos]:
                    yield line[start_word_pos:pos], start_word_pos + 1
                start_word_pos = pos + 1
    if start_word_pos != -1:
        if line[start_word_pos:]:
            yield line[start_word_pos:], start_word_pos + 1


def levenshtein_distance(first, second):
    """Возвращает минимальное количество операций, необходимых для
        получения одной строки из другой"""
    lengths = len(first), len(second)
    if min(lengths) == 0:
        return max(lengths)
    opt = [[0] * (len(second) + 1) for _ in range(len(first) + 1)]
    for i in range(len(first) + 1):
        opt[i][0] = i
    for i in range(len(second) + 1):
        opt[0][i] = i
    for i in range(1, len(first) + 1):
        for j in range(1, len(second) + 1):
            if first[i - 1] == second[j - 1]:
                opt[i][j] = opt[i - 1][j - 1]
            else:
                opt[i][j] = 1 + min(opt[i - 1][j],
                                    opt[i][j - 1],
                                    opt[i - 1][j - 1])
    return opt[len(first)][len(second)]


def count_max_number_types(search_accuracy, first_len, second_len):
    """В зависимости от опции, возвращает максимальное количество опечаток,
        которое можно совершить в слове"""
    max_length = max(first_len, second_len)
    max_count_types = (search_accuracy * max_length) // 100
    return max_count_types


def compare_strings(search_accuracy, first, second,
                    consider_case_of_letters=False):
    """Сравнивает строки, они могул либо полностью совпасть,
        либо совпать с учётом возможных опечаток,
            либо не совпасть"""
    if not consider_case_of_letters:
        first = first.lower()
        second = second.lower()
    count_typos = levenshtein_distance(first, second)
    max_count_types = count_max_number_types(search_accuracy,
                                             len(first),
                                             len(second))
    if count_typos == 0:
        return MatchingLines.FULL_MATCH
    if count_typos > max_count_types:
        return MatchingLines.MISMATCH
    return MatchingLines.POSSIBLE_TYPOS
