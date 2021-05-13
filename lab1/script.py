def solve():
    S = input()
    Q = int(input())
    ans = ""
    changes = [0 for symb in S] 
    for i in range(Q):
        L, R = map(int, input().split(' '))
        for j in range(L - 1, R):
            changes[j] ^= 1
    for i in range(len(S)):
        ans += S[i].swapcase() if changes[i] else S[i]
    return ans


print(solve())
