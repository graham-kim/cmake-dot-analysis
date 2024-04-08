import typing as tp
import argparse
import networkx as nx

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dot_filename', help="Input .dot file name")
    parser.add_argument('input_cmds_filename', help="Path to instructions")
    parser.add_argument('--twopi', help="Flag to use twopi when drawing")
    return parser

class OutputGraphBuilder:
    def __init__(self, inG: nx.DiGraph):
        self.inG = inG
        self.outG = nx.DiGraph()

    def _add_out_node(self, node_name: str):
        if node_name not in self.outG:
            self.outG.add_node(node_name)

    def add_link_between(self, from_node: str, to_node: str):
        self._add_out_node(from_node)
        self._add_out_node(to_node)
        self.outG.add_edge(from_node, to_node)

    def add_immediate_child_nodes_of(self, target_node: str):
        self._add_out_node(target_node)

        child_nodes = list(nx.neighbors(self.inG, target_node))
        for child_node in child_nodes:
            self._add_out_node(child_node)
            self.outG.add_edge(target_node, child_node)

def get_graph_to_draw(inG: nx.DiGraph, args) -> nx.DiGraph:
    builder = OutputGraphBuilder(inG)

    with open(args.input_cmds_filename, 'r') as inF:
        for line in inF:
            if "->" in line:
                tokens = line.split("->")
                assert len(tokens) > 1, f"Need >= 1 token around '->':\n{line}"
                tokens = [tok.strip() for tok in tokens]
                for i in range(1,len(tokens)):
                    if tokens[i] == "*":
                        assert tokens[i-1] != "*", f"Can't have double * around '->':\n{line}"
                        builder.add_immediate_child_nodes_of(tokens[i-1])
                    else:
                        builder.add_link_between(tokens[i-1], tokens[i])

    return builder.outG

if __name__ == '__main__':
    args = setup_parser().parse_args()
    inG = nx.DiGraph(nx.nx_pydot.read_dot(args.input_dot_filename))

    if false:
        outG = get_graph_to_draw(inG, args)

        dot_prog = "twopi" if args.twopi else None
        nx.nx_pydot.to_pydot(outG).write_jpg("out.jpg", prog=dot_prog)

    

