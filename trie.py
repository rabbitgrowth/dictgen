from collections import defaultdict

class Trie:
    def __init__(self, default_factory=None):
        self.root = Node()
        self.default_factory = default_factory

    def __getitem__(self, key):
        node = self.root
        for char in key:
            node = node.children[char]
        if self.default_factory is not None and node.value is None:
            node.value = self.default_factory()
        return node.value

    def __setitem__(self, key, value):
        node = self.root
        for char in key:
            node = node.children[char]
        node.value = value

    def lookup_prefixes(self, word):
        node = self.root
        if node.value is not None:
            yield node.value
        for char in word:
            if char not in node.children:
                return
            node = node.children[char]
            if node.value is not None:
                yield node.value

class Node:
    def __init__(self):
        self.value = None
        self.children = defaultdict(Node)
