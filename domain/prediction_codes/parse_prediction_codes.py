import re
from typing import List

from domain.prediction_codes.prediction_codes import PredictionCodes


def parse_prediction_codes(path_to_prediction: str) -> List[PredictionCodes]:
    with open(path_to_prediction) as prediction_file:
        predictions_raw = prediction_file.read().strip()
    predictions = []
    for domain_prediction in predictions_raw.split('\n'):
        name, pred, scores_raw = domain_prediction.split('\t')
        scores = {}
        for score_item in scores_raw.split(';'):
            score_float = float(re.findall(r'[0-9]+.[0-9]+', score_item)[0])
            acid = score_item.split('(')[0]
            scores[acid] = score_float
        predictions.append(PredictionCodes(name, pred, scores))

    return predictions
