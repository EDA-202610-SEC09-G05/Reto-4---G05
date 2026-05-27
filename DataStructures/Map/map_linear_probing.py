import random
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):

    capacity = mf.next_prime(int(num_elements / load_factor))

    table = []
    for i in range(capacity):
        table.append(me.new_map_entry(None, None))

    new_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": 1,   # fijo para que coincida con los tests
        "shift": 0,   # fijo para que coincida con los tests
        "table": {
            "elements": table,
            "size": capacity
        },
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0
    }

    return new_map

def size(my_map):
    return my_map["size"]

def is_available(table, index):

    entry = table["elements"][index]

    if entry["key"] is None:
        return True
    return False

def default_compare(key, entry):

    if entry["key"] == key:
        return True
    return False

def find_slot(my_map, key, hash_value):

    table = my_map["table"]
    elements = table["elements"]
    capacity = my_map["capacity"]

    first_available = None
    index = hash_value

    while True:

        if is_available(table, index):
            if first_available is None:
                first_available = index

            if elements[index]["key"] is None:
                return False, first_available

        elif default_compare(key, elements[index]):
            return True, index

        index = (index + 1) % capacity

def put(my_map, key, value):

    hash_pos = mf.hash_value(my_map, key)

    found, pos = find_slot(my_map, key, hash_pos)

    table = my_map["table"]["elements"]

    if found:
        table[pos]["value"] = value
    else:
        table[pos]["key"] = key
        table[pos]["value"] = value

        my_map["size"] += 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map

def contains(my_map, key):

    hash_pos = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_pos)

    return found

def get(my_map, key):

    hash_pos = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_pos)

    if found:
        return my_map["table"]["elements"][pos]["value"]

    return None

def remove(my_map, key):

    hash_pos = mf.hash_value(my_map, key)
    found, pos = find_slot(my_map, key, hash_pos)

    if found:
        my_map["table"]["elements"][pos]["key"] = None
        my_map["table"]["elements"][pos]["value"] = None

        my_map["size"] -= 1
        my_map["current_factor"] = my_map["size"] / my_map["capacity"]

    return my_map