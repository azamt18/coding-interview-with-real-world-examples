"""
    Feature #2: Design Search Autocomplete System

    Time complexity
        ctor(): O(n x l) to create the trie
        addRecord(): O()
        search(): O()
        dfs(): O()
        autoComplete(): O(q + m + l(log(l)))
    Space complexity
        ctor(): O(n x l) to store in the trie
        addRecord(): O()
        search(): O()
        dfs(): O()
        autoComplete(): O(n x l) to output list
"""
from typing import List


class Node:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.data = ""
        self.rank = 0

class AutocompleteSystem:
    def __init__(self, sentences: List[str], times: List[int]):
        self.root = Node()
        self.keyword = ""
        for i, sent in enumerate(sentences):
            self.addRecord(sent, times[i])

    def addRecord(self, sentence: str, hot: int):
        node = self.root
        for c in sentence:
            if c not in node.children:
                node.children[c] = Node()
            node = node.children.get(c)
        node.is_end = True
        node.data = sentence
        node.rank -= hot

    def search(self, query):
        node = self.root
        for c in query:
            if c not in node.children:
                return []
            node = node.children[c]
        return self.dfs(node)

    def dfs(self, node):
        result = []
        if node.is_end:
            result.append((node.rank, node.data))
        for child in node.children:
            child_node = node.children[child]
            child_response = self.dfs(child_node)
            result.extend(child_response)
        return result


    def autoComplete(self, c: str):
        results = []
        if c != '#':
            self.keyword += c
            results = self.search(self.keyword)
        else:
            self.addRecord(self.keyword, 1)
            self.keyword = ""

        results = sorted(results[:3])
        return [sent for rank, sent in results]


# Driver code
sentences = ["beautiful", "best quotes", "best friend", "best birthday wishes", "instagram", "internet"]
times = [30, 14, 21, 10, 10, 15]
auto = AutocompleteSystem(sentences, times)
print(auto.autoComplete("b"))
print(auto.autoComplete("e"))
print(auto.autoComplete("s"))
print(auto.autoComplete("t"))
print(auto.autoComplete("#"))