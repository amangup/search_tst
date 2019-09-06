import pickle
import re

from search_lib.parse_email import parse_email
from search_lib.persist_index import persist_dict
from search_lib.search_index import create_index
from search_lib.trie import find_words_with_prefix


def search(query, tf_filename, idf, trie, doc_locations, numResults=10):
    terms = re.split('\W', query)
    final_query = terms[:]

    for word in terms:
        _, _, prefix_match_words = find_words_with_prefix(trie, word)
        final_query.extend(prefix_match_words)

    idf_local = dict([(word, idf.get(word, 0)) for word in final_query])

    scores = {}
    with open(tf_filename, 'rb') as tf_file:
        while True:
            try:
                [message_id, tf_score] = pickle.load(tf_file)
                score = 0
                for word in final_query:
                    score += tf_score.get(word, 0) * idf_local.get(word, 0)
                scores[message_id] = score
            except EOFError:
                break

    top_scorers = sorted(scores.items(), key=lambda tup: tup[1], reverse=True)[:numResults]
    result_emails = []
    for id, _ in top_scorers:
        _, _, email_content = parse_email(doc_locations[id], include_content=True)
        result_emails.append(email_content)

    return result_emails


if __name__ == '__main__':
    tf, idf, trie, doc_locations = create_index("/home/aman/PycharmProjects/testa/maildir/", test=True)
    persist_dict(tf, 'tf.index')

    print("\n\n".join(search('add', "tf.index", idf, trie, doc_locations)))

