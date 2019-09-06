

class TrieNode(object):
    def __init__(self, char: str):
        self.char = char
        self.children = []
        self.word_finished = False
        self.counter = 1

    def add(self, word: str):
        node = self
        for char in word:
            found_in_child = False
            for child in node.children:
                if child.char == char:
                    child.counter += 1
                    node = child
                    found_in_child = True
                    break
            if not found_in_child:
                new_node = TrieNode(char)
                node.children.append(new_node)
                node = new_node
        node.word_finished = True


def _find_all_words_dfs_(node, word, word_list):
    new_word = word + node.char
    if node.word_finished:
        word_list.append(new_word)

    for ch in node.children:
        _find_all_words_dfs_(ch, new_word, word_list)


def find_words_with_prefix(root, prefix):
    node = root
    if not root.children:
        return False, 0
    for char in prefix:
        char_not_found = True
        for child in node.children:
            if child.char == char:
                char_not_found = False
                node = child

        if char_not_found:
            return False, 0, []

    word_list = []
    _find_all_words_dfs_(node, prefix[:-1], word_list)


    # Well, we are here means we have found the prefix. Return true to indicate that
    # And also the counter of the last node. This indicates how many words have this
    # prefix
    return True, node.counter, word_list


if __name__ == "__main__":
    root = TrieNode('*')
    root.add("hackathon")
    root.add('hack')

    print(find_words_with_prefix(root, 'hac'))
