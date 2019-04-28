import itertools
import pandas as pd
import timeit
import sys

from coloring.coloring import *
from coloring.examples import cycle

algorithms = {
    'AMIS': amis_fold_color,
    'tDSATUR': total_dsatur_fold_color,
    'oDSATUR': outer_dsatur_fold_color,
    'interCS': cs_interchange_fold_color,
}


def run(algorithm, graph, folds):
    def func():
        return algorithm(graph, folds)

    return func


def test_performance():
    columns = ['folds', 'graph']
    columns.extend(algorithms.keys())
    data = {column: [] for column in columns}

    fold_values = [2, 3, 5, 10]
    min_cl, max_cl, step_cl = 5, 75, 2

    for folds in fold_values:
        for cycle_length in range(min_cl, max_cl, step_cl):
            graph = cycle(cycle_length)
            graph_name = "cycle({})".format(cycle_length)

            data['folds'].append(folds)
            data['graph'].append(graph_name)

            for alg, alg_func in algorithms.items():
                func = run(alg_func, graph, folds)
                time = timeit.timeit(func, number=10)
                data[alg].append(time)

    file_path = 'test/data/odd_cycles_performance.csv'
    df = pd.DataFrame.from_dict(data)
    df.to_csv(file_path, encoding='utf-8')


def test_accuracy():
    columns = ['folds', 'graph', 'algorithm', 'ratio', 'percentage']
    data = {column: [] for column in columns}

    fold_values = [2, 3, 5, 10]
    cycle_lengths = [5, 15, 25, 35, 45]

    for folds in fold_values:
        for cycle_length in cycle_lengths:
            graph = cycle(cycle_length)
            graph_name = "cycle({})".format(cycle_length)

            for alg, alg_func in algorithms.items():
                ratios = []
                for _ in range(100):
                    num_colors, _ = alg_func(graph, folds)
                    color_ratio = num_colors / folds
                    ratios.append(color_ratio)

                ratios_by_count = {ratio: len(list(occurrences))
                                   for ratio, occurrences
                                   in itertools.groupby(ratios)}

                ratios.sort()
                for ratio, count in ratios_by_count.items():
                    data['folds'].append(folds)
                    data['graph'].append(graph_name)
                    data['algorithm'].append(alg)
                    data['ratio'].append(round(ratio, 2))
                    data['percentage'].append(count)

    file_path = 'test/data/odd_cycles_accuracy.csv'
    df = pd.DataFrame.from_dict(data)
    df.to_csv(file_path, encoding='utf-8')


if __name__ == '__main__':
    usage = 'usage: python3 odd_cycles.py [performance | accuracy]'
    if len(sys.argv) < 2:
        print(usage)
    if sys.argv[1] == 'performance':
        test_performance()
    elif sys.argv[1] == 'accuracy':
        test_accuracy()
    else:
        print(usage)
