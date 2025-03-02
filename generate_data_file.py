import sys
import os
import argparse

sys.path.append(os.path.join(os.path.dirname(__file__), "treecut"))

from treecut.gen_data import generate_qa_file
import random

random.seed(42)

def main():
    parser = argparse.ArgumentParser(description="Generate a QA data file with specified parameters.")

    # Define arguments with help messages
    parser.add_argument("--theme", type=str, required=True, choices=["food", "outfit"],
                        help="Either 'food' or 'outfit'. 'food' is used in the paper.")
    parser.add_argument("--compositeName", type=lambda x: (str(x).lower() == "true"), required=True, help="True/False for composite/simple item names.")
    parser.add_argument("--numVars", type=int, required=True, help="Number of variables.")
    parser.add_argument("--ansDepth", type=int, required=True, help="Answer depth.")
    parser.add_argument("--order", type=str, required=True, choices=["random", "forward", "backward"],
                        help="Order of the sentences.")
    parser.add_argument("--hallu", type=lambda x: (str(x).lower() == "true"), required=True,
                        help="True/False for unanswerable/answerable problems.")
    parser.add_argument("--cutDepth", type=int, default=0, help="cutDepth for unanswerable problem.")
    parser.add_argument("--REP", type=int, default=100, help="Number of generated problems in the file.")
    parser.add_argument("--overwrite", type=lambda x: (str(x).lower() == "true"), default=False,
                        help="Overwrite existing files (True/False).")
    parser.add_argument("--verbose", type=lambda x: (str(x).lower() == "true"), default=False,
                        help="Verbose output (True/False).")

    # Parse arguments
    args = parser.parse_args()

    # Call the function with parsed arguments
    generate_qa_file(
        theme=args.theme,
        compositeName=args.compositeName,
        numVars=args.numVars,
        ansDepth=args.ansDepth,
        order=args.order,
        hallu=args.hallu,
        cutDepth=args.cutDepth,
        REP=args.REP,
        overwrite=args.overwrite,
        verbose=args.verbose
    )


if __name__ == "__main__":
    main()
