import argparse
import os
from collections import Counter

from bwt_fmindex_search.sa import *

# Using \0 instead of $ for terminal character because latter would not work with strings containing spaces
terminal_char = '\0'


def bw_transform(text, suffix_array):
    """ Returns BWT(text) """
    bw = []
    for si in suffix_array:
        if si == 0:
            bw.append(terminal_char)
        else:
            bw.append(text[si - 1])
    return ''.join(bw)  # return string-ized version of list bw


def count_characters(text):
    """ Returns a Counter object containing number of occurrences of each character in text """
    return Counter(text)


def calculate_ranks(text):
    """ Calculates rank of each character of input text """
    count = Counter()
    ranks = []
    for c in text:
        ranks.append(count[c])
        count[c] += 1
    return ranks


def terminate_string(s):
    """ Terminates the string with terminal_char if it is not terminated already.
     This character needs to be the smallest character in entire string. """
    return s if s[-1:] == terminal_char else s + terminal_char


class FColumn:
    def __init__(self, count, first_occurrence):
        self._count = count
        self._first_occurrence = first_occurrence

    def char_range(self, c):
        return self.get_first_occurrence(c), self.get_first_occurrence(c) + self._count[c]

    def get_first_occurrence(self, c):
        return self._first_occurrence.get(c, 0)


class FMIndex:
    def __init__(self, bwt, sa, ranks, f_column):
        self._bwt = bwt
        self._sa = sa
        self._ranks = ranks
        self._f_column = f_column

    def _find_preceders(self, c, start, end):
        first_index = self._bwt.find(c, start, end)
        if first_index == -1:
            return 0, 0
        else:
            return self._ranks[first_index], self._bwt.count(c, first_index, end)

    def query(self, pattern):
        reverse_pattern = pattern[::-1]
        start_index, end_index = self._f_column.char_range(reverse_pattern[0])
        for c in reverse_pattern[1:]:
            first_rank, count = self._find_preceders(c, start_index, end_index)
            if count == 0:
                return []
            else:
                start_index = self._f_column.get_first_occurrence(c) + first_rank
                end_index = start_index + count
        return self._sa[start_index:end_index]


def calculate_first_occurrences(counts):
    first_occurrences = {}
    s = 0
    for k, v in sorted(counts.items()):
        first_occurrences[k] = s
        s += v
    return first_occurrences


def create_f_column(text):
    count = count_characters(text)
    first_occurrence = calculate_first_occurrences(count)
    return FColumn(count, first_occurrence)


def create_fm_index(text):
    t = terminate_string(text)
    sa = suffix_array_manber_myers(t)
    bwt = bw_transform(t, sa)
    ranks = calculate_ranks(bwt)
    f_column = create_f_column(t)
    return FMIndex(bwt, sa, ranks, f_column)


if __name__ == "__main__":
    # create command line arguments parser
    parser = argparse.ArgumentParser(description='BWT + FM index for string search.')
    parser.add_argument("-t", "--text", required=True, help="Path to text file.")
    parser.add_argument("-p", "--patterns", required=True, help="Path to patterns file.")
    parser.add_argument("-r", "--results", required=False,
                        help="Path to output results file. If omitted, results will be printed to standard output.")
    args = vars(parser.parse_args())

    text_path = args["text"]
    patterns_path = args["patterns"]
    results_path = args["results"]

    # read input files
    if not os.path.isfile(text_path):
        print("File could not be found on path " + text_path)
    elif not os.path.isfile(patterns_path):
        print("File could not be found on path " + patterns_path)
    else:
        with open(text_path, 'r') as f:
            text = f.read()
        with open(patterns_path, 'r') as f:
            patterns = f.read().splitlines()

    # search for patterns
    fm_index = create_fm_index(text)
    results = [fm_index.query(pattern) for pattern in patterns]

    # write results
    if results_path:
        with open(results_path, 'w') as f:
            f.writelines("\n".join([" ".join(str(e) for e in result) for result in results]))
    else:
        print("\n".join([" ".join(str(e) for e in result) for result in results]))
