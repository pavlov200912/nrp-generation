from typing import List

from domain.acid_graph.acid_graph import AcidGraph
from domain.prediction_codes.prediction_codes import PredictionCodes


def simple_linear(predictions: List[PredictionCodes]) -> AcidGraph:
    graph = AcidGraph()
    for i, prediction in enumerate(predictions):
        graph.push_vertex(prediction.predicted_acid)
        if i == 0:
            continue
        graph.push_edge(i - 1, i)

    str(graph)
    return graph
