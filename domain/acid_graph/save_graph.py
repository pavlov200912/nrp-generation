import os

from domain.acid_graph.acid_graph import AcidGraph


def save_graph(path_to_output: str, graph: AcidGraph, base_name: str):
    already_existed_num = len(list(filter(lambda x: x.startswith(base_name), os.listdir(path_to_output))))

    with open(os.path.join(path_to_output, f'{base_name}_graph_{already_existed_num}.txt'), 'w') as graph_file:
        graph_file.write(str(graph))
