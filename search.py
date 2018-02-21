import sys
import argparse
from format_writer import FormatWriter
from string_operations import split_line, compare_strings
from constants import (MatchingLines, MESSAGE_FULL_MATCH,
                       MESSAGE_POSSIBLE_TYPOS, MESSAGE_MISMATCH)


def set_files_in_encoding(args):
    """Открывает файлы из аргументов в заданной кодирове и возвращает их"""
    output_file = None
    try:
        input_text = open(args.input_text, encoding=args.encoding)
        if args.output_file:
            output_file = open(args.output_file, 'w', encoding=args.encoding)
        alphabet = None, None
        if args.alphabet:
            alphabet = open(args.alphabet, encoding=args.encoding), False
        elif args.alphabet_with_space:
            alphabet = open(args.alphabet_with_space,
                            encoding=args.encoding), True
    except (OSError, LookupError) as e:
        print(e, file=sys.stderr)
        sys.exit(1)
    return input_text, output_file, alphabet


def create_parser():
    """Разбор аргументов запуска"""

    def percent(number):
        """Проверяет, что значение является процентом"""
        number = int(number)
        if number < 0 or number > 100:
            raise ValueError
        return number

    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encoding',
                        help='кодировка файла со словами и тектом',
                        default='utf-8')
    parser.add_argument('-p', '--progress',
                        help='показать прогрессбар',
                        action='store_true')
    parser.add_argument('-c', '--consider_case_of_letters',
                        help='учитывать регистр букв,'
                             'по умолчанию - нет',
                        action='store_true')
    parser.add_argument('-f', '--format',
                        help='выводить результат в удобном для дальнейшей'
                             'обработки формате',
                        action='store_const',
                        const=FormatWriter())
    parser.add_argument('-t', '--input_text', required=True,
                        help='файл с исходным текстом,'
                             'в котором будут искаться слова')
    parser.add_argument('-o', '--output_file',
                        help='Файл в который будет выводиться результат, '
                             'если нет, результат будет выведен на консоль')
    parser.add_argument('-a', '--alphabet',
                        help='алфавит исходного текста и искомых '
                             'слов, по умолчанию используется русский и '
                             'английский, можно задать файлом, содержащим '
                             'все символы этого алфавита, если файл с '
                             'алфавитом не найден, то будет использоваться '
                             'алфавит по умолчанию, в качестве символа '
                             'алфавита нельзя использовать пробел и символ'
                             'переноса строки чтобы его '
                             'использовать используйте "-as"')
    parser.add_argument('-as', '--alphabet_with_space',
                        help='то же, что и "-a", только в передаваемом '
                             'алфавите можно использовать пробел')
    parser.add_argument('-s', '--search_accuracy', default=0,
                        help='определяет количество возможных опечаток в '
                             'процентах в зависимости от длины слова',
                        type=percent)
    return parser.parse_args()


def close_files(files_list):
    """Закрывает файлы из переданного списка"""
    for file in files_list:
        if file:
            file.close()


def read_alphabet(file_alphabet, is_space):
    """Помещает символы алфавита из файла в множество
        и возвращает его, в зависимовти
            от опции удаляет пробел и перевод строки"""
    alphabet = set()
    if file_alphabet:
        for line in file_alphabet:
            for char in line:
                alphabet.add(char)
    if not is_space:
        alphabet -= {' ', '\n'}
    return alphabet


def output_result(args, output_file, format_result, check_word, word_search,
                  number_line, number_position):
    """Выводит результат в файл или на консоль"""
    if not args.format:
        result = ''
        if format_result == MatchingLines.MISMATCH:
            result = MESSAGE_MISMATCH.format(word_search)
        elif format_result == MatchingLines.FULL_MATCH:
            result = MESSAGE_FULL_MATCH.format(check_word,
                                               number_line,
                                               number_position)
        elif format_result == MatchingLines.POSSIBLE_TYPOS:
            result = MESSAGE_POSSIBLE_TYPOS.format(word_search,
                                                   number_line,
                                                   number_position,
                                                   check_word)
        if output_file:
            output_file.write(result + '\n')
        else:
            print(result)
    else:
        if format_result == MatchingLines.FULL_MATCH:
            args.format.add_coordinate(number_line, number_position, True)
        elif format_result == MatchingLines.POSSIBLE_TYPOS:
            args.format.add_coordinate(number_line, number_position, False)
        else:
            result = '{} {}'.format(word_search, args.format.return_coordinates())
            if output_file:
                output_file.write(result + '\n')
            else:
                print(result)


def show_progress(check_word, number_line):
    """Показывает прогресс поиска слова в файле, печатается
            проверяемое слово и номер строки"""
    print('\r', " Поиск слова '{}' в "
                "строке {}".format(check_word, number_line + 1), end='')
    print('\r', ' ' * 100, end='')
    print('\r', end='')


def split_file(file, alphabet, need_show_progress, check_word=None):
    """Разбивает файл по словам, возвращает слово, строку и позицию
        найденного слова, в зависимости от
            аргумента показывает прогресс поиска"""
    for number_line, line in enumerate(file):
        if check_word:
            if need_show_progress:
                show_progress(check_word, number_line)
        for word, number_position in split_line(line, alphabet):
            yield word, number_line + 1, number_position


def main():
    args = create_parser()
    input_text, output_file, alphabet_file = set_files_in_encoding(args)
    alphabet = read_alphabet(*alphabet_file)
    try:
        for word_search, _, _ in split_file(sys.stdin, alphabet, False):
            was_found = False
            for check_word, number_line, number_position in split_file(
                    input_text, alphabet, args.progress, word_search):
                result = compare_strings(args.search_accuracy,
                                         word_search, check_word,
                                         args.consider_case_of_letters)
                if result != MatchingLines.MISMATCH:
                    was_found = True
                    output_result(args, output_file, result, check_word,
                                  word_search, number_line, number_position)
            if not was_found or args.format:
                output_result(args, output_file, MatchingLines.MISMATCH,
                              None, word_search, None, None)
            input_text.seek(0)
    except KeyboardInterrupt:
        pass
    finally:
        close_files((input_text, output_file, alphabet_file[0]))


if __name__ == '__main__':
    main()
