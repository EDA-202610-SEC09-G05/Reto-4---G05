from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import digraph as g
from DataStructures.List import single_linked_list as lt

 
def dfs(graph, source):
    search = {
        'source': source,
        'visited': map.new_map(g.order(graph), 0.5)
    }
   
    map.put(search['visited'], source, {'marked': True, 'edgeTo': None})
    dfs_vertex(search, graph, source)
    return search
 
 
def dfs_vertex(search, graph, vertex):
    adj_list = g.adjacents(graph, vertex)
    keys = _get_keys(adj_list)
 
    for adj_key in keys:
        visited_entry = map.get(search['visited'], adj_key)
        if visited_entry is None:
            map.put(search['visited'], adj_key, {'marked': True, 'edgeTo': vertex})
            dfs_vertex(search, graph, adj_key)
 
 
def has_path_to(search, vertex):
    entry = map.get(search['visited'], vertex)
    return entry is not None
 
 
def path_to(search, vertex):
    if not has_path_to(search, vertex):
        return None
    path = lt.new_list()
    current = vertex
    while current != search['source']:
        lt.add_first(path, current)
        entry = map.get(search['visited'], current)
        current = entry['value']['edgeTo']
    lt.add_first(path, search['source'])
    return path
 

def _get_keys(adj_list):
    if adj_list is None:
        return lt.new_list()
    if isinstance(adj_list, list):
        return adj_list
    # TAD list con campo 'elements'
    if isinstance(adj_list, dict) and 'elements' in adj_list:
        return [e for e in adj_list['elements'] if e is not None]
    # TAD SingleLinked con campo 'first'
    if isinstance(adj_list, dict) and 'first' in adj_list:
        result = lt.new_list()
        node = adj_list['first']
        while node is not None:
            lt.add_last(result, node['info'])
            node = node['next']
        return result
    return list(adj_list)
 