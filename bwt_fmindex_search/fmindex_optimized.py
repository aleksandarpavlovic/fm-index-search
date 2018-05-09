from collections import Counter
from bwt_fmindex_search.sa import *
import os
import argparse

# Using \0 instead of $ for terminal character because latter would not work with strings containing spaces
terminal_char = '\0'


def bw_transform(text, sa):
    """ Returns BWT(text) """
    bw = []
    for si in sa.array:
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


def query(bwt, f_column, tally, suffix_array, pattern):
    reverse_pattern = pattern[::-1]
    start_index, end_index = f_column.char_range(reverse_pattern[0])
    if start_index == end_index:
        return []
    for c in reverse_pattern[1:]:
        first_rank, count = find_preceders(bwt, start_index, end_index, tally, c)
        if count == 0:
            return []
        else:
            start_index = f_column.first_occurrence(c) + first_rank
            end_index = start_index + count
    return [find_suffix(suffix_array, bwt, tally, f_column, i) for i in range(start_index, end_index)]


def find_suffix(sa, bwt, tally, f_column, index):
    if index % sa.factor == 0:
        return sa.array[index // sa.factor]
    else:
        rank = find_tally(bwt, index, tally, bwt[index]) - 1
        return 1 + find_suffix(sa, bwt, tally, f_column.first_occurrence(bwt[index]) + rank)


def find_preceders(bwt, start_index, end_index, tally, c):
    first_tally = find_tally(bwt, start_index - 1, tally, c)
    last_tally = find_tally(bwt, end_index - 1, tally, c)

    return first_tally, last_tally - first_tally


def find_tally(bwt, index, tally, c):
    if not tally.ranks[c]:
        return -1
    if index % tally.factor == 0:
        return tally.ranks[c][index // tally.factor]
    else:
        count_back = index % tally.factor <= tally.factor // 2
        sub_bwt = bwt[round_down(index, tally.factor) + 1: index + 1] if count_back else bwt[index: round_up(index,
                                                                                                             tally.factor)]
        if count_back:
            return tally.ranks[c][index // tally.factor] + sub_bwt.count(c)
        else:
            return tally.ranks[c][index // tally.factor + 1] - sub_bwt.count(c)


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
    return tally


def positive_int(value):
    ivalue = int(value)
    if ivalue <= 0:
        raise argparse.ArgumentTypeError("%s is an invalid positive int value" % value)
    return ivalue


class Tally:
    def __init__(self, bwt, factor):
        self.factor = factor
        self.ranks = create_ranks_tally(bwt, factor)


class SuffixArray:
    def __init__(self, text, factor):
        self.factor = factor
        self.array = suffix_array_manber_myers(text)[::factor]

class FColumn:
    def __init__(self, text):
        self.counts = count_characters(text)
        self.zero_rank_indices = calculate_first_occurrences(self.counts)

    def char_range(self, c):
        return self.first_occurrence(c), self.first_occurrence(c) + self.counts[c]

    def first_occurrence(self, c):
        return self.zero_rank_indices.get(c, 0)


class FMIndex:
    def __init__(self, text, sa_factor=1, tally_factor=1):
        text_terminated = terminate_string(text)
        self.f_column = FColumn(text_terminated)
        self.suffix_array = SuffixArray(text_terminated, sa_factor)
        self.bwt = bw_transform(text_terminated, self.suffix_array)
        self.tally = Tally(self.bwt, tally_factor)

    def query(self, pattern):
        return query(self.bwt, self.f_column, self.tally, self.suffix_array, pattern)


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
    fm_index = FMIndex(text)
    results = [fm_index.query(pattern) for pattern in patterns]

    # write results
    if results_path:
        with open(results_path, 'w') as f:
            f.writelines("\n".join([" ".join(str(e) for e in result) for result in results]))
    else:
        print("\n".join([" ".join(str(e) for e in result) for result in results]))