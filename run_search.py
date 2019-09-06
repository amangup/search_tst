import os

from search_lib.search_index import create_index
from search_lib.persist_index import *
from search_lib.search import search

def build_and_persist_index(maildir_root, tf_file, idf_file, trie_file, doc_locs_file, test=False):
    tf, idf, trie, doc_locations = create_index(maildir_root, test=test)
    persist_dict(tf, tf_file)
    persist_object(idf, idf_file)
    persist_object(trie, trie_file)
    persist_object(doc_locations, doc_locs_file)


def load_index(idf_file, trie_file, doc_locs_file):
    idf = parse_object(idf_file)
    trie = parse_object(trie_file)
    doc_locs = parse_object(doc_locs_file)

    return idf, trie, doc_locs


if __name__ == '__main__':
    dir = os.getcwd()

    tf_file = dir + '/tf.index'
    idf_file = dir + '/idf.index'
    trie_file = dir + '/trie.index'
    doc_locs_file = dir + '/doc_locs.index'

    build_and_persist_index("/home/aman/PycharmProjects/testa/maildir/",
                            tf_file,
                            idf_file,
                            trie_file,
                            doc_locs_file,
                            test=True)
    idf, trie, doc_locs = load_index(idf_file, trie_file, doc_locs_file)

    print("\n\n".join(search('add', "tf.index", idf, trie, doc_locs)))
