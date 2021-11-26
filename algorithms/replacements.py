import json
import os
import shutil
from collections import defaultdict
from typing import List, Dict

from domain.acid_graph.acid_graph import AcidGraph, AcidLabeledGraph
from domain.acid_graph.graph_from_rban import process_rban_compound
from domain.match.compound_match import parse_compound_match, CompoundMatch
from domain.replacement.replacement import Replacement, build_graph_with_replacement


def replacements_from_compound(match: CompoundMatch, bgc: str, reverse_monomers: Dict[str, List[str]]) -> List[
    Replacement]:
    replacements = []
    for new_graph_acid in reverse_monomers[match.genome_acid]:
        replacements.append(
            Replacement(
                match.rban_graph_id,
                match.graph_acid,
                new_graph_acid,
                bgc
            )
        )
    return replacements


def generate_replacements(compound_variant_match: str, reverse_monomers: Dict[str, List[str]]) -> List[
    Replacement]:
    dfs, bgcs, scores = parse_compound_match(compound_variant_match)
    all_replacements = []

    print(f"Found {len(dfs)} alignments")
    replacement_count = 0
    for df, bgc in zip(dfs, bgcs):

        df['neq'] = (df['Prediction_Top_Residue'] != df['Matched_Residue'])
        df['not_none'] = (df['Prediction_Top_Residue'] != 'none') & (df['Matched_Residue'] != 'none')
        replacement_rows = (df[df['not_none'] & df['neq']])

        replacement_count += len(replacement_rows)

        for _, row in replacement_rows.iterrows():
            match = CompoundMatch.from_dataframe_row(row)
            reps = replacements_from_compound(match, bgc, reverse_monomers)
            all_replacements.extend(reps)

    print(f"Found {replacement_count} mismatches")
    print(f"Generated {len(all_replacements)} replacements")
    return all_replacements


def replacements(path_to_details: str, path_to_rban: str, reverse_path: str, path_to_output: str,
                 bonds: bool, info_format: bool, info_path: str = None):
    with open(reverse_path) as file:
        reverse_monomers = json.load(file)


    if not info_format:
        with open(path_to_rban) as rban_file:
            compounds = json.load(rban_file)
    else:
        compounds = {}
        with open(info_path) as info_file:
            lines = info_file.read().strip().split('\n')
            for line in lines:
                graph_str = line.split(' ')[1]
                name_strs = line.split(' ')[-1]
                names = [a for a in name_strs.split('|') if a != '']
                for name in names:
                    compounds[name] = graph_str




    print("WARNING: Removing content from", path_to_output)
    for filename in os.listdir(path_to_output):
        if 'BGC' in filename:
            file_path = os.path.join(path_to_output, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    for compound_variant_path in os.listdir(path_to_details):
        if not info_format:
            compound_name = '_'.join(compound_variant_path.split('_')[:-1])
            variant_name = compound_variant_path.split('_')[-1].split('.')[0]
            print("Processing", compound_name, variant_name)
            compound_graph = [c for c in compounds if c['id'] == compound_name][0]
            graph = process_rban_compound(compound_graph)
        else:
            compound_name = compound_variant_path[:-len('.match')]
            graph = AcidLabeledGraph().from_string(compounds[compound_name])
            print(graph)

        with open(os.path.join(path_to_details, compound_variant_path)) as match_file:
            compound_variant_match = match_file.read()

        reps = generate_replacements(compound_variant_match, reverse_monomers)



        bgc_to_graphs = defaultdict(list)
        for rep in reps:
            if not bonds:
                new_graph = build_graph_with_replacement(graph, rep)
                new_graph_no_bonds = AcidGraph()
                new_graph_no_bonds.vertex_names = new_graph.vertex_names
                new_graph_no_bonds.edges = [(a, b) for a, b, c in new_graph.edges]

                bgc_to_graphs[rep.bgc].append(
                    str(new_graph_no_bonds)
                )

            else:
                new_graph = build_graph_with_replacement(graph, rep)
                bgc_to_graphs[rep.bgc].append(
                    str(new_graph)
                )
                print(len(new_graph.edges))

        for bgc, graphs in bgc_to_graphs.items():
            with open(os.path.join(path_to_output, compound_name + '_' + bgc + '.txt'), 'a') as file:
                file.write('\n'.join(graphs))
