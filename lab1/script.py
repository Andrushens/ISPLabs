def solve(s):
    if len(s) == 1:
        return s
    return s[0:-1] if s == s[::-1] else s

print(solve(input()))
