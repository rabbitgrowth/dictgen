from collections import defaultdict

class Trie:
    def __init__(self, pairs):
        self.root = Node()
        for key, value in pairs:
            node = self.root
            for char in key:
                node = node.children[char]
            node.values.append(value)

    def lookup(self, word):
        node = self.root
        yield node.values
        for char in word:
            if char not in node.children:
                return
            node = node.children[char]
            yield node.values

class Node:
    def __init__(self):
        self.values   = []
        self.children = defaultdict(Node)
