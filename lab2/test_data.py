test_number = 228
test_dict = {test_number: test_number, "b": 123, 228: 456.789}
test_list = [1, "qwe", 3, 22.8, test_dict, (1, 2, 3), False, None]

test_lambda = lambda x: x + test_list[5][2]

def test_recursion(n):
    if n == 0:
        return test_number
    else:
        return n * test_recursion(n - 1)