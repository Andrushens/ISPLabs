def serialize_toml(obj) -> str:
    if type(obj) == tuple:
        ans = ""
        for i in obj:
            ans += f"{serialize_toml(i)}, "
        return f"[ {ans[0:len(ans) - 1]}]"
    else:
        return f"\"{str(obj)}\"".replace("\n", "\\n")

def deserialize_toml(obj: str):
    if obj == '[]':
        return tuple()
    elif obj[0] == '[':
        obj = obj[1:len(obj) - 1]
        parsed = []
        depth = 0
        quote = False
        substr = ""
        for i in obj:
            if i == '[':
                depth += 1
            elif i == ']':
                depth -= 1
            elif i == '\"':
                quote = not quote
            elif i == ',' and not quote and depth == 0:
                parsed.append(deserialize_toml(substr))
                substr = ""
                continue
            elif i == ' ' and not quote:
                continue
            substr += i
        return tuple(parsed)
    else:
        return obj[1:len(obj) - 1]