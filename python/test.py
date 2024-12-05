import pandas as pd
import Exception
import re

def main():
    s = input("Enter a string: ")
    pattern = r'\((.*),(.*)\)'
    result = re.search(pattern, s)
    if result:
        x = result.group(1)
        y = result.group(2)
        try:
            x = int(result.group(1))
        except ValueError:
            pass
        try:
            y = int(result.group(2))
        except ValueError:
            pass
        
        print("x =", x)
        print("y =", y)
    else:
        print("No match")

if __name__ == '__main__':
    main()
