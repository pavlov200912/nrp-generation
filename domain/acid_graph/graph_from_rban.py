from domain.acid_graph.acid_graph import AcidLabeledGraph


def process_rban_compound(comp) -> AcidLabeledGraph:
    # Andy's code
    name = comp['id']
    comp = comp['monomericGraph']['monomericGraph']
    monomers = comp['monomers']
    bonds = comp['bonds']
    nodes = []
    edges = []
    s = ''
    for monomer in monomers:
        monomer_name = monomer['monomer']['monomer']['monomer']
        nodes.append(monomer_name)
        s += monomer_name + ','
    s = s[:-1]
    for bond in bonds:
        edges.append(bond['bond']['monomers'])
        s += ';' + str(bond['bond']['monomers'][0] - 1) + ',' + str(bond['bond']['monomers'][1] - 1) + \
             ',' + str(bond['bond']['bondTypes'][0])
    return AcidLabeledGraph().from_string(s)
