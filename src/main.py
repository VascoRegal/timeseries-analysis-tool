from timeseries import *
from parsers import *
import sys

def main():
    if len(sys.argv) != 2:
        exit("File not provided")
    
    groups = []

    config = json_parser(sys.argv[1])

    global_vals = config['global']
    timeseries = config['timeseries']

    for g in timeseries.keys():
        groups.append(SeriesGroup(global_vals, g, timeseries[g]))

    for g in groups:
        g.visit_series()

if __name__ == '__main__':
    main()