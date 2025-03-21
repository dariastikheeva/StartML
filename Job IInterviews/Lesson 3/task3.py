def is_subsequence(s: str, t: str) -> bool:
    """
    Given two strings s and t, return True if s is a subsequence of t, and False otherwise.
    For example:
    is_subsequence("abc", "ahbgdc") == True
    is_subsequence("axc", "ahbgdc") == False
    """
    i = 0
    j = 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            i += 1
        j += 1
    return i == len(s)
