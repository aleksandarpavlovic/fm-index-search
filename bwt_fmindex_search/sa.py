from collections import defaultdict

def suffix_array_naive(text):
    """ Returns list of offsets in suffix array of text.
     Not efficient approach since n strings are created. Memory complexity is n^2.
     TODO come up with something more efficient """
    satups = sorted([(text[i:], i) for i in range(len(text))])
    # extract and return just the offsets
    return map(lambda x: x[1], satups)

def sort_bucket(str, bucket, bucket_level=0, keylen=2):
    d = defaultdict(list)
    for i in bucket:
        key = str[i+bucket_level : i+bucket_level+keylen]
        d[key].append(i)
    result = []
    for k,v in sorted(d.items()):
        if len(v) > 1:
            result += sort_bucket(str, v, bucket_level + keylen, keylen*2)
        else:
            result.append(v[0])
    return result

def suffix_array_manber_myers(str):
    """ Returns suffix array without having to create every suffix in the process.
    Much more memory efficient than naive implementation.
    Major drawback is recursion.
    TODO try to replace recursion with iterative approach. """
    return sort_bucket(str, (i for i in range(len(str))))

if __name__ == "__main__":
    text = "bananananananananananananananananananananananananan$"
    print(list(suffix_array_naive(text)))
    print(suffix_array_manber_myers(text))