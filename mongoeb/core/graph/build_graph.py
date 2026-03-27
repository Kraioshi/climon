from pyvis.network import Network
from mongoeb.core.graph.build_tree import build_tree

SHAPE_COLOR = "#6FA8DC"
EDGE_COLOR = "#303342"

def build_graph(net: Network, collection: str, field_map: dict):

    # ROOT NODES
    node_map = {"ROOT": 0}

    net.add_node(n_id=0, label=collection, size=20, color="#01915f", shape="diamond")
    tree = build_tree([key for key in field_map])
    tree_keys = [key for key in tree]

    count = 1
    for key in tree_keys:
        node_map[key] = count


        net.add_node(n_id=count, label=key, size=10, shape="dot", color=SHAPE_COLOR)
        net.add_edge(source=count, to=0, color=EDGE_COLOR)

        count += 1

    for parent_key, children in tree.items():
        parent_id = node_map[parent_key]

        for child_key in children:
            full_key = f"{parent_key}.{child_key}"

            node_map[full_key] = count

            net.add_node(n_id=count, label=child_key, size=4, color="#d1d1d1", shape="diamond")
            net.add_edge(source=parent_id, to=count, color="#423037", width=0.4)

            count += 1