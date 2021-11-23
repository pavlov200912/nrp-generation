import json
import os
from typing import List, Dict

from domain.acid_graph.graph_from_rban import process_rban_compound
from domain.acid_graph.save_graph import save_graph
from domain.match.compound_match import parse_compound_match, CompoundMatch
from domain.replacement.replacement import Replacement, build_graph_with_replacement


def replacements_from_compound(match: CompoundMatch, reverse_monomers: Dict[str, List[str]]) -> List[Replacement]:
    replacements = []
    for new_graph_acid in reverse_monomers[match.genome_acid]:
        replacements.append(
            Replacement(
                match.rban_graph_id,
                match.graph_acid,
                new_graph_acid
            )
        )
    return replacements


def generate_replacements(compound_variant_match: str, reverse_monomers: Dict[str, List[str]]) -> List[
    Replacement]:
    df, name = parse_compound_match(compound_variant_match)
    df['neq'] = (df['Prediction_Top_Residue'] != df['Matched_Residue'])
    df['not_none'] = (df['Prediction_Top_Residue'] != 'none') & (df['Matched_Residue'] != 'none')
    replacement_rows = (df[df['not_none'] & df['neq']])

    all_replacements = []

    print(f"Found {len(replacement_rows)} mismatches")

    for _, row in replacement_rows.iterrows():
        match = CompoundMatch.from_dataframe_row(row)
        reps = replacements_from_compound(match, reverse_monomers)
        all_replacements.extend(reps)

    print(f"Generated {len(all_replacements)} replacements")
    return all_replacements


def replacements(path_to_details: str, path_to_rban: str, reverse_path: str, path_to_output: str):
    with open(reverse_path) as file:
        reverse_monomers = json.load(file)

    with open(path_to_rban) as rban_file:
        compounds = json.load(rban_file)

    for compound_variant_path in os.listdir(path_to_details):
        compound_name = '_'.join(compound_variant_path.split('_')[:2])
        variant_name = compound_variant_path.split('_')[-1].split('.')[0]
        print("Processing", compound_name, variant_name)
        with open(os.path.join(path_to_details, compound_variant_path)) as match_file:
            compound_variant_match = match_file.read()
        compound_graph = [c for c in compounds if c['id'] == compound_name][0]
        graph = process_rban_compound(compound_graph)

        reps = generate_replacements(compound_variant_match, reverse_monomers)
        for rep in reps:
            new_graph = build_graph_with_replacement(graph, rep)
            save_graph(path_to_output, new_graph, base_name=compound_name + '_' + variant_name)

