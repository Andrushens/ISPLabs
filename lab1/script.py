def solve():
    """Дана строка S и Q запросов вида L R - промежуток, на котором нужно инвертировать регистр символов. Требутеся найти строку S после выполнения всех запросов"""
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
    print(ans)


print(solve.__doc__)
solve()
