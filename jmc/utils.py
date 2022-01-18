import regex
import re
from typing import Tuple, List

from . import Logger

logger = Logger(__name__)


class BracketRegex:
    match_bracket_count = 0

    def __init__(self) -> None:
        self.remove_list = []

    def compile(self, strings: Tuple[str]) -> Tuple[str]:
        strings = list(strings)
        for index in sorted(self.remove_list, reverse=True):
            del strings[index-1]
        return tuple(strings)

    def match_bracket(self, bracket: str, start_group: int) -> str:
        start_group += self.match_bracket_count * 3
        self.match_bracket_count += 1
        self.remove_list += [start_group, start_group+2, start_group+3]
        return f'(\\{bracket[0]}((?:(?:(\\\\*["\'])(?:(?=(\\\\?))\\{start_group+3}.)*?\\{start_group+2}|[^{bracket[1]}{bracket[0]}])+|(?{start_group}))*+)\\{bracket[1]})'


def split(string: str, split_item: str = ',') -> List[str]:
    bracket_regex = BracketRegex()
    qoute_regex = r"(\\*[\"'])((?:\\{2})*|(?:.*?[^\\](?:\\{2})*))\1"
    parse_regex = f'{qoute_regex}|{bracket_regex.match_bracket("{}", 3)}|{bracket_regex.match_bracket("()", 4)}|{bracket_regex.match_bracket("[]", 5)}|({split_item})'
    result = []
    i = 0
    for match in regex.finditer(parse_regex, string):
        match: re.Match
        item = bracket_regex.compile(match.groups())[5]
        if item is not None:
            position = match.start()
            content = string[i:position]
            if content != '':
                result.append(content.strip())
            i = match.end()
    content = string[i:]
    if content != '':
        result.append(content.strip())
    return result


def syntax_swap(string: str, swap_1: str, swap_2: str) -> str:
    """Swap swap_1 with swap_2 in string"""
    bracket_regex = BracketRegex()
    qoute_regex = r"(\\*[\"'])((?:\\{2})*|(?:.*?[^\\](?:\\{2})*))\1"
    parse_regex = f'{qoute_regex}|{bracket_regex.match_bracket("{}", 3)}|{bracket_regex.match_bracket("()", 4)}|{bracket_regex.match_bracket("[]", 5)}|({swap_1}|{swap_2})'

    def swap(match: re.Match):
        match: re.Match
        item = bracket_regex.compile(match.groups())[5]
        if item == swap_1:
            return swap_2
        elif item == swap_2:
            return swap_1

    return regex.sub(parse_regex, swap, string)


class Re:
    integer = r'([-+]?[0-9]+)'
    match_range = r'([-+]?[0-9]+)?..([-+]?[0-9]+)?'
    var = r'(\$[a-zA-Z0-9._]+)'
    var_nosigncap = r'\$([a-zA-Z0-9._]+)'
    operator_noequal = r'([+\-*\/%]=)'
    operator_equal = r'([+\-*\/%]?=)'
    function_call = r'(run |^)([\w\.]+)\(\)'
    condition_operator = r'(<|<=|=|>=|>)'
    start_cmd = r'(run |^)'
    start_var = r'((?:run |^)\$[a-zA-Z0-9._]+)'
