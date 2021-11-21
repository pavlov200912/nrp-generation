from typing import List

from domain.acid_graph.acid_graph import AcidGraph
from domain.prediction_codes.prediction_codes import PredictionCodes


def simple_linear(predictions: List[PredictionCodes]) -> AcidGraph:
    graph = AcidGraph()
    prev_v = None
    for prediction in predictions:
        if prev_v is None:
            prev_v = prediction.predicted_acid
            continue
        graph.push_edge(v1_name=prev_v, v2_name=prediction.predicted_acid)
        prev_v = prediction.predicted_acid
    return graph
