import pkg_resources
import re

from typing import List

__version__ = pkg_resources.require('numaster')[0].version

_unit_map = {
    '十': 10, '拾': 10,
    '百': 100, '佰': 100, '陌': 100,
    '千': 1000, '仟': 1000, '阡': 1000,
    '万': 10000, '萬': 10000,
    '億': 10 ** 8,
    '兆': 10 ** 12,
    '割': 0.1,
    '分': 0.01, '%': 0.01, '％': 0.01,
    '厘': 0.001,
}

_number_words = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "ten": 10, "eleven": 11, "twelve": 12, "thirteen": 13, "fourteen": 14,
    "fifteen": 15, "sixteen": 16, "seventeen": 17, "eighteen": 18, "nineteen": 19,
    "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
    "seventy": 70, "eighty": 80, "ninety": 90,
}

_figure_map = {
    'hundred': 100,
    'thousand': 1000,
    'million': 10 ** 6,
    'billion': 10 ** 9,
    'trillion': 10 ** 12,
}


def has_english_number(number: str) -> bool:
    n = number.lower()
    for word in list(_number_words.keys()) + list(_figure_map.keys()):
        if word in n:
            return True
    else:
        return False


def _normalize_english(number: str) -> str:
    result = 0
    current = 0
    numbers = number.split(' ')
    length = len(numbers)
    for i, n in enumerate(numbers):
        current_number = n.lower()
        if current_number in _figure_map:
            figure_number = (1 if current == 0 else current) * _figure_map[current_number]
            if current_number == 'hundred' and i != length and numbers[i + 1] in _figure_map:
                current = figure_number
            else:
                result += figure_number
                current = 0
        else:
            current += _number_words[current_number]
    return str(result + current)

_number_map = {
    value: key for key, values in [
        ('0', ['0', '０', '零', '〇']),
        ('1', ['1', '１', '一', '壱', '壹']),
        ('2', ['2', '２', '弌', '二', '弐', '貳', '弍']),
        ('3', ['3', '３', '三', '参', '參', '弎']),
        ('4', ['4', '４', '四', '肆']),
        ('5', ['5', '５', '五', '伍']),
        ('6', ['6', '６', '六', '陸']),
        ('7', ['7', '７', '七', '漆', '柒', '質']),
        ('8', ['8', '８', '八', '捌']),
        ('9', ['9', '９', '九', '玖']),
    ] for value in values
}

# Usually Japanese people doesn't use those Kanji as number. If you need those number, you can
# compound with _number_map.
_strict_number_map = {
    value: key for key, values in [
        ('0', []),
        ('1', ['壹']),
        ('2', ['貳']),
        ('3', ['参', '參', '弎']),
        ('4', ['肆']),
        ('5', ['伍']),
        ('6', ['陸']),
        ('7', ['漆', '柒', '質']),
        ('8', ['捌']),
        ('9', ['玖']),
    ] for value in values
}

# '廿': '20', '卄': '20',
# '卅': '30', '丗': '30',
# '卌': '40',

_sub_units = {'千', '仟', '阡', '万', '萬', '億', '兆'}


extract_re = re.compile(
    '[{}]+'.format(
        ''.join(
            list(_number_map.keys()) + list(_unit_map.keys())
        )
    ), re.UNICODE
)

segment_re = re.compile(
    '([{}]*[{}])+?[{}]?'.format(
        ''.join(_number_map.keys()),
        ''.join(list(_number_map.keys()) + list(_unit_map.keys())),
        ''.join(_sub_units),
    ), re.UNICODE
)


def extract(text: str, ignore_words: List[str]=[]) -> List[str]:
    """Extract numbers.
    :text: is a source text. Find number words from this text.
    :ignore_words: are list of regex. This function ignore words that matched with it.
    """
    for ignore_word in ignore_words:
        text = re.sub(ignore_word, '#', text)  # There is no big mean for '#'.
    return [i.group() for i in extract_re.finditer(text)]


def _clean(number: str) -> str:
    if '.' not in number:
        return number

    integer, decimal = number.split('.')
    if int(decimal) == 0:
        return integer
    return number


def _normalize(number: str, decimal_point=None, separator=None) -> str:
    result = 0
    if separator is not None:
        number = number.replace(separator, '')
    if decimal_point is not None:
        number = number.replace(decimal_point, '.')

    for match in segment_re.finditer(number):
        units = []
        numbers = []
        for c in match.group():
            _c = _number_map.get(c)
            if _c is not None:
                numbers.append(_c)
                continue
            units.append(_unit_map[c])

        n = 1 if len(numbers) == 0 else int(''.join(numbers))
        if len(units) == 0:
            units.append(1)

        for unit in units:
            n *= unit
        result += n

    return _clean(str(result))


def normalize(number: str, decimal_point=None, separator=None) -> str:
    if has_english_number(number):
        return _normalize_english(number)
    else:
        return _normalize(number, decimal_point, separator)
