import getopt
import sys

options = "h"
long_options = ["Help"]


def parse_args():
    argumentList = sys.argv[1:]
    arguments, values = getopt.getopt(argumentList, options, long_options)

    for currentArgument, currentValue in arguments:
        if currentArgument in ("-h", "--Help"):
            print("Displaying Help")
    return 0


if __name__ == "__main__":
    parse_args()
