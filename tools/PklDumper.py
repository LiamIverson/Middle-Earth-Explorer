# Tool to dump pickle file attributes to ensure
# editor is properly populating attributes

import sys
import pickle
import pandas as pd

sys.path.append('../')

def main():
    path = sys.argv[1]
    objects = []
    with open(path, "rb") as openfile:
        while True:
            try:
                objects.append(pd.read_pickle(openfile))
            except EOFError:
                break
    for object in objects:
        print(vars(object))


if __name__ == "__main__":
    main()
