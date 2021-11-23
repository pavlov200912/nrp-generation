from domain.acid_graph.acid_graph import AcidGraph


def process_rban_compound(comp) -> AcidGraph:
    # Andy's code
    name = comp['id']
    comp = comp['monomericGraph']['monomericGraph']
    monomers = comp['monomers']
    bonds = comp['bonds']
    nodes = []
    edges = []
    s = ''
    for monomer in monomers:
        nodes.append(sorted(monomer['monomer']['monomer']['codes'], key=len)[0])
        s += sorted(monomer['monomer']['monomer']['codes'], key=len)[0] + ','
    s = s[:-1]
    for bond in bonds:
        edges.append(bond['bond']['monomers'])
        s += ';' + str(bond['bond']['monomers'][0] - 1) + ',' + str(bond['bond']['monomers'][1] - 1)
    return AcidGraph().from_string(s)