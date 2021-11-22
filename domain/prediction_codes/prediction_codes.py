from typing import Dict


class PredictionCodes:
    def __init__(self, domain_name: str, predicted_acid: str, acid_scores: Dict[str, float]):
        self.domain_name = domain_name
        self.predicted_acid = predicted_acid
        self.acid_scores = acid_scores

    def __repr__(self):
        return f"Domain: {self.domain_name}, Predicted: {self.predicted_acid}, Scores: {str(self.acid_scores)}"
