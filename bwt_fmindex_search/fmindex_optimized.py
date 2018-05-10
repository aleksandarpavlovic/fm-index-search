import argparse
import os
from collections import Counter

from bwt_fmindex_search.sa import *

# Using \0 instead of $ for terminal character because latter would not work with strings containing spaces
terminal_char = '\0'


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


def bw_transform(text, sa):
    """ Returns BWT(text) """
    bw = []
    for si in sa:
        if si == 0:
            bw.append(terminal_char)
        else:
            bw.append(text[si - 1])
    return ''.join(bw)  # return string-ized version of list bw


def count_characters(text):
    """ Returns a Counter object containing number of occurrences of each character in text """
    return Counter(text)


def terminate_string(s):
    """ Terminates the string with terminal_char if it is not terminated already.
     This character needs to be the smallest character in entire string. """
    return s if s[-1:] == terminal_char else s + terminal_char


def round_down(n, base):
    return n // base * base


def round_up(n, base):
    return (n + base - 1) // base * base


def calculate_first_occurrences(counts):
    first_occurrences = {}
    s = 0
    for k, v in sorted(counts.items()):
        first_occurrences[k] = s
        s += v
    return first_occurrences


class Tally:
    def __init__(self, ranks, factor):
        self.ranks = ranks
        self.factor = factor


class FColumn:
    def __init__(self, counts, zero_rank_indices):
        self._counts = counts
        self._zero_rank_indices = zero_rank_indices

    def char_range(self, c):
        return self.first_occurrence(c), self.first_occurrence(c) + self._counts[c]

    def first_occurrence(self, c):
        return self._zero_rank_indices.get(c, 0)


class FMIndex:
    def __init__(self, bwt, sa_sample, tally, f_column):
        self._bwt = bwt
        self._sa_sample = sa_sample
        self._tally = tally
        self._f_column = f_column

    def query(self, pattern):
        reverse_pattern = pattern[::-1]
        start_index, end_index = self._f_column.char_range(reverse_pattern[0])
        if start_index == end_index:
            return []
        for c in reverse_pattern[1:]:
            first_rank, count = self._find_preceders(start_index, end_index, c)
            if count == 0:
                return []
            else:
                start_index = self._f_column.first_occurrence(c) + first_rank
                end_index = start_index + count
        return [self._find_suffix(i) for i in range(start_index, end_index)]

    def _find_preceders(self, start_index, end_index, c):
        first_tally = self._find_tally(start_index - 1, c)
        last_tally = self._find_tally(end_index - 1, c)
        return first_tally, last_tally - first_tally

    def _find_tally(self, index, c):
        if not self._tally.ranks[c]:
            return -1
        if index % self._tally.factor == 0:
            return self._tally.ranks[c][index // self._tally.factor]
        else:
            count_back = index % self._tally.factor <= self._tally.factor // 2
            sub_bwt = self._bwt[round_down(index, self._tally.factor) + 1: index + 1] if count_back else self._bwt[index + 1: min(len(self._bwt), round_up(index, self._tally.factor) + 1)]
            if count_back:
                return self._tally.ranks[c][index // self._tally.factor] + sub_bwt.count(c)
            else:
                return self._tally.ranks[c][index // self._tally.factor + 1] - sub_bwt.count(c)

    def _find_suffix(self, index):
        suffix = self._sa_sample.get(index, None)
        if suffix is not None:
            return suffix
        else:
            rank = self._find_tally(index, self._bwt[index]) - 1
            return 1 + self._find_suffix(self._f_column.first_occurrence(self._bwt[index]) + rank)


def create_ranks_tally(bwt, tally_factor):
    """ Creates tally matrix containing only every tally_factor-th rank of a character"""
    count = Counter()
    tally = defaultdict(list)
    for i in range(0, len(bwt)):
        c = bwt[i]
        count[c] += 1
        if i % tally_factor == 0:
            for k, v in count.items():
                if not tally[k]:
                    tally[k].extend([0] * (i // tally_factor))
                tally[k].append(v)
    # for search simplicity add additional tally row
    for k, v in count.items():
        if not tally[k]:
            tally[k].extend([0] * ((len(bwt) - 1) // tally_factor + 1))
        tally[k].append(v)
    return tally


def create_sa_sample(sa, factor):
    sample = {}
    for i in range(len(sa)):
        if sa[i] % factor == 0:
            sample[i] = sa[i]
    return sample


def create_f_column(text):
    count = count_characters(text)
    first_occurrence = calculate_first_occurrences(count)
    return FColumn(count, first_occurrence)


def create_tally(bwt, tally_factor):
    return Tally(create_ranks_tally(bwt, tally_factor), tally_factor)


def create_fm_index(text, sa_factor, tally_factor):
    t = terminate_string(text)
    sa = suffix_array_manber_myers(t)
    sa_sample = create_sa_sample(sa, sa_factor)
    bwt = bw_transform(t, sa)
    tally = create_tally(bwt, tally_factor)
    f_column = create_f_column(t)
    return FMIndex(bwt, sa_sample, tally, f_column)


if __name__ == "__main__":
    # create command line arguments parser
    parser = argparse.ArgumentParser(description='BWT + FM index for string search.')
    parser.add_argument("-t", "--text", required=True, help="Path to text file.")
    parser.add_argument("-p", "--patterns", required=True, help="Path to patterns file.")
    parser.add_argument("-r", "--results", required=False,
                        help="Path to output results file. If omitted, results will be printed to standard output.")
    parser.add_argument("--sa_factor", type=positive_int, default=1, required=False,
                        help="Suffix array factor. Defines compression level of suffix array. If omitted, full size suffix array will be used.")
    parser.add_argument("--tally_factor", type=positive_int, default=1, required=False,
                        help="Ranks tally matrix factor. Defines compression level of tally matrix. If omitted, full size tally will be used.")
    args = vars(parser.parse_args())

    text_path = args["text"]
    patterns_path = args["patterns"]
    results_path = args["results"]
    sa_factor = args["sa_factor"]
    tally_factor = args["tally_factor"]

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
    fm_index = create_fm_index(text, sa_factor, tally_factor)
    results = [fm_index.query(pattern) for pattern in patterns]

    # write results
    if results_path:
        with open(results_path, 'w') as f:
            f.writelines("\n".join([" ".join(str(e) for e in result) for result in results]))
    else:
        print("\n".join([" ".join(str(e) for e in result) for result in results]))