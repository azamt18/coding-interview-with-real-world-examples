"""
    Feature #1: Store and Fetch Words

    Time complexity
        insertWord(): O(l)
        searchWord(): O(l)
        startsWith(): O(l)
    Space complexity
        insertWord(): O(l) for l nodes in trie
        searchWord(): O(1)
        startsWith(): O(1)

    l = length of the word
"""

class Node:
    def __init__(self):
        self.children = {}
        self.is_word = False

class WordDictionary:
    def __init__(self):
        self.root = Node()

    def insertWord(self, word: str) -> None:
        node = self.root
        for c in word:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children.get(c)
        node.is_word = True

    def searchWord(self, word: str) -> bool:
        node = self.root
        for c in word:
            if c not in node.children:
                return False
            node = node.children.get(c)
        return node.is_word

    def startsWith(self, prefix: str) -> bool:
        node = self.root
        for c in prefix:
            if c not in node.children:
                return False
            node = node.children.get(c)
        return True

# driver code
keys = ["the", "a", "there", "answer", "any",
        "by", "bye", "their", "abc"]
print("Keys to insert: ")
print(keys)

d = WordDictionary()

for i in range(len(keys)):
    d.insertWord(keys[i])

print("Searching 'there' in the dictionary results: " + str(d.searchWord("there")))
print("Searching the prefix 'by' in the dictionary results: " + str(d.startsWith("by")))