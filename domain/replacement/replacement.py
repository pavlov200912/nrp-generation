from domain.acid_graph.acid_graph import AcidGraph


class Replacement:
    def __init__(self, replacement_node_index: int, graph_acid: str, genome_acid: str):
        self.replacement_node_index = replacement_node_index
        self.graph_acid = graph_acid
        self.genome_acid = genome_acid

    def __repr__(self):
        return self.graph_acid + '-->' + self.genome_acid

    def __str__(self):
        return self.__repr__()


def build_graph_with_replacement(graph: AcidGraph, replacement: Replacement) -> AcidGraph:
    new_graph = AcidGraph()
    new_graph.vertex_names = graph.vertex_names
    new_graph.edges = graph.edges
    new_graph.vertex_names[replacement.replacement_node_index] = replacement.genome_acid
    return new_graph