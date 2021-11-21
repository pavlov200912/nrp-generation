from typing import Dict, List, Tuple


class AcidGraph:
    def __init__(self):
        self.vertex_names: List[str] = []
        self.vertices: Dict[str, int] = {}
        self.edges: List[Tuple[int, int]] = []

    def push_edge(self, v1_name: str, v2_name: str):
        if v1_name not in self.vertices:
            self.vertices[v1_name] = len(self.vertices)
            self.vertex_names.append(v1_name)

        if v2_name not in self.vertices:
            self.vertices[v2_name] = len(self.vertices)
            self.vertex_names.append(v2_name)

        self.push_edge_index(self.vertices[v1_name], self.vertices[v2_name])

    def push_edge_index(self, v1: int, v2: int):
        self.edges.append((v1, v2))

    def __str__(self):
        return ','.join(self.vertex_names) + ';' + ';'.join(str(a) + ',' + str(b) for a, b in self.edges)

    def from_string(self, acid_graph_string: str):
        acid_graph_string = acid_graph_string.strip()
        self.edges = [tuple(map(int, edge.split(','))) for edge in acid_graph_string.split(';')[1:]]
        self.vertices = acid_graph_string.split(';')[0].split(',')
        self.vertex_names = {name: i for i, name in enumerate(self.vertices)}
        return self