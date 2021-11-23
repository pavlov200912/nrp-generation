from typing import List

import pandas as pd


class CompoundMatch:
    # ORF_ID
    # A_domain_Idx
    # Prediction_DL - config (not used)
    # Prediction_Top_Residue
    # Prediction_Top_Score
    # Prediction_Modifications
    # Matched_Residue
    # Matched_Residue_Score
    # Nerpa_Score
    # Monomer_Idx
    # Monomer_Code
    # Monomer_DL - config (not used)
    # Monomer_Residue
    # Monomer_Modifications
    def __init__(self, orf_id: str, a_domain_id: int, genome_acid: str,
                 genome_score: int, genome_modification: str,
                 graph_acid: str, graph_score: int,
                 nerpa_score: float, rban_graph_id: int,
                 rban_acid_code: str, rban_acid: str,
                 rban_modification: str):
        self.orf_id = orf_id
        self.a_domain_id = a_domain_id
        self.genome_acid = genome_acid
        self.genome_score = genome_score
        self.genome_modification = genome_modification
        self.graph_acid = graph_acid
        self.graph_score = graph_score
        self.nerpa_score = nerpa_score
        self.rban_graph_id = rban_graph_id
        self.rban_acid_code = rban_acid_code
        self.rban_acid = rban_acid
        self.rban_modification = rban_modification

    @staticmethod
    def from_dataframe_row(row):
        return CompoundMatch(
            orf_id=row['ORF_ID'],
            a_domain_id=int(row['A_domain_Idx']),
            genome_acid=row['Prediction_Top_Residue'],
            genome_score=int(row['Prediction_Top_Score']),
            genome_modification=row['Prediction_Modifications'],
            graph_acid=row['Matched_Residue'],
            graph_score=int(row['Matched_Residue_Score']),
            nerpa_score=float(row['Nerpa_Score']),
            rban_graph_id=int(row['Monomer_Idx']),
            rban_acid_code=row['Monomer_Code'],
            rban_acid=row['Monomer_Residue'],
            rban_modification=row['Monomer_Modifications'],
        )


def parse_compound_match(match_file_content: str):
    match_file_content = match_file_content.strip()
    matches = list(map(lambda x: x.strip(), match_file_content.split('\n\n\n')))

    max_score = None
    top_df = None
    top_name = None

    for m in matches:
        match_lines = m.split('\n')
        compound_name = match_lines[0]
        predictors_path = match_lines[1]
        score = float(match_lines[2].strip().split(' ')[-1])
        alignment = match_lines[3]
        tsv_report = '\n'.join(match_lines[4:])
        if max_score is None or max_score < score:
            max_score = score
            top_df = pd.DataFrame([x.split(' ') for x in tsv_report.split('\n')[1:]],
                                  columns=tsv_report.split('\n')[0].split(' '))

            top_name = compound_name

    return top_df, top_name
