from collections import Counter
from bwt_fmindex_search.sa import *
import os
import argparse

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

def query(bwt, counts, ranks, suffix_array, pattern):
    reverse_pattern = pattern[::-1]
    start_index, end_index = char_range(counts, reverse_pattern[0])
    for c in reverse_pattern[1:]:
        first_rank, count = find_preceders(bwt[start_index : end_index], ranks[start_index : end_index], c)
        if count == 0:
            return []
        else:
            start_index = first_occurrence(counts, c) + first_rank
            end_index = start_index + count
    return suffix_array[start_index:end_index]

def find_preceders(bwt, ranks, c):
    first_index = bwt.find(c)
    if (first_index == -1):
        return 0,0
    else:
        return ranks[first_index], bwt.count(c, first_index)

def char_range(counts, char):
    """ Returns range of indices in F array inside which char is contained.
     The range is in form [start, end) i.e. does not include end index """
    start_index = first_occurrence(counts, char)
    return (start_index, start_index + counts[char])

def first_occurrence(counts, char):
    return sum (count[1] for count in counts.items() if count[0] < char)


class FMIndex:
    def __init__(self, text):
        self.text = terminate_string(text)
        self.char_count = count_characters(self.text)
        self.suffix_array = suffix_array_manber_myers(self.text)
        self.bwt = bw_transform(self.text, self.suffix_array)
        self.ranks = calculate_ranks(self.bwt)

    def query(self, pattern):
        return query(self.bwt, self.char_count, self.ranks, self.suffix_array, pattern)

if __name__ == "__main__":
    # create command line arguments parser
    parser = argparse.ArgumentParser(description='BWT + FM index for string search.')
    parser.add_argument("-t", "--text", required=True, help="Path to text file.")
    parser.add_argument("-p", "--patterns", required=True, help="Path to patterns file.")
    parser.add_argument("-r", "--results", required=False, help="Path to output results file. If omitted, results will be printed to standard output.")
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
    fm_index = FMIndex(text)
    results = [fm_index.query(pattern) for pattern in patterns]

    # write results
    if results_path:
        with open(results_path, 'w') as f:
            f.writelines("\n".join([" ".join(str(e) for e in result) for result in results]))
    else:
        print("\n".join([" ".join(str(e) for e in result) for result in results]))
