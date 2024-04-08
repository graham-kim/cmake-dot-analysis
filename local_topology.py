import typing as tp
import argparse
import networkx as nx

def setup_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument('input_dot_filename', help="Input .dot file name")
    parser.add_argument('--target', help="Node to focus analysis on")
    return parser

def get_immediate_child_nodes(inG: nx.DiGraph, target_node: str):
    outG = nx.DiGraph()
    outG.add_node(target_node, shape='box')
    child_nodes = list(nx.neighbors(inG, target_node))
    for child_node in child_nodes:
        outG.add_node(child_node)
        outG.add_edge(target_node, child_node)

    dot_prog = None if len(child_nodes) < 4 else "twopi"
    nx.nx_pydot.to_pydot(outG).write_jpg("out.jpg", prog=dot_prog)

if __name__ == '__main__':
    args = setup_parser().parse_args()
    inG = nx.DiGraph(nx.nx_pydot.read_dot(args.input_dot_filename))

    if args.target is not None:
        get_immediate_child_nodes(inG, args.target)

    

