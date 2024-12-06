import re

text = "qweqwewq_CHANGE_123123(xxxx,aaaa)"
pattern = r'^.*CHANGE.*\(([^)]+),([^)]+)\).*$'
match = re.match(pattern, text)
if match:
    print("'CHANGE'")
    print("a", match.group(1))
    print("b", match.group(2))
