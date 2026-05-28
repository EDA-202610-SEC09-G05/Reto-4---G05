from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import digraph as G
from DataStructures.List import single_linked_list as lt
from DataStructures.Graph import edge as edg


def dijkstra(my_graph, source):

    visited_map = map.new_map(
        num_elements=G.order(my_graph),
        load_factor=0.5
    )

    vertices_list = G.vertices(my_graph)
    total_vertices = lt.size(vertices_list)

    # inicialización
    pos = 0
    while pos < total_vertices:
        vertex = lt.get_element(vertices_list, pos)
        if vertex == source:
            map.put(visited_map, vertex, {"edge_from": None, "dist_to": 0})
        else:
            map.put(visited_map, vertex, {"edge_from": None, "dist_to": float('inf')})
        pos += 1

    pending = map.new_map(G.order(my_graph), 0.5)

    pos_p = 0
    while pos_p < total_vertices:
        v = lt.get_element(vertices_list, pos_p)
        map.put(pending, v, True)
        pos_p += 1

    while map.size(pending) > 0:

        current_vertex = None
        min_dist = float('inf')

        pos_k = 0
        while pos_k < total_vertices:
            v = lt.get_element(vertices_list, pos_k)
            if map.contains(pending, v):
                v_info = map.get(visited_map, v)['value']
                if v_info['dist_to'] < min_dist:
                    min_dist = v_info['dist_to']
                    current_vertex = v
            pos_k += 1

        if current_vertex is None or min_dist == float('inf'):
            break

        map.remove(pending, current_vertex)

        adj_edges = G.edges_vertex(my_graph, current_vertex)
        total_edges = lt.size(adj_edges)

        pos_e = 0
        while pos_e < total_edges:

            edge = lt.get_element(adj_edges, pos_e)

            v_destination = edg.to(edge)
            weight = edg.weight(edge)

            current_info = map.get(visited_map, current_vertex)['value']
            dest_info = map.get(visited_map, v_destination)['value']

            new_distance = current_info['dist_to'] + weight

            if new_distance < dest_info['dist_to']:
                map.put(visited_map, v_destination, {
                    "edge_from": current_vertex,
                    "dist_to": new_distance
                })

            pos_e += 1

    return visited_map