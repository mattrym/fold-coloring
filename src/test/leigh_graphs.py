import itertools
import pandas as pd
import timeit
import sys

from coloring.coloring import *
from coloring.examples import load_dimacs

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
    chrom_nums = [5, 15, 25]
    variants = ['a', 'b', 'c', 'd']

    for folds in fold_values:
        for chrom_num in chrom_nums:
            for variant in variants:
                print("Testing performance - folds = {}, chrom_num = {}, variant = {}".format(folds, chrom_num, variant))
                filename = "le450_{}{}.col".format(chrom_num, variant)
                file_path = "test/instances/" + filename

                graph = load_dimacs(file_path)
                graph_name = "le450_{}{}".format(chrom_num, variant)

                data['folds'].append(folds)
                data['graph'].append(graph_name)

                for alg, alg_func in algorithms.items():
                    func = run(alg_func, graph, folds)
                    time = timeit.timeit(func, number=10)
                    data[alg].append(time)

    file_path = 'test/data/leigh_graphs_performance.csv'
    df = pd.DataFrame.from_dict(data)
    df.to_csv(file_path, encoding='utf-8')


def test_accuracy():
    columns = ['folds', 'graph', 'algorithm', 'ratio', 'percentage']
    data = {column: [] for column in columns}

    fold_values = [2, 3, 5, 10]
    chrom_nums = [5, 15, 25]
    variants = ['a', 'b', 'c', 'd']

    for folds in fold_values:
        for chrom_num in chrom_nums:
            for variant in variants:
                print("Testing accuracy - folds = {}, chrom_num = {}, variant = {}".format(folds, chrom_num, variant))

                filename = "le450_{}{}.col".format(chrom_num, variant)
                file_path = "test/instances/" + filename

                graph = load_dimacs(file_path)
                graph_name = "le450_{}{}".format(chrom_num, variant)

                for alg, alg_func in algorithms.items():
                    ratios = []
                    for _ in range(100):
                        num_colors, _ = alg_func(graph, folds)
                        color_ratio = num_colors / folds
                        ratios.append(color_ratio)

                    ratios.sort()
                    ratios_by_count = {ratio: len(list(occurrences))
                                       for ratio, occurrences
                                       in itertools.groupby(ratios)}

                    for ratio, count in ratios_by_count.items():
                        data['folds'].append(folds)
                        data['graph'].append(graph_name)
                        data['algorithm'].append(alg)
                        data['ratio'].append(round(ratio, 2))
                        data['percentage'].append(count)

    file_path = 'test/data/leigh_graphs_accuracy.csv'
    df = pd.DataFrame.from_dict(data)
    df.to_csv(file_path, encoding='utf-8')


if __name__ == '__main__':
    usage = 'usage: python3 leigh_graphs.py [performance | accuracy]'
    if len(sys.argv) < 2:
        print(usage)
    if sys.argv[1] == 'performance':
        test_performance()
    elif sys.argv[1] == 'accuracy':
        test_accuracy()
    else:
        print(usage)
