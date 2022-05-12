"""
    Term Frequency
    menghitung frequency dari kata
"""


def term_frequency(tokens, bow):
    word_dict = {}
    for word in tokens:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    tf_dict = {}
    for word, count in word_dict.items():
        tf_dict[word] = count / len(bow)
    return tf_dict


if __name__ == '__main__':
    import preprocessing.__index

    preprocessed, _ = preprocessing.__index.preprocessing("Saya menyukai cabai")
    print(term_frequency(preprocessed, ['suka', 'cabai']))
