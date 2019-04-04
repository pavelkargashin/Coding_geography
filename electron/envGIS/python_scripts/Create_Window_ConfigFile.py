import os
import sys


def main(path):
    with open(path, 'w+') as config_file:
        config_file.write("asdasd")


if __name__ == '__main__':
    a = sys.argv[1]
    main(a)
