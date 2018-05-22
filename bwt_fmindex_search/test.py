from bwt_fmindex_search.fmindex import *

# Test suffix array functions

# Naive algorithm tests
text_normal_1 = "abracadabra"
text_normal_2 = "banana"
text_repetitive = "nanananananinininenene"
text_empty = ""
text_with_num = "aaba4bba2"
text_with_blancs = "This is a text"


def error_message_builder(function, reason):
    return "Assertion Error: " + function + " failed on: " + reason + "!"


assert set(suffix_array_naive(text_normal_1)) == set([10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]), \
    error_message_builder("suffix_array_naive", "text_normal_1")

assert set(suffix_array_naive(text_normal_2)) == set([5, 3, 1, 0, 4, 2]), \
    error_message_builder("suffix_array_naive", "text_normal_2")

assert set(suffix_array_naive(text_repetitive)) == set([1, 3, 5, 7, 9, 21, 19, 17, 15, 13, 11, 0, 2, 4, 6, 8, 20,
                                                 18, 16, 14, 12, 10]), \
    error_message_builder("suffix_array_naive", "text_repetitive")

assert set(suffix_array_naive(text_empty)) == set([]), error_message_builder("suffix_array_naive", "text_empty")
assert set(suffix_array_naive(text_with_num)) == set([8, 4, 7, 3, 0, 1, 6, 2, 5]), \
    error_message_builder("suffix_array_naive", "text_empty")

assert set(suffix_array_naive(text_with_blancs)) == set([7, 4, 9, 0, 8, 11, 1, 5, 2, 6, 3, 13, 10, 12]), \
    error_message_builder("suffix_array_naive", "text_with_blancs")

# Suffix_array_manber_myers tests
assert (suffix_array_manber_myers(text_normal_1)) == [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2], \
    error_message_builder("suffix_array_manber_myers", "text_normal_1")

assert (suffix_array_manber_myers(text_normal_2)) == [5, 3, 1, 0, 4, 2], \
    error_message_builder("suffix_array_manber_myers", "text_normal_2")

assert (suffix_array_manber_myers(text_repetitive)) == [1, 3, 5, 7, 9, 21, 19, 17, 15, 13, 11, 0, 2, 4, 6, 8, 20, 18,
                                                        16, 14, 12, 10], \
    error_message_builder("suffix_array_manber_myers", "text_normal_repetitive")

assert (suffix_array_manber_myers(text_empty)) == [], error_message_builder("suffix_array_manber_myers", "text_empty")

assert (suffix_array_manber_myers(text_with_num)) == [8, 4, 7, 3, 0, 1, 6, 2, 5], \
    error_message_builder("suffix_array_manber_myers", "text_with_num")

assert (suffix_array_manber_myers(text_with_blancs)) == [7, 4, 9, 0, 8, 11, 1, 5, 2, 6, 3, 13, 10, 12], \
    error_message_builder("suffix_array_manber_myers", "text_with_blancs")


# Test bucket sort
assert(sort_bucket(text_normal_1, (i for i in range(len(text_normal_1))))) == [10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2]
assert(sort_bucket(text_empty, (i for i in range(len(text_empty))))) == []
assert(sort_bucket(text_repetitive, (i for i in range(len(text_repetitive)-3)), 2, 4)) == [1, 3, 5, 7, 17, 15, 13,
                                                                                           11, 9, 0, 2, 4, 6, 18, 16,
                                                                                           14, 12, 10, 8]

# Test BWT
text_normal_1_terminal = "abracadabra"+'\0'
text_normal_2_terminal = "banana"+'\0'
text_repetitive_terminal = "nanananananinininenene"+'\0'
text_empty_terminal = '\0'
text_num_terminal = "aaba4bba2"+'\0'
text_blancs_terminal = "This is a text"+'\0'

suffix_array_normal_1 = suffix_array_manber_myers(text_normal_1_terminal)
suffix_array_normal_2 = suffix_array_manber_myers(text_normal_2_terminal)
suffix_array_repetitive = suffix_array_manber_myers(text_repetitive_terminal)
suffix_array_empty = suffix_array_manber_myers(text_empty_terminal)
suffix_array_num = suffix_array_manber_myers(text_num_terminal)
suffix_array_blancs = suffix_array_manber_myers(text_blancs_terminal)

assert (bw_transform(text_normal_1_terminal, suffix_array_normal_1)) == "ard"+'\0'"rcaaaabb", \
    error_message_builder("bw_transform", "text_normal_1_terminal")
assert (bw_transform(text_normal_2_terminal, suffix_array_normal_2)) == "annb"+'\0'"aa", \
    error_message_builder("bw_transform", "text_normal_2_terminal")
assert (bw_transform(text_repetitive_terminal, suffix_array_repetitive)) == "ennnnnnnnnnn"+'\0'"aaaaeeiiia", \
    error_message_builder("bw_transform", "text_repetitive_terminal")
assert (bw_transform(text_empty_terminal, suffix_array_empty)) == '\0', \
    error_message_builder("bw_transform", "text_empty_terminal")
assert (bw_transform(text_num_terminal, suffix_array_num)) == "2aabb"+'\0'"aba4", \
    error_message_builder("bw_transform", "text_num_terminal")
assert (bw_transform(text_blancs_terminal, suffix_array_blancs)) == "tssa" + '\0' + " tT hiix e", \
    error_message_builder("bw_transform", "text_blancs_terminal")

# TEST HELPER FUNCTIONS
# count characters
assert(count_characters(text_normal_1)) == (Counter({'a': 5, 'b': 2, 'c': 1, 'd': 1, 'r': 2})), \
    error_message_builder("count_characters", "text_normal_1")
assert(count_characters(text_empty)) == Counter(), error_message_builder("count_characters", "text_empty")
assert(count_characters(text_with_blancs)) == (Counter({' ': 3, 'i': 2, 's': 2, 't': 2, 'a': 1, 'e': 1,
                                                        'h': 1, 'T': 1, 'x': 1})), \
    error_message_builder("count_characters", "text_with_blancs")

# terminate string
assert(terminate_string(text_normal_1)) == "abracadabra"+'\0', \
    error_message_builder("terminate_string", "text_normal_1")
assert(terminate_string(text_with_blancs)) == "This is a text"+'\0', \
    error_message_builder("terminate_string", "text_with_blancs")
assert(terminate_string(text_empty)) == '\0', error_message_builder("terminate_string", "text_empty")
assert(terminate_string(text_num_terminal)) == "aaba4bba2"+'\0', \
    error_message_builder("terminate_string", "text_num_terminal")

# calculate ranks
assert (calculate_ranks(text_normal_1)) == [0, 0, 0, 1, 0, 2, 0, 3, 1, 1, 4], \
    error_message_builder("calculate_ranks", "text_normal_1")
assert (calculate_ranks(text_normal_1_terminal)) == [0, 0, 0, 1, 0, 2, 0, 3, 1, 1, 4, 0], \
    error_message_builder("calculate_ranks", "text_normal_1_terminal")
assert (calculate_ranks(text_normal_2)) == [0, 0, 0, 1, 1, 2], error_message_builder("calculate_ranks", "text_normal_2")
assert (calculate_ranks(text_normal_2_terminal)) == [0, 0, 0, 1, 1, 2, 0], \
    error_message_builder("calculate_ranks", "text_normal_2_terminal")
assert (calculate_ranks(text_empty)) == [], error_message_builder("calculate_ranks", "text_empty")
assert (calculate_ranks(text_empty_terminal)) == [0], error_message_builder("calculate_ranks", "text_empty_terminal")
assert (calculate_ranks(text_repetitive)) == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 0, 6, 1, 7, 2, 8, 0, 9, 1, 10, 2], \
    error_message_builder("calculate_ranks", "text_repetitive")
assert (calculate_ranks(text_repetitive_terminal)) == [0, 0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 0, 6, 1, 7, 2, 8, 0, 9, 1, 10,
                                                      2, 0], \
    error_message_builder("calculate_ranks", "text_repetitive_terminal")
assert (calculate_ranks(text_with_blancs)) == [0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 0, 0, 0, 1], \
    error_message_builder("calculate_ranks", "text_with_blancs")
assert (calculate_ranks(text_blancs_terminal)) == [0, 0, 0, 0, 0, 1, 1, 1, 0, 2, 0, 0, 0, 1, 0], \
    error_message_builder("calculate_ranks", "text_blancs_terminal")
assert (calculate_ranks(text_num_terminal)) == [0, 1, 0, 2, 0, 1, 2, 3, 0, 0],\
    error_message_builder("calculate_ranks", "text_num_terminal")

#FM testing
count_normal_text_1 = count_characters(text_normal_1_terminal)
count_normal_text_2 = count_characters(text_normal_2_terminal)
count_text_num = count_characters(text_num_terminal)
count_text_empty = count_characters(text_empty_terminal)
count_text_repetitive = count_characters(text_repetitive_terminal)
count_text_blancs = count_characters(text_blancs_terminal)
count_empty = count_characters(text_empty)

assert(calculate_first_occurrences(count_normal_text_1)) == {'\0': 0, 'a': 1, 'b': 6, 'c': 8, 'd': 9, 'r': 10}, \
    error_message_builder("calculate_first_occurrences", "text_normal_1_terminal")
assert(calculate_first_occurrences(count_normal_text_2)) == {'\0': 0, 'a': 1, 'b': 4, 'n': 5}, \
    error_message_builder("calculate_first_occurrences", "text_normal_2_terminal")
assert(calculate_first_occurrences(count_text_num)) == {'\0': 0, '2': 1, '4': 2, 'a': 3, 'b': 7}, \
    error_message_builder("calculate_first_occurrences", "text_with_num_terminal")
assert(calculate_first_occurrences(count_text_empty)) == {'\0': 0},\
    error_message_builder("calculate_first_occurrences", "text_empty_terminal")
assert(calculate_first_occurrences(count_text_repetitive)) == {'\0': 0, 'a': 1, 'e': 6, 'i': 9, 'n': 12}, \
    error_message_builder("calculate_first_occurrences", "text_repetitive_terminal")
assert(calculate_first_occurrences(count_text_blancs)) == {'\0': 0, ' ': 1, 'T': 4, 'a': 5, 'e': 6, 'h': 7, 'i': 8,
                                                           's': 10, 't': 12, 'x': 14}, \
    error_message_builder("calculate_first_occurrences", "text_with_blancs_terminal")
assert(calculate_first_occurrences(count_empty)) == {}, \
    error_message_builder("calculate_first_occurrences", "count_empty")

#Test f_column creation
f_column_text_normal_1 = create_f_column(text_normal_1_terminal)
f_column_text_normal_2 = create_f_column(text_normal_2_terminal)
f_column_text_num = create_f_column(text_num_terminal)
f_column_text_empty = create_f_column(text_empty_terminal)
f_column_text_repetitive = create_f_column(text_repetitive_terminal)
f_column_text_blancs = create_f_column(text_blancs_terminal)


def f_column_equality_check(f_column_org, counter, first_occurrence):
    result = (f_column_org._count == counter) and (f_column_org._first_occurrence == first_occurrence)
    return result


assert f_column_equality_check(f_column_text_normal_1, Counter({'\0': 1, 'a': 5, 'b': 2, 'c': 1, 'd': 1, 'r': 2}),
                               {'\0': 0, 'a': 1, 'b': 6, 'c': 8, 'd': 9, 'r': 10}), \
    error_message_builder("f_column_equality_check", "text_normal_1")

assert f_column_equality_check(f_column_text_normal_2, Counter({'\0': 1, 'a': 3, 'b': 1, 'n': 2}),
                               {'\0': 0, 'a': 1, 'b': 4, 'n': 5}), \
    error_message_builder("f_column_equality_check", "text_normal_2")

assert f_column_equality_check(f_column_text_num, Counter({'\0': 1, '2': 1, '4': 1, 'a': 4, 'b': 3}),
                               {'\0': 0, '2': 1, '4': 2, 'a': 3, 'b': 7}), \
    error_message_builder("f_column_equality_check", "text_with_num")

assert f_column_equality_check(f_column_text_empty, Counter({'\0': 1}), {'\0': 0}), \
    error_message_builder("f_column_equality_check", "text_empty")

assert f_column_equality_check(f_column_text_repetitive, Counter({'\0': 1, 'a': 5, 'e': 3, 'i': 3, 'n': 11}),
                               {'\0': 0, 'a': 1, 'e': 6, 'i': 9, 'n': 12}), \
    error_message_builder("f_column_equality_check", "text_repetitive")

assert f_column_equality_check(f_column_text_blancs, Counter({'\0': 1, ' ': 3, 'i': 2, 's': 2, 't': 2, 'a': 1, 'e': 1,
                                                             'h': 1, 'T': 1, 'x': 1}),
                               {'\0': 0, ' ': 1, 'T': 4, 'a': 5, 'e': 6, 'h': 7, 'i': 8, 's': 10, 't': 12, 'x': 14}), \
    error_message_builder("f_column_equality_check", "text_with_blancs")

#Test FColumn.get_first_occurence
assert f_column_text_normal_1.get_first_occurrence('a') == 1, \
    error_message_builder("get_first_occurrence", "text_normal_1")
assert f_column_text_num.get_first_occurrence('4') == 2, error_message_builder("get_first_occurrence", "text_with_num")
assert f_column_text_empty.get_first_occurrence('\0') == 0, error_message_builder("get_first_occurrence", "text_empty")
assert f_column_text_repetitive.get_first_occurrence('u') == 0 #ako je karakter nepostojeci, da li je ok da vraca  0???
assert f_column_text_blancs.get_first_occurrence(' ') == 1, \
    error_message_builder("get_first_occurrence", "text_with_blancs")

#Test FColumn.char_range
assert f_column_text_normal_1.char_range('r') == (10, 12), error_message_builder("char_range", "text_normal_1")
assert f_column_text_normal_2.char_range('b') == (4, 5), error_message_builder("char_range", "text_normal_2")
assert f_column_text_empty.char_range('a') == (0, 0), error_message_builder("char_range", "text_empty")
assert f_column_text_repetitive.char_range('n') == (12, 23), error_message_builder("char_range", "text_repetitive")
assert f_column_text_repetitive.char_range('e') == (6, 9), error_message_builder("char_range", "text_repetitive")
assert f_column_text_blancs.char_range('T') == (4, 5), error_message_builder("char_range", "text_with_blancs")
assert f_column_text_blancs.char_range(' ') == (1, 4), error_message_builder("char_range", "text_with_blancs")
assert f_column_text_blancs.char_range('\0') == (0, 1), error_message_builder("char_range", "text_with_blancs")

#Test create_fm_index
fm_index_1 = create_fm_index(text_normal_1)
fm_index_2 = create_fm_index(text_normal_2)
fm_index_repetitive = create_fm_index(text_repetitive)
fm_index_empty = create_fm_index(text_empty)
fm_index_num = create_fm_index(text_with_num)
fm_index_blancs = create_fm_index(text_with_blancs)

def fm_index_equality_check(fm_index_org, bwt_test, sa_test, ranks_test, f_column_counter, f_column_first_occurrence):
    return (fm_index_org._bwt == bwt_test) and (fm_index_org._sa == sa_test) and (fm_index_org._ranks == ranks_test) \
           and f_column_equality_check(fm_index_org._f_column, f_column_counter, f_column_first_occurrence)


assert fm_index_equality_check(fm_index_1, "ard"+'\0'"rcaaaabb", [11, 10, 7, 0, 3, 5, 8, 1, 4, 6, 9, 2],
                               [0, 0, 0, 0, 1, 0, 1, 2, 3, 4, 0, 1],
                               Counter({'\0': 1, 'a': 5, 'b': 2, 'c': 1, 'd': 1, 'r': 2}),
                               {'\0': 0, 'a': 1, 'b': 6, 'c': 8, 'd': 9, 'r': 10}), \
    error_message_builder("fm_index_equality_check", "text_normal_1")

assert fm_index_equality_check(fm_index_2, "annb"+'\0'"aa", [6, 5, 3, 1, 0, 4, 2], [0, 0, 1, 0, 0, 1, 2],
                               Counter({'\0': 1, 'a': 3, 'b': 1, 'n': 2}), {'\0': 0, 'a': 1, 'b': 4, 'n': 5}), \
    error_message_builder("fm_index_equality_check", "text_normal_2")

assert fm_index_equality_check(fm_index_repetitive, "ennnnnnnnnnn"+'\0'"aaaaeeiiia",
                               [22, 1, 3, 5, 7, 9, 21, 19, 17, 15, 13, 11, 0, 2, 4, 6, 8, 20, 18, 16, 14, 12, 10],
                               [0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 0, 0, 1, 2, 3, 1, 2, 0, 1, 2, 4],
                               Counter({'\0': 1, 'a': 5, 'e': 3, 'i': 3, 'n': 11}),
                               {'\0': 0, 'a': 1, 'e': 6, 'i': 9, 'n': 12}), \
    error_message_builder("fm_index_equality_check", "text_repetitive")

assert fm_index_equality_check(fm_index_empty, '\0', [0], [0], Counter({'\0': 1}), {'\0': 0}), \
    error_message_builder("fm_index_equality_check", "text_empty")

assert fm_index_equality_check(fm_index_num, "2aabb"+'\0'"aba4", [9, 8, 4, 7, 3, 0, 1, 6, 2, 5],
                               [0, 0, 1, 0, 1, 0, 2, 2, 3, 0],
                               Counter({'\0': 1, '2': 1, '4': 1, 'a': 4, 'b': 3}),
                               {'\0': 0, '2': 1, '4': 2, 'a': 3, 'b': 7}), \
    error_message_builder("fm_index_equality_check", "text_with_num")

assert fm_index_equality_check(fm_index_blancs, "tssa" + '\0' + " tT hiix e",
                               [14, 7, 4, 9, 0, 8, 11, 1, 5, 2, 6, 3, 13, 10, 12],
                               [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 2, 0],
                               Counter({'\0': 1, ' ': 3, 'i': 2, 's': 2, 't': 2,
                                        'a': 1, 'e': 1, 'h': 1, 'T': 1, 'x': 1}),
                               {'\0': 0, ' ': 1, 'T': 4, 'a': 5, 'e': 6, 'h': 7, 'i': 8, 's': 10, 't': 12, 'x': 14}), \
    error_message_builder("fm_index_equality_check", "text_with_blancs")


assert fm_index_1._find_preceders('b', 0, 11) == (0, 1)
assert fm_index_1._find_preceders('b', 0, 12) == (0, 2)
assert fm_index_1._find_preceders('a', 0, 0) == (0, 0)
assert fm_index_1._find_preceders('a', 0, 8) == (0, 3)
assert fm_index_1._find_preceders('a', 3, 8) == (1, 2)
assert fm_index_1._find_preceders('a', 7, 8) == (2, 1)
assert fm_index_1._find_preceders('a', 7, 7) == (0, 0)
assert fm_index_2._find_preceders('k', 0, 5) == (0, 0)
assert fm_index_repetitive._find_preceders('n', 4, 8) == (3, 4)
assert fm_index_blancs._find_preceders("T", 1, 8) == (0, 1)

#QUERY TEST

text_for_querying = "Abyssus abyssum invocat. Cave ab homine unius libri"

pattern_should_exist_1 = "Abyssus abyssum"
pattern_should_exist_2 = "us libri"
pattern_should_exist_3 = "invocat. Cave"
pattern_should_exist_4 = 'm'
pattern_empty = ""
pattern_should_not_exist_1 = "Abyssusium"
pattern_should_not_exist_2 = "usa libri"
pattern_should_not_exist_3 = "ab  "

query_fm_index = create_fm_index(text_for_querying)

assert (query_fm_index.query(pattern_should_exist_1)) == [0], error_message_builder("query", "pattern_should_exist_1")
assert (query_fm_index.query(pattern_should_exist_2)) == [43], error_message_builder("query", "pattern_should_exist_2")
assert (query_fm_index.query(pattern_should_exist_3)) == [16], error_message_builder("query", "pattern_should_exist_3")
assert (query_fm_index.query(pattern_should_exist_4)) == [14, 35], \
    error_message_builder("query", "pattern_should_exist_4")
assert (query_fm_index.query(pattern_should_not_exist_1)) == [], \
    error_message_builder("query", "pattern_should_not_exist_1")
assert (query_fm_index.query(pattern_should_not_exist_2)) == [], \
    error_message_builder("query", "pattern_should_not_exist_2")
assert (query_fm_index.query(pattern_should_not_exist_3)) == [], \
    error_message_builder("query", "pattern_should_not_exist_3")
assert (query_fm_index.query(pattern_empty)) == [], "should return empty array"

