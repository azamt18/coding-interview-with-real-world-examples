"""
    Feature #3: Add White Spaces to Create Words
    Time complexity
        O(n^2) for two nested loops x O(n) for substring computation = O(n^3)
    Space complexity
        O(n)
"""

def break_query(query, dict) -> bool:
    n = len(query)
    dp = [False for i in range(n+1)]
    dp[0] = True # "" empty space is always present

    for i in range(n):
        if dp[i] == True:
            for dict_word in dict:
                substring_length = len(dict_word)
                if i+substring_length > n:
                    continue
                substring = query[i:i+substring_length]
                if substring == dict_word:
                    dp[i+substring_length] = True
    return dp[n]

dict = ["i", "cream", "cook", "scream", "ice", "cat", "book", "icecream", "vegan"]

query = "vegancookbook"
print(break_query(query, dict))

query = "veganicetea"
print(break_query(query, dict))