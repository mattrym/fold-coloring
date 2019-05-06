import argparse
import time

from coloring.coloring import (
    amis_fold_color,
    cs_interchange_fold_color,
    outer_dsatur_fold_color,
    total_dsatur_fold_color
)
from coloring.examples import load_dimacs

algorithms = {
    'AMIS': amis_fold_color,
    'interCS': cs_interchange_fold_color,
    'oDSATUR': outer_dsatur_fold_color,
    'tDSATUR': total_dsatur_fold_color,
}


def run(path, algorithm, folds):
    graph = load_dimacs(path)
    fun = algorithms[algorithm]

    start_time = time.time()
    num_colors, coloring = fun(graph, folds)
    end_time = time.time()

    print('*** Time elapsed (in seconds): {}'.format(end_time - start_time))
    print('*** Number of colors: {}'.format(num_colors))
    print()
    print('*** Coloring: ')
    for vertex, colors in coloring.items():
        print('{}: {}'.format(vertex, colors))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run fold coloring')
    parser.add_argument('path',
                        type=str,
                        help='path to graph file')
    parser.add_argument('algorithm',
                        choices=algorithms.keys(),
                        help='algorithm name')
    parser.add_argument('folds',
                        type=int,
                        help='number of folds')
    args = parser.parse_args()

    run(args.path, args.algorithm, args.folds)
