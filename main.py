import click
import os
import sys
import csv
from outlier_dm import detect_outliers_subpopulation_lattice
from preprocessing_dm import construct_input_csv


def search_file(filename, searchPath):
    """
    Given a search path, find file
    """
    fileFound = 0
    for path in searchPath:
        if os.path.isfile(os.path.join(path, filename)):
            fileFound = 1
            break
    if fileFound:
        return os.path.abspath(os.path.join(path, filename))
    else:
        return None


def validate_csv(fname):
    with open(fname) as csvfile:
        csv.reader(csvfile)
    return True


@click.command()
@click.option('--csv', default='', help='path of the input file in csv format')
@click.option('--link', default='', help='link of the input file in json format')
def do_outlier_detection(csv, link):
    """
    input data can be a csv file, or a link of the json file
    :param csv:
    :param link:
    :return:
    """
    if csv != '':
        if not os.path.isabs(csv):
            csv = search_file(csv, sys.path+[os.getcwd()])

        if os.path.isfile(csv):
            if validate_csv(csv):
                detect_outliers_subpopulation_lattice(csv)
            else:
                print('input csv file is not valid')
    if link != '':
        csv = construct_input_csv(link)
        if validate_csv(csv):
            detect_outliers_subpopulation_lattice(csv)
        else:
            print('input link is not valid json link')


if __name__ == '__main__':
    do_outlier_detection()

