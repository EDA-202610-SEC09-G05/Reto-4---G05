from DataStructures.Tree import bst_node as bn

def default_compare(key1, key2):
    if key1 == key2:
        return 0
    elif key1 < key2:
        return -1
    else:
        return 1
    
def insert_node(root, key, value, repeated=False):
    if root is None:
        if repeated:
            return bn.new_node(key, [value])
        return bn.new_node(key, value)

    cmp = default_compare(key, root['key'])

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

    root['size'] = 1 + size_tree(root['left']) + size_tree(root['right'])
    return root

def put(my_bst, key, value, repeated=False):
    my_bst['root'] = insert_node(my_bst['root'], key, value, repeated)
    return my_bst

def get_node(root, key):
    if root is None:
        return None

    cmp = default_compare(key, root['key'])

    if cmp == 0:
        return root
    elif cmp < 0:
        return get_node(root['left'], key)
    else:
        return get_node(root['right'], key)
    
def get(my_bst, key):
    node = get_node(my_bst['root'], key)
    return node['value'] if node else None

def size_tree(root):
    if root is None:
        return 0
    return root['size']

def size(my_bst):
    return size_tree(my_bst['root'])

def contains(my_bst, key):
    return get(my_bst, key) is not None

def is_empty(my_bst):
    return my_bst['root'] is None

def key_set_tree(root, keys):
    if root is None:
        return
    key_set_tree(root['left'], keys)
    keys.append(root['key'])
    key_set_tree(root['right'], keys)

def key_set(my_bst):
    keys = []
    key_set_tree(my_bst['root'], keys)
    return keys

def value_set_tree(root, values):
    if root is None:
        return
    value_set_tree(root['left'], values)
    values.append(root['value'])
    value_set_tree(root['right'], values)

def value_set(my_bst):
    values = []
    value_set_tree(my_bst['root'], values)
    return values

def get_min_node(root):
    if root['left'] is None:
        return root
    return get_min_node(root['left'])

def get_min(my_bst):
    if my_bst['root'] is None:
        return None
    return get_min_node(my_bst['root'])['key']

def get_max_node(root):
    if root['right'] is None:
        return root
    return get_max_node(root['right'])

def get_max(my_bst):
    if my_bst['root'] is None:
        return None
    return get_max_node(my_bst['root'])['key']

def delete_min_tree(root):
    if root['left'] is None:
        return root['right']

    root['left'] = delete_min_tree(root['left'])
    root['size'] = 1 + size_tree(root['left']) + size_tree(root['right'])
    return root

def delete_min(my_bst):
    if my_bst['root'] is not None:
        my_bst['root'] = delete_min_tree(my_bst['root'])
    return my_bst

def delete_max_tree(root):
    if root['right'] is None:
        return root['left']

    root['right'] = delete_max_tree(root['right'])
    root['size'] = 1 + size_tree(root['left']) + size_tree(root['right'])
    return root

def delete_max(my_bst):
    if my_bst['root'] is not None:
        my_bst['root'] = delete_max_tree(my_bst['root'])
    return my_bst

def height_tree(root):
    if root is None:
        return -1
    return 1 + max(height_tree(root['left']), height_tree(root['right']))

def height(my_bst):
    return height_tree(my_bst['root'])

def keys_range(root, low, high, keys):
    if root is None:
        return

    if low < root['key']:
        keys_range(root['left'], low, high, keys)

    if low <= root['key'] <= high:
        keys.append(root['key'])

    if high > root['key']:
        keys_range(root['right'], low, high, keys)
        

def keys(my_bst, low, high):
    result = []
    keys_range(my_bst['root'], low, high, result)
    return result

def values_range(root, low, high, values):
    if root is None:
        return

    if low < root['key']:
        values_range(root['left'], low, high, values)

    if low <= root['key'] <= high:
        values.append(root['value'])

    if high > root['key']:
        values_range(root['right'], low, high, values)
        
def values(my_bst, low, high):
    result = []
    values_range(my_bst['root'], low, high, result)
    return result





