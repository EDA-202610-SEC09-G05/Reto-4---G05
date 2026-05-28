from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import vertex as v
from DataStructures.Graph import edge as e

def new_graph(size=17):
    graph = {
        'vertices': map.new_map(size, 0.5),
        'num_edges': 0
    }
    return graph

def insert_vertex(graph, key, value):
    if not contains_vertex(graph, key):
        vertex = v.new_vertex(key, value)
        map.put(graph['vertices'], key, vertex)
    return graph
 
 
def add_edge(graph, key_a, key_b, weight=1):

    entry_a = map.get(graph['vertices'], key_a)
    entry_b = map.get(graph['vertices'], key_b)

    if entry_a is None:
        return graph
    if entry_b is None:
        return graph

    vertex_a = entry_a.get('value')

    if vertex_a is None:
        return graph

    if 'adjacents' not in vertex_a:
        return graph

    edge = e.new_edge(key_b, weight)

    map.put(vertex_a['adjacents'], key_b, edge)

    graph['num_edges'] += 1

    return graph


 
 
def contains_vertex(graph, key):
    entry = map.get(graph['vertices'], key)
    return entry is not None
 
 
def order(graph):
    return map.size(graph['vertices'])
 
 
def size(graph):
    return graph['num_edges']
 
 
def degree(graph, key):
    entry = map.get(graph['vertices'], key)
    if entry is None:
        return 0
    vertex = entry['value']
    return map.size(vertex['adjacents'])
 
 
def adjacents(graph, key):
    entry = map.get(graph['vertices'], key)
    if entry is None:
        return []
    vertex = entry['value']
    keys_list = map.key_set(vertex['adjacents'])
    return keys_list
 
 
def vertices(graph):
    return map.key_set(graph['vertices'])
 
 
def edges_vertex(graph, key):
    entry = map.get(graph['vertices'], key)
    if entry is None:
        return []
    vertex = entry['value']
    return map.value_set(vertex['adjacents'])
 
 
def get_vertex(graph, key):
    entry = map.get(graph['vertices'], key)
    if entry is None:
        return None
    return entry['value']
 
 
def update_vertex_info(graph, key, value):
    entry = map.get(graph['vertices'], key)
    if entry is not None:
        entry['value']['value'] = value
    return graph
 
 
def get_vertex_information(graph, key):
    entry = map.get(graph['vertices'], key)
    if entry is None:
        return None
    return entry['value']['value']
 