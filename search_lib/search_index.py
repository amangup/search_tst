import glob
import math
import os

from search_lib.trie import TrieNode
from search_lib.parse_email import parse_email


def create_index(root_path, test=False):
    docs = []
    tf = {}
    doc_locations = {}

    doc_count = 0

    for file in glob.glob(root_path + "/**", recursive=True):
        if os.path.isfile(file):
            doc_count += 1
            if test and doc_count > 5000:
                break

            metadata, content_words, _ = parse_email(file)
            if not metadata:
                continue

            docs.append(content_words)
            doc_locations[metadata['Message-ID']] = file

            tf[metadata['Message-ID']] = word_count(content_words)

    idf, trie = get_idf_and_trie(docs)

    return tf, idf, trie, doc_locations


def word_count(word_list):
    counts = {}
    for word in word_list:
        counts[word] = counts.get(word, 0) + 1

    return counts


def update_word_count(sentence, current_counts):
    new_counts = word_count(sentence)
    for word, _ in new_counts.items():
        current_counts[word] = current_counts.get(word, 0) + 1


def get_idf_and_trie(documents):
    word_counts = {}
    for doc in documents:
        update_word_count(doc, word_counts)
    idf = {}

    trie = TrieNode('*')

    N = len(documents)
    for word, count in word_counts.items():
        idf[word] = math.log(N / count)
        trie.add(word)

    return idf, trie


if __name__ == '__main__':
    tf, idf, _, _ = create_index("/home/aman/PycharmProjects/testa/maildir/", test=True)
    print(len(tf))
    print(len(idf))
