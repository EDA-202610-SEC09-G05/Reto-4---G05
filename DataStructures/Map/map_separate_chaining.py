from DataStructures.List import array_list as al
from DataStructures.List import single_linked_list as sll
from DataStructures.Map import map_entry as me
from DataStructures.Map import map_functions as mf


def new_map(num_elements, load_factor, prime=109345121):

    capacity = int(num_elements / load_factor)
    if capacity < 1:
        capacity = 1

    table = al.new_list()

    for _ in range(capacity):
        al.add_last(table, sll.new_list())

    my_map = {
        "prime": prime,
        "capacity": capacity,
        "scale": 1,   # fijo para tests
        "shift": 0,   # fijo para tests
        "table": table,
        "current_factor": 0,
        "limit_factor": load_factor,
        "size": 0
    }

    return my_map



def put(my_map, key, value):

    index = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], index)

    node = bucket["first"]

    while node is not None:
        entry = node["info"]
        if me.get_key(entry) == key:
            me.set_value(entry, value)
            return my_map
        node = node["next"]

    new_entry = me.new_map_entry(key, value)
    sll.add_last(bucket, new_entry)

    my_map["size"] += 1
    my_map["current_factor"] = my_map["size"] / my_map["capacity"]

  
    if my_map["current_factor"] > my_map["limit_factor"]:
        new_map_obj = rehash(my_map)
        my_map.clear()
        my_map.update(new_map_obj)

    return my_map

def get(my_map, key):

    index = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], index)

    node = bucket["first"]

    while node is not None:
        entry = node["info"]
        if me.get_key(entry) == key:
            return me.get_value(entry)
        node = node["next"]

    return None



def contains(my_map, key):
    return get(my_map, key) is not None


def remove(my_map, key):

    index = mf.hash_value(my_map, key)
    bucket = al.get_element(my_map["table"], index)

    prev = None
    node = bucket["first"]

    while node is not None:
        entry = node["info"]

        if me.get_key(entry) == key:

            if prev is None:
                bucket["first"] = node["next"]
            else:
                prev["next"] = node["next"]

            if node == bucket["last"]:
                bucket["last"] = prev

            bucket["size"] -= 1
            my_map["size"] -= 1
            my_map["current_factor"] = my_map["size"] / my_map["capacity"]

            return my_map

        prev = node
        node = node["next"]

    return my_map



def size(my_map):
    return my_map["size"]



def is_empty(my_map):
    return my_map["size"] == 0



def key_set(my_map):

    keys = al.new_list()
    table = my_map["table"]

    for i in range(al.size(table)):
        bucket = al.get_element(table, i)
        node = bucket["first"]

        while node is not None:
            entry = node["info"]
            al.add_last(keys, me.get_key(entry))
            node = node["next"]

    return keys



def value_set(my_map):

    values = al.new_list()
    table = my_map["table"]

    for i in range(al.size(table)):
        bucket = al.get_element(table, i)
        node = bucket["first"]

        while node is not None:
            entry = node["info"]
            al.add_last(values, me.get_value(entry))
            node = node["next"]

    return values


def rehash(my_map):

    old_table = my_map["table"]
    old_capacity = my_map["capacity"]

    new_capacity = old_capacity * 2

    new_map_obj = new_map(new_capacity, my_map["limit_factor"], my_map["prime"])

    for i in range(al.size(old_table)):
        bucket = al.get_element(old_table, i)
        node = bucket["first"]

        while node is not None:
            entry = node["info"]
            put(new_map_obj, me.get_key(entry), me.get_value(entry))
            node = node["next"]

    return new_map_obj

def add_number(my_map, key, number):

    current_value = get(my_map, key)

    if current_value is None:
        return my_map

    new_value = current_value + number
    put(my_map, key, new_value)

    return my_map