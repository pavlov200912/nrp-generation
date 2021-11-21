from typing import Dict, List, Tuple


class AcidGraph:
    def __init__(self):
        self.vertex_names: Dict[int, str] = {}
        self.edges: List[Tuple[int, int]] = []

    def push_edge(self, v1: int, v2: int):
        self.edges.append((v1, v2))

    def push_vertex(self, v_name: str):
        self.vertex_names[len(self.vertex_names)] = v_name

    def __str__(self):
        return ','.join([v for k, v in sorted(self.vertex_names.items(), key=lambda x: x[0])]) \
               + ';' + ';'.join(str(a) + ',' + str(b) for a, b in self.edges)

    def from_string(self, acid_graph_string: str):
        acid_graph_string = acid_graph_string.strip()
        self.edges = [tuple(map(int, edge.split(','))) for edge in acid_graph_string.split(';')[1:]]
        vertices = acid_graph_string.split(';')[0].split(',')
        self.vertex_names = {i: name for i, name in enumerate(vertices)}
        return self