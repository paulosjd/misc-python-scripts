import json


class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def __repr__(self):
        return str(self.data)


def serialize(root):
    if not root:
        return None

    left = serialize(root.left)
    right = serialize(root.right)

    tree_map = {'data': root.data}
    if left:
        tree_map['left'] = left
    if right:
        tree_map['right'] = right

    return json.dumps(tree_map)


def deserialize(s):
    tree_map = json.loads(s)

    node = Node(tree_map['data'])
    if 'left' in tree_map:
        node.left = deserialize(tree_map['left'])
    if 'right' in tree_map:
        node.right = deserialize(tree_map['right'])

    return node


node_a, node_b, node_c, node_d, node_e, node_f, node_g = [
    Node(s) for s in ['a', 'b', 'c', 'd', 'e', 'f', 'g']
]
node_a.left = node_b
node_a.right = node_c
node_b.left = node_d
node_b.right = node_e
node_c.left = node_f
node_c.right = node_g

serialize(node_g)
serialize(node_d)
serialized_a = serialize(node_a)
print(serialized_a)

deserialized_a = deserialize(serialized_a)
assert str(deserialized_a) == "a"
