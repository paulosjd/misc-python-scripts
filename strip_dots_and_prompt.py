"""
Usage: python strip_dots_and_prompt.py myfile.txt
Strips first 4 characters (prompts/dots and whitespace) to allow copy, paste and run code snippets
Example input file contents:
>>> @my_decorator
... def my_function(a, b):
...     return a + b
...
"""
import sys


def main(filename):
    cleaned = []
    with open(filename, 'r') as file:
        for line in file.readlines():
            try:
                cleaned.append(line[4:])
            except IndexError:
                pass
    with open(filename, 'a') as file:
        file.write('\n\n')
        file.writelines(cleaned)


if __name__ == '__main__':
    main(sys.argv[1])
