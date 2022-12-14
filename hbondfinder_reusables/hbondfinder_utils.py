import getopt
import math
import sys
import argparse
import os

"""
This file contains some utility functions for working with hbondfinder format
    - run hbondfinder in one function
    - make a folder for holding hbondfinder data
    - batch run hbondfinder (not yet implemented)
    - provide an input of HBondFinder file lines split using spaces, and will parse it to find intramolecular or intermolecular edges between atoms
"""


def read_and_parse_folder(dir):
    PDBlist = os.listdir(dir)
    return PDBlist


# Main function to run hbond finder on an input file. Unfortunately, no option to specify an output.
def run_hbondfinder(file):
    make_hbondfinder_dir()
    PDBcode = file.split(".")[0]
    if os.path.exists("/hbondfinder/HBondFinder_" + PDBcode):
        print("File already ran through HBondFinder.")
    else:
        os.system(
            "python hbondfinder.py -i "
            + file
            + " -j JSON_Files/acceptors_donors_dict.json"
        )


# Util function to make a folder for collecting hbondfinder data
def make_hbondfinder_dir():
    print("Creating hbondfinder folder for collecting results...")
    try:
        os.mkdir("hbondfinder_data")
        print("---Successfully created folder---")
    except OSError as error:
        print("---Directory already exists. Adding files to existing directory---")


# Not yet tested
def batch_run_hbondfinder(dir):
    make_hbondfinder_dir()
    file_list = read_and_parse_folder(dir)
    for each in file_list:
        os.system(
            "python hbondfinder.py -i ./"
            + dir
            + "/"
            + each
            + " -j JSON_Files/acceptors_donors_dict.json"
        )


def parse_hbond_lines(lines, inter=False):
    edges = []
    for line in lines:
        if line[0] == line[4]:
            same_chain = True
        else:
            same_chain = False
        if inter == False or same_chain == False:
            donor = line[0] + line[1]
            acceptor = line[4] + line[5]
            dist = line[8]
            edge = [donor, acceptor, dist]
            edges.append(edge)

    return edges


def main():
    # os.chdir(hbondfinder_path)
    print(os.listdir())
    # PDBlist = read_and_parse_folder()
    # run_hbondfinder(PDBlist)
    # run_hbondfinder("../Dataset/1A4Y.pdb")


if __name__ == "__main__":
    main()
