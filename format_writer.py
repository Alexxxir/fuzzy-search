class FormatWriter:
    """Умеет добавлять в строку координаты слов и возвращать полученную строку"""
    def __init__(self):
        self.word_coordinates = ''

    def add_coordinate(self, num_line, num_pos, is_full_match):
        if is_full_match:
            string = '{},{} '
        else:
            string = '{},{}? '
        self.word_coordinates += string.format(str(num_line), str(num_pos))

    def return_coordinates(self):
        string = self.word_coordinates
        self.word_coordinates = ''
        return string
