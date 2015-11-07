import re

from typing import List

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

_number_map = {
    '0': '0', '０': '0', '零': '0', '〇': '0',
    '1': '1', '１': '1', '一': '1', '壱': '1', '壹': '1',
    '2': '2', '２': '2', '弌': '2', '二': '2', '弐': '2', '貳': '2', '弍': '2',
    '3': '3', '３': '3', '三': '3', '参': '3', '參': '3', '弎': '3',
    '4': '4', '４': '4', '四': '4', '肆': '4',
    '5': '5', '５': '5', '五': '5', '伍': '5',
    '6': '6', '６': '6', '六': '6', '陸': '6',
    '7': '7', '７': '7', '七': '7', '漆': '7', '柒': '7', '質': '7',
    '8': '8', '８': '8', '八': '8', '捌': '8',
    '9': '9', '９': '9', '九': '9', '玖': '9',
    # '廿': '20', '卄': '20',
    # '卅': '30', '丗': '30',
    # '卌': '40',
}

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


def extract(text: str) -> List[str]:
    return [i.group() for i in extract_re.finditer(text)]


def _clean(number: str) -> str:
    if '.' not in number:
        return number

    integer, decimal = number.split('.')
    if int(decimal) == 0:
        return integer
    return number


def normalize(number: str, decimal_point=None, separator=None) -> str:
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
