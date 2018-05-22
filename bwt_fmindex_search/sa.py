from collections import defaultdict


def suffix_array_naive(text):
    """ Returns list of offsets in suffix array of text.
     Not efficient approach since n strings are created. Memory complexity is n^2.
     TODO come up with something more efficient """
    satups = sorted([(text[i:], i) for i in range(len(text))])
    # extract and return just the offsets
    return map(lambda x: x[1], satups)


def sort_bucket(str, bucket, bucket_level=0, keylen=6):
    d = defaultdict(list)
    for i in bucket:
        key = str[i+bucket_level : i+bucket_level+keylen]
        d[key].append(i)
    result = []
    for k,v in sorted(d.items()):
        if len(v) > 1:
            result += sort_bucket(str, v, bucket_level + keylen, keylen*2)
        elif v:
            result.append(v[0])
    return result


def suffix_array_manber_myers(str):
    """ Returns suffix array without having to create every suffix in the process.
    Much more memory efficient than naive implementation.
    Major drawback is recursion.
    TODO try to replace recursion with iterative approach. """
    return sort_bucket(str, (i for i in range(len(str))))


def is_smaller_equal(text, first, second):
    if first == second:
        return True
    offset = 0
    step = 20
    while True:
        s1 = text[first + offset: first + offset + step]
        s2 = text[second + offset: second + offset + step]
        if s1 < s2:
            return True
        elif s1 > s2:
            return False
        else:
            offset += step


# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot
def partition(arr, text, low, high):
    i = (low - 1)  # index of smaller element
    pivot = arr[high]  # pivot

    for j in range(low, high):

        # If current element is smaller than or
        # equal to pivot
        if is_smaller_equal(text, arr[j], pivot):
            # increment index of smaller element
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]

    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


# The main function that implements QuickSort
# arr[] --> Array to be sorted,
# low  --> Starting index,
# high  --> Ending index

# Function to do Quick sort
def quick_sort(arr, text, low, high):
    if low < high:
        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(arr, text, low, high)

        # Separately sort elements before
        # partition and after partition
        quick_sort(arr, text, low, pi - 1)
        quick_sort(arr, text, pi + 1, high)


def suffix_array_quicksort(text):
    sa = list(range(len(text)))
    quick_sort(sa, text, 0, len(text) - 1)
    return sa


if __name__ == "__main__":
    text = "bananananananananananananananananananananananananan$"
    print(suffix_array_quicksort(text))
    print(list(suffix_array_naive(text)))
    print(suffix_array_manber_myers(text))