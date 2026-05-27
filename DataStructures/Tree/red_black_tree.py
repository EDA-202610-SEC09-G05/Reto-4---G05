
from DataStructures.Tree import rbt_node as rn
from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list
from DataStructures.Map import map_linear_probing
from DataStructures.Map import map_separate_chaining
from DataStructures.List import single_linked_list as sl


def new_map():
    rbt = {
        'root': None,
        'type': 'RBT'
    }
    return rbt

def default_compare(key, element):
    if key == element['key']:
        return 0
    elif key > element['key']:
        return 1
    else:
        return -1

    
def is_red(node_rbt):
    if node_rbt is None:
        return False
    return node_rbt['color'] == rn.RED

def size_tree(root):
    if root is None:
        return 0
    return root['size']

def rotate_left(node_rbt):
    x = node_rbt['right']
    node_rbt['right'] = x['left']
    x['left'] = node_rbt

    x['color'] = node_rbt['color']
    node_rbt['color'] = rn.RED

    x['size'] = node_rbt['size']
    node_rbt['size'] = 1 + size_tree(node_rbt['left']) + size_tree(node_rbt['right'])

    return x

def rotate_right(node_rbt):
    x = node_rbt['left']
    node_rbt['left'] = x['right']
    x['right'] = node_rbt

    x['color'] = node_rbt['color']
    node_rbt['color'] = rn.RED

    x['size'] = node_rbt['size']
    node_rbt['size'] = 1 + size_tree(node_rbt['left']) + size_tree(node_rbt['right'])

    return x

def flip_node_color(node_rbt):
    if node_rbt['color'] == rn.RED:
        node_rbt['color'] = rn.BLACK
    else:
        node_rbt['color'] = rn.RED
    return node_rbt


def flip_colors(node_rbt):
    flip_node_color(node_rbt)
    flip_node_color(node_rbt['left'])
    flip_node_color(node_rbt['right'])
    return node_rbt

def insert_node(root, key, value, repeated=False):
    if root is None:
        if repeated:
            return rn.new_node(key, [value])
        return rn.new_node(key, value)

    cmp = default_compare(key, root)

    if cmp == 0:
        if repeated:
            if isinstance(root['value'], list):
                root['value'].append(value)
            else:
                root['value'] = [root['value'], value]
        else:
            root['value'] = value
    elif cmp < 0:
        root['left'] = insert_node(root['left'], key, value, repeated)
    else:
        root['right'] = insert_node(root['right'], key, value, repeated)

    if is_red(root['right']) and not is_red(root['left']):
        root = rotate_left(root)

    if is_red(root['left']) and is_red(root['left']['left']):
        root = rotate_right(root)

    if is_red(root['left']) and is_red(root['right']):
        root = flip_colors(root)

    root['size'] = 1 + size_tree(root['left']) + size_tree(root['right'])
    return root

def put(my_rbt, key, value, repeated=False):
    my_rbt['root'] = insert_node(my_rbt['root'], key, value, repeated)
    my_rbt['root']['color'] = rn.BLACK
    return my_rbt


def get_node(root, key):
    if root is None:
        return None

    cmp = default_compare(key, root)

    if cmp == 0:
        return root['value']
    elif cmp < 0:
        return get_node(root['left'], key)
    else:
        return get_node(root['right'], key)


def get(my_rbt, key):
    return get_node(my_rbt['root'], key)


def contains(my_rbt, key):
    return get(my_rbt, key) is not None


def size(my_rbt):
    return size_tree(my_rbt['root'])


def is_empty(my_rbt):
    return my_rbt['root'] is None

def key_set_tree(root, key_list):
    if root is None:
        return
    key_set_tree(root['left'], key_list)
    al.add_last(key_list, root['key'])
    key_set_tree(root['right'], key_list)

    

def key_set(my_rbt):
    keys = al.new_list()
    key_set_tree(my_rbt['root'], keys)
    return keys

def value_set_tree(root, value_list):
    if root is None:
        return
    value_set_tree(root['left'], value_list)
    al.add_last(value_list, root['value'])
    value_set_tree(root['right'], value_list)
    
    
def value_set(my_rbt):
    values = al.new_list()
    value_set_tree(my_rbt['root'], values)
    return values

def get_min_node(root):
    if root['left'] is None:
        return root
    return get_min_node(root['left'])


def get_min(my_rbt):
    if my_rbt['root'] is None:
        return None
    return get_min_node(my_rbt['root'])['key']

def get_max_node(root):
    if root['right'] is None:
        return root
    return get_max_node(root['right'])

def get_max(my_rbt):
    if my_rbt['root'] is None:
        return None
    return get_max_node(my_rbt['root'])['key']


def height_tree(root):
    if root is None:
        return -1
    return 1 + max(height_tree(root['left']),
                   height_tree(root['right']))


def height(my_rbt):
    return height_tree(my_rbt['root'])

def keys_range(root, key_initial, key_final, list_key):
    if root is None:
        return

    if key_initial < root['key']:
        keys_range(root['left'], key_initial, key_final, list_key)

    if key_initial <= root['key'] <= key_final:
        list_key.append(root['key'])

    if key_final > root['key']:
        keys_range(root['right'], key_initial, key_final, list_key)

def keys(my_rbt, key_initial, key_final):
    result = []
    keys_range(my_rbt['root'], key_initial, key_final, result)
    return result

def values_range(root, key_initial, key_final, value_list):
    if root is None:
        return

    if key_initial < root['key']:
        values_range(root['left'], key_initial, key_final, value_list)

    if key_initial <= root['key'] <= key_final:
        value_list.append(root['value'])

    if key_final > root['key']:
        values_range(root['right'], key_initial, key_final, value_list)
        

def values(my_rbt, key_initial, key_final):
    result = []
    values_range(my_rbt['root'], key_initial, key_final, result)
    return result