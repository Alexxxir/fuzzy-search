from enum import Enum


class MatchingLines(Enum):
    FULL_MATCH = 1
    POSSIBLE_TYPOS = 2
    MISMATCH = 3


MESSAGE_FULL_MATCH = "Слово '{}' было найдено в {} строке, {} позиция"
MESSAGE_POSSIBLE_TYPOS = ("Слово '{}' возможно было написано с опечаткой"
                          " в {} строке, {} позиция, найдено '{}'")
MESSAGE_MISMATCH = "Слово '{}' не найдено в тексте"
