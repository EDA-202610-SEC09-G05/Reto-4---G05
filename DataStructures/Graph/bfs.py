from DataStructures.Map import map_linear_probing as map
from DataStructures.Graph import digraph as G
from DataStructures.List import single_linked_list as lt

def dijkstra(my_graph, source):
    """
    Calcula los caminos más cortos desde un vértice origen 'source' 
    a todos los demás vértices habitables usando el algoritmo de Dijkstra.
    Retorna un mapa con los resultados.
    """
    # 1. Creamos el mapa de resultados (visited_map)
    visited_map = map.new_map(
        num_elements=G.order(my_graph),
        load_factor=0.5
    )
    
    # 2. Inicializamos todos los vértices del grafo usando indexación posicional
    vertices_list = G.vertices(my_graph)
    total_vertices = lt.size(vertices_list)
    
    pos = 0
    while pos < total_vertices:
        vertex = lt.get_element(vertices_list, pos)
        if vertex == source:
            map.put(visited_map, vertex, {"edge_from": None, "dist_to": 0})
        else:
            map.put(visited_map, vertex, {"edge_from": None, "dist_to": float('inf')})
        pos += 1
            
    # 3. Estructura para controlar los vértices pendientes por procesar
    pending = map.new_map(num_elements=G.order(my_graph), load_factor=0.5)
    
    pos_p = 0
    while pos_p < total_vertices:
        v = lt.get_element(vertices_list, pos_p)
        map.put(pending, v, True)
        pos_p += 1

    # 4. Bucle principal del algoritmo
    while map.size(pending) > 0:
        current_vertex = None
        min_dist = float('inf')
        
        # En lugar de usar map.keys(), recorremos la lista de vértices completa
        # y filtramos usando map.contains para ver cuáles siguen pendientes
        pos_k = 0
        while pos_k < total_vertices:
            v = lt.get_element(vertices_list, pos_k)
            
            # Si el vértice todavía está en el mapa de pendientes...
            if map.contains(pending, v):
                v_info = map.get(visited_map, v)['value']
                if v_info['dist_to'] < min_dist:
                    min_dist = v_info['dist_to']
                    current_vertex = v
            pos_k += 1
                
        # Si la distancia mínima es infinito, los vértices restantes son inalcanzables
        if current_vertex is None or min_dist == float('inf'):
            break
            
        map.remove(pending, current_vertex)
        
        # 5. Relajamos todas las aristas salientes del vértice actual
        adj_edges = G.adjacents(my_graph, current_vertex) 
        total_edges = lt.size(adj_edges)
        
        pos_e = 0
        while pos_e < total_edges:
            edge = lt.get_element(adj_edges, pos_e)
            v_destination = edge['vertex2'] 
            weight = edge['weight']
            
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

def dist_to(key_v, visited_map):
    """
    Retorna la distancia acumulada desde el origen hasta el vértice key_v.
    """
    if map.contains(visited_map, key_v):
        info = map.get(visited_map, key_v)['value']
        return info['dist_to']
    return float('inf')


def has_path_to(key_v, visited_map):
    """
    Indica si existe un camino válido hacia el vértice key_v.
    """
    if map.contains(visited_map, key_v):
        info = map.get(visited_map, key_v)['value']
        return info['dist_to'] < float('inf')
    return False


def path_to(key_v, visited_map):
    """
    Retorna el camino recorrido desde el origen hasta key_v en una lista del TAD,
    ordenada desde el origen hasta el destino.
    """
    if not has_path_to(key_v, visited_map):
        return None
        
    path_list = lt.new_list()
    current = key_v
    
    while current is not None:
        # add_first mete los elementos al inicio. Como vamos del destino al origen,
        # al meterlos al inicio quedan ordenados al revés (origen -> destino).
        lt.add_first(path_list, current)
        
        info = map.get(visited_map, current)['value']
        current = info['edge_from']
        
    return path_list