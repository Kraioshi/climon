def build_tree(keys: list[str]):
    tree: dict = {}

    for key in keys:
        parts = key.split(".")
        current_node = tree
        for part in parts:
            if part not in current_node:
                current_node[part] = {}

            current_node = current_node[part]

    return tree