"""
    Feature #4: Suggest Possible Queries After Adding White Spaces
    Time complexity
        O(n^2 + 2^n + w), n = query length, l = words length
    Space complexity
        O((n x 2^n) + l)

"""
from functools import cache
from typing import List


def break_query(query: str, dict: List[str]) -> List[str]:
    return helper(query, set(dict), {})

def helper(query, dict, result):
    if not query:
        return []

    if query in result:
        return result[query]

    ans = []
    for word in dict:
        if not query.startswith(word):
            continue
        if len(word) == len(query):
            ans.append(word)
        else:
            result_of_the_rest = helper(query[len(word):], dict, result)
            for item in result_of_the_rest:
                item = word + ' ' + item
                ans.append(item)
    result[query] = ans
    return ans

""" date: 22.01, 
    dp top-down
    O(n * 2^n) time, O(n * 2^n) space 
"""
def decode_coding_interviews_search_engine(s: str, wordDict: List[str]) -> List[str]:
    word_set = set(wordDict)

    # cache on query only,
    # result is redundant with @cache, @cache does it
    @cache
    def dfs(query: str) -> List[str]:
        if not query:
            return []

        ans = []
        for word in word_set:
            if query.startswith(word):
                if len(word) == len(query):
                    ans.append(word)
                else:
                    result_of_rest = dfs(query[len(word):])
                    for item in result_of_rest:
                        item = word + ' ' + item
                        ans.append(item)
        return ans

    return dfs(s)

query = "vegancookbook"
dict = ["an", "book", "car", "cat", "cook", "cookbook", "crash",
        "cream", "high", "highway", "i", "ice", "icecream", "low",
        "scream", "veg", "vegan", "way"]
print(break_query(query, dict))

query = "highwaycarcrash"
print(break_query(query, dict))