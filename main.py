import argparse
import os

from domain.acid_graph.acid_graph import AcidGraph
from domain.acid_graph.save_graph import save_graph
from algorithms.simple_linear import simple_linear
from domain.prediction_codes.parse_prediction_codes import parse_prediction_codes

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate possible NRP structure variants.')
    parser.add_argument('input', help='path to directory with antismash outputs')
    parser.add_argument('--algorithm', default='simple', help='code name of an algorithm to use')
    parser.add_argument('--output', help='path to output directory')
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print("Invalid argument --input, directory doesn't exist")

    input_dir_path = args.input
    output_dir_path = './out' if args.output is None else args.output

    predictions_path = os.path.join(input_dir_path, 'nrpspks_predictions_txt', 'ctg1_nrpspredictor2_codes.txt')
    predictions = parse_prediction_codes(path_to_prediction=predictions_path)

    algorithm = args.algorithm

    if algorithm == 'simple':
        graph = simple_linear(predictions)
        for f in os.listdir(output_dir_path):
            os.remove(os.path.join(output_dir_path, f))
        save_graph(output_dir_path, graph)

