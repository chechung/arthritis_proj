#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
data_proc.py
Demo including:
    - reading in numeric data from a csv
    - calculating the mean, max, and min per row
    - plotting the results
"""

import sys
import argparse
import numpy as np
import matplotlib.pyplot as plt
import os

IO_ERROR = 2
SUCCESS = 0

DEF_DATA_FILE = "data.csv"


def warning(*objs):
    """Writes a message to stderr."""
    print("WARNING: ", *objs, file=sys.stderr)


# def canvas(with_attribution=True):
#     """
#     Placeholder function to show example docstring (NumPy format)
#
#     Replace this function and doc string for your own project
#
#     Parameters
#     ----------
#     with_attribution : bool, Optional, default: True
#         Set whether or not to display who the quote is from
#
#     Returns
#     -------
#     quote : str
#         Compiled string including quote and optional attribution
#     """
#
#     quote = "The code is but a canvas to our imagination."
#     if with_attribution:
#         quote += "\n\t- Adapted from Henry David Thoreau"
#     return quote

def data_analysis(data_array):
    """
    Finds the average, min, and max for each row of the given array

    Parameters
    ----------
    data_array : numpy array of patient data (one line per patient, daily measurements) in plasma inflammation units

    Returns
    -------
    data_stats : numpy array
        array with same number of rows as data_array, and columns for average, max, and min values (in that order)
    """
    num_patients, num_days = data_array.shape
    data_stats = np.zeros((num_patients, 3))

    data_stats[:, 0] = np.mean(data_array, axis=1)
    data_stats[:, 1] = np.max(data_array, axis=1)
    data_stats[:, 2] = np.min(data_array, axis=1)

    return data_stats


def parse_cmdline(argv):
    """
    Returns the parsed argument list and return code.
    `argv` is a list of arguments, or `None` for ``sys.argv[1:]``.
    """
    if argv is None:
        argv = sys.argv[1:]

    # initialize the parser object:
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--csv_data_file", help="The location of the csv file with data to analyze",
                        default=DEF_DATA_FILE)
    args = None
    try:
        args = parser.parse_args(argv)
        args.csv_data = np.loadtxt(fname=args.csv_data_file, delimiter=',')
    except IOError as e:
        warning("Problems reading file:", e)
        parser.print_help()
        return args, IO_ERROR

    return args, SUCCESS


def plot_stats(base_f_name, data_stats):
    """
    Makes a plot of the mean, max, and min inflammation per patient
    :param base_f_name: str of base output name (without extension)
    :param data_stats: numpy array with shape (num_patients, num_stats) where num_stats = 3 (mean, max, min)
    :return: saves a png file
    """
    num_patients, num_stats = data_stats.shape
    x_axis = np.arange(1, num_patients + 1, 1)
    # red dashes, blue squares and green triangles
    plt.plot(x_axis, data_stats[:, 0], 'bs',
             x_axis, data_stats[:, 1], 'g^',
             x_axis, data_stats[:, 2], 'r.')
    plt.title('Patient Arthritis Data')
    plt.xlabel('Patient Number')
    plt.ylabel('Plasma Inflammation Units')
    out_name = base_f_name + ".png"
    plt.savefig(out_name)
    print("Wrote file: {}".format(out_name))


def main(argv=None):
    args, ret = parse_cmdline(argv)
    if ret != SUCCESS:
        return ret
    data_stats = data_analysis(args.csv_data)

    # get the name of the input file without the directory it is in, if one was specified
    base_out_fname = os.path.basename(args.csv_data_file)
    # get the first part of the file name (omit extension) and add the suffix
    base_out_fname = os.path.splitext(base_out_fname)[0] + '_stats'
    # add suffix and extension
    out_fname = base_out_fname + '.csv'
    np.savetxt(out_fname, data_stats, delimiter=',')
    print("Wrote file: {}".format(out_fname))

    # send the base_out_fname and data to a new function that will plot the data
    plot_stats(base_out_fname, data_stats)
    return SUCCESS  # success


if __name__ == "__main__":
    status = main()
    sys.exit(status)
