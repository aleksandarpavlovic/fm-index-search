import time

from fmindex_optimized import *
from util import *

sa_factors = [4, 16, 64, 256]
tally_factors = [8, 32, 128, 512]


def read_fasta_file(file):
    result = []
    for line in file:
        if line[0] != '>':
            result.append(line.rstrip().upper())
    result.append(terminal_char)
    return ''.join(result)


if __name__ == "__main__":
    # create command line arguments parser
    parser = argparse.ArgumentParser(description='BWT + FM index for string search.')
    parser.add_argument("-i", "--input", required=True, help="Path to text file.")
    parser.add_argument("-p", "--patterns", required=True, help="Path to patterns file.")
    parser.add_argument("-o", "--output", required=False, help="Path to output results file. If omitted, results will be printed to standard output.")
    args = vars(parser.parse_args())

    input_path = args["input"]
    patterns_path = args["patterns"]
    output_path = args["output"]

    with open(input_path, 'r') as input_file, open(patterns_path, 'r') as pattern_file:
        text = read_fasta_file(input_file)
        patterns = pattern_file.read().splitlines()
    sa = suffix_array_manber_myers(text)
    bwt = bw_transform(text, sa)
    bwt_size = get_size(bwt)
    f_column = create_f_column(text)
    f_column_size = get_size(f_column._zero_rank_indices) + get_size(f_column._counts)


    results = []
    for sa_factor in sa_factors:
        sa_sample = create_sa_sample(sa, sa_factor)
        sa_sample_size = get_size(sa_sample)
        for tally_factor in tally_factors:
            tally = create_tally(bwt, tally_factor)
            fm_index = FMIndex(bwt, sa_sample, tally, f_column)
            tally_size = get_size(tally.ranks)
            for pattern in patterns:
                start_time = time.process_time()
                query_count = fm_index.query(pattern)
                end_time = time.process_time()
                results.append((sa_factor, tally_factor, pattern, sa_sample_size, tally_size, sa_sample_size + tally_size + bwt_size + f_column_size, end_time - start_time))
    with open(output_path, 'w') as f:
        f.writelines("\n".join([" ".join(str(e) for e in result) for result in results]))



