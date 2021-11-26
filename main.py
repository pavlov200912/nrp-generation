import argparse
import os

from algorithms.replacements import replacements
from algorithms.simple_linear import simple_linear
from domain.acid_graph.save_graph import save_graph
from domain.prediction_codes.parse_prediction_codes import parse_prediction_codes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate possible NRP structure variants.')
    parser.add_argument('input', help='path to directory with antismash outputs')
    parser.add_argument('--algorithm', default='simple', help='code name of an algorithm to use')
    parser.add_argument('--output', help='path to output directory')
    parser.add_argument('--base_name', help='base name for output graph files')
    parser.add_argument('--info_format', action='store_true', help='whether to use .info nerpa graph format')
    parser.add_argument('--info_file', help='obligatory in case if --info_format used, path to file .info')
    parser.add_argument('--monomers',
                        help='path to the file with mapping from genome monomers to popular variants of graph monomers')

    parser.add_argument('--bonds', dest='feature', action='store_true')
    parser.add_argument('--no-bonds', dest='feature', action='store_false')
    parser.set_defaults(feature=True)
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("Invalid argument --input, directory doesn't exist")

    input_dir_path = args.input
    output_dir_path = './out' if args.output is None else args.output
    if not os.path.exists(output_dir_path):
        print("Directory created", output_dir_path)
        os.mkdir(output_dir_path)
    base_name = args.base_name if args.base_name is not None else ''

    algorithm = args.algorithm

    if algorithm == 'simple':
        predictions_path = os.path.join(input_dir_path, '', 'nrpspks_predictions_txt', 'ctg1_nrpspredictor2_codes.txt')
        predictions = parse_prediction_codes(path_to_prediction=predictions_path)
        graph = simple_linear(predictions)
        save_graph(output_dir_path, graph, base_name)
    elif algorithm == 'replacements':
        reverse_path = 'reverse_monomers.json' if args.monomers is None else args.monomers
        path_to_details = os.path.join(input_dir_path, 'details')
        if not os.path.exists(path_to_details):
            raise FileNotFoundError("Can't find directory details")

        path_to_rban = os.path.join(input_dir_path, 'rban.output.json')
        if not os.path.exists(path_to_rban):
            raise FileNotFoundError("Can'r find rban.output.json")

        replacements(path_to_details, path_to_rban, reverse_path, output_dir_path, args.feature,
                     args.info_format, args.info_file)
