import os

from domain.acid_graph.acid_graph import AcidGraph


def save_graph(path_to_output: str, graph: AcidGraph):
    if not os.path.exists(path_to_output):
        print("Directory created", path_to_output)
        os.mkdir(path_to_output)
    already_existed_num = len(os.listdir(path_to_output))

    with open(os.path.join(path_to_output, f'graph_{already_existed_num}.txt'), 'w') as graph_file:
        graph_file.write(str(graph))

