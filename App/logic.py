import os
import csv
import time
import math
from datetime import datetime
from tabulate import tabulate
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Map import map_separate_chaining as mc
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import sort
from DataStructures.Graph import bfs as bfs
from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as G
from DataStructures.Graph import edge as edge
from DataStructures.Graph import dijsktra_structure as djk

 
csv.field_size_limit(2147483647)

def new_logic():

    catalog = {
        "vertices_map": mc.new_map(1000, 0.5),
        "mmsi_map": mc.new_map(5000, 0.5),
        "edges_map": mc.new_map(2000, 0.5),
        "g_distance": G.new_graph(20000),
        "g_time": G.new_graph(20000),
        "total_records": 0,
        "creation_order": al.new_list()
    }

    return catalog

def load_data(catalog, filename):

    start = get_time()
    file = open("./data/" + filename, encoding="utf-8")
    input_file = csv.DictReader(file)

    # --- LECTURA ÚNICA ---
    for row in input_file:

        record = format_record(row)

        # VÉRTICES
        load_vertex(catalog, record)

        # MMSI MAP (trayectorias)
        load_mmsi_map(catalog, record)

        catalog["total_records"] += 1

    file.close()

    # --- POST-PROCESO ---
    compute_vertex_averages(catalog)
    build_edges(catalog)
    build_graphs(catalog)

    end = get_time()

    return catalog, delta_time(start, end)

def format_record(row):

    return {
        "mmsi": row["MMSI"].strip(),
        "cluster": row["DEST_CLUSTER"].strip(),
        "lat": float(row["LAT"]),
        "lon": float(row["LON"]),
        "sog": float(row["SOG"]) if row["SOG"] != "" else 0,
        "time": row["BASEDATETIME"],
        "name": row["VESSELNAME"],
        "type": row["VESSELTYPE"],
        "cargo": row["CARGO"],
        "speed_cat": row["SPEED_CATEGORY"]
    }
    
    
def load_vertex(catalog, record):

    cid = record["cluster"]
    vertex = mc.get(catalog["vertices_map"], cid)

    if vertex is None:
        vertex = new_vertex(cid)
        mc.put(catalog["vertices_map"], cid, vertex)
        al.add_last(catalog["creation_order"], cid)

    update_vertex(vertex, record)
    
def new_vertex(cid):

    return {
        "id": cid,
        "lat_sum": 0,
        "lon_sum": 0,
        "count": 0,
        "sog_sum": 0,
        "mmsi": al.new_list(),
        "names": al.new_list()
    }

def update_vertex(v, record):

    v["lat_sum"] += record["lat"]
    v["lon_sum"] += record["lon"]
    v["sog_sum"] += record["sog"]
    v["count"] += 1

    al.add_last(v["mmsi"], record["mmsi"])
    al.add_last(v["names"], record["name"])
    
def compute_vertex_averages(catalog):

    keys = mc.key_set(catalog["vertices_map"])

    for i in range(al.size(keys)):

        cid = al.get_element(keys, i)
        v = mc.get(catalog["vertices_map"], cid)  

        v["lat"] = v["lat_sum"] / v["count"]
        v["lon"] = v["lon_sum"] / v["count"]
        v["avg_sog"] = round(v["sog_sum"] / v["count"], 2)
        
def load_mmsi_map(catalog, record):

    mmsi = record["mmsi"]
    lst = mc.get(catalog["mmsi_map"], mmsi)

    if lst is None:
        lst = al.new_list()
        mc.put(catalog["mmsi_map"], mmsi, lst)

    al.add_last(lst, record)

    
def build_edges(catalog):

    keys = mc.key_set(catalog["mmsi_map"])

    for i in range(al.size(keys)):

        mmsi = al.get_element(keys, i)
        records = mc.get(catalog["mmsi_map"], mmsi)

        sort.merge_sort(records, compare_time, al)

        for j in range(al.size(records) - 1):

            a = al.get_element(records, j)
            b = al.get_element(records, j + 1)

            if a["cluster"] != b["cluster"]:
                add_edge_info(catalog, a, b)
                
def compare_time(a, b):
    return a["time"] < b["time"]

def add_edge_info(catalog, a, b):

    source = a["cluster"]
    target = b["cluster"]

    v1 = mc.get(catalog["vertices_map"], source)
    v2 = mc.get(catalog["vertices_map"], target)

    if v1 is None or v2 is None:
        return

    key = source + "-" + target
    edge = mc.get(catalog["edges_map"], key)

    if edge is None:

        dist = haversine(v1["lat"], v1["lon"], v2["lat"], v2["lon"])

        edge = {
            "source": source,
            "target": target,
            "distance": dist,
            "count": 0,
            "time_sum": 0
        }

        mc.put(catalog["edges_map"], key, edge)

    time = time_diff(a["time"], b["time"])

    edge["count"] += 1
    edge["time_sum"] += time
    
def haversine(lat1, lon1, lat2, lon2):

    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)

    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    return R * c

def time_diff(t1, t2):

    fmt = "%Y-%m-%d %H:%M:%S"

    d1 = datetime.strptime(t1, fmt)
    d2 = datetime.strptime(t2, fmt)

    return (d2 - d1).total_seconds()

def build_graphs(catalog):

    keys = mc.key_set(catalog["vertices_map"])

    for i in range(al.size(keys)):
        vid = al.get_element(keys, i)

        if not G.contains_vertex(catalog["g_distance"], vid):
            G.insert_vertex(catalog["g_distance"], vid, None)

        if not G.contains_vertex(catalog["g_time"], vid):
            G.insert_vertex(catalog["g_time"], vid, None)

    ekeys = mc.key_set(catalog["edges_map"])

    for i in range(al.size(ekeys)):

        key = al.get_element(ekeys, i)
        e = mc.get(catalog["edges_map"], key)

        source = e["source"]
        target = e["target"]

        if not G.contains_vertex(catalog["g_distance"], source):
            continue
        if not G.contains_vertex(catalog["g_distance"], target):
            continue

        avg_time = e["time_sum"] / e["count"]

        G.add_edge(catalog["g_distance"], source, target, e["distance"])
        G.add_edge(catalog["g_time"], source, target, avg_time)

def get_first_3_mmsi(lst):

    result = []
    size = al.size(lst)

    limit = 3 if size >= 3 else size

    for i in range(limit):
        result.append(str(al.get_element(lst, i)))

    return ", ".join(result)


def req_1(catalog):

    origen_id = catalog["req1_origen"]
    destino_id = catalog["req1_destino"]

    info_origen = mc.get(catalog["vertices_map"], origen_id)
    info_destino = mc.get(catalog["vertices_map"], destino_id)

    if info_origen is None:
        return {"error": f"La zona de origen '{origen_id}' no existe"}

    if info_destino is None:
        return {"error": f"La zona de destino '{destino_id}' no existe"}

    if origen_id == destino_id:
        return {"error": "El origen y el destino son la misma zona"}

    # BFS manual: menor número de arcos
    visitados = {origen_id: None}  # vertice: predecesor
    cola = [origen_id]
    encontrado = False

    while cola:
        actual = cola.pop(0)

        if actual == destino_id:
            encontrado = True
            break

        adyacentes = G.adjacents(catalog["g_distance"], actual)
        total = al.size(adyacentes)

        for i in range(total):
            vecino = al.get_element(adyacentes, i)
            if vecino not in visitados:
                visitados[vecino] = actual
                cola.append(vecino)

    if not encontrado:
        return {
            "existe_trayectoria": False,
            "mensaje": f"No existe trayectoria entre '{origen_id}' y '{destino_id}'"
        }

    # Reconstruir camino
    camino = []
    actual = destino_id
    while actual is not None:
        camino.append(actual)
        actual = visitados[actual]
    camino.reverse()

    total_zonas = len(camino)

    if total_zonas <= 10:
        indices = list(range(total_zonas))
    else:
        indices = list(range(5)) + list(range(total_zonas - 5, total_zonas))

    vertices_mostrar = al.new_list()
    for i in indices:
        vid = camino[i]
        al.add_last(vertices_mostrar, _info_vertice_req1(catalog, vid))

    return {
        "existe_trayectoria": True,
        "origen": origen_id,
        "destino": destino_id,
        "total_zonas": total_zonas,
        "total_arcos": total_zonas - 1,
        "vertices": vertices_mostrar
    }


def _info_vertice_req1(catalog, vid):

    v = mc.get(catalog["vertices_map"], vid)

    if v is None:
        return {
            "id": vid,
            "lat": "Unknown",
            "lon": "Unknown",
            "num_embarcaciones": "Unknown",
            "nombres": "Unknown"
        }

    names_lst = v.get("names", al.new_list())
    mmsi_lst = v.get("mmsi", al.new_list())
    total_nombres = al.size(names_lst)

    nombres_mostrar = []
    if total_nombres <= 6:
        for i in range(total_nombres):
            nombres_mostrar.append(str(al.get_element(names_lst, i)))
    else:
        for i in range(3):
            nombres_mostrar.append(str(al.get_element(names_lst, i)))
        for i in range(total_nombres - 3, total_nombres):
            nombres_mostrar.append(str(al.get_element(names_lst, i)))

    mmsi_unicos = set()
    for i in range(al.size(mmsi_lst)):
        mmsi_unicos.add(al.get_element(mmsi_lst, i))

    return {
        "id": vid,
        "lat": v.get("lat", "Unknown"),
        "lon": v.get("lon", "Unknown"),
        "num_embarcaciones": len(mmsi_unicos),
        "nombres": ", ".join(nombres_mostrar) if nombres_mostrar else "Unknown"
    }

def req_2(catalog, cluster_id, radio):

    graph = catalog["g_distance"]

    if not G.contains_vertex(graph, cluster_id):
        return {"error": f"La zona '{cluster_id}' no existe"}

    info_central = mc.get(catalog["vertices_map"], cluster_id)

    lat_base = info_central["lat"]
    lon_base = info_central["lon"]

    keys = mc.key_set(catalog["vertices_map"])

    respuesta = al.new_list()

    for i in range(al.size(keys)):

        vid = al.get_element(keys, i)  

        if not G.contains_vertex(graph, vid):
            continue

        info = mc.get(catalog["vertices_map"], vid)

        if info is not None:

            dist = haversine(lat_base, lon_base, info["lat"], info["lon"])

            if dist <= radio:

                dato = {
                    "id": vid,
                    "lat": info["lat"],
                    "lon": info["lon"],
                    "reg": info["count"],
                    "vel": info["avg_sog"],
                    "distancia": round(dist, 2)
                }

                al.add_last(respuesta, dato)

    sort.merge_sort(respuesta, comparar_req2, al)

    return {
        "zona_origen": cluster_id,
        "radio": radio,
        "total_zonas": al.size(respuesta),
        "zonas": respuesta
    }


def comparar_req2(a, b):

    if a["distancia"] != b["distancia"]:
        return a["distancia"] < b["distancia"]

    return str(a["id"]) < str(b["id"])


def req_3(catalog, n):
    """
    Retorna el resultado del requerimiento 3
    """
    mapa_arcos = catalog["edges_map"]
    lista_arcos = mc.value_set(mapa_arcos) 

    sort.merge_sort(lista_arcos, comparar_arcos_req3, al)

    salida = al.new_list()
    cantidad_total = al.size(lista_arcos)
    if cantidad_total < n:
        limite = cantidad_total
    else:
        limite = n
    for indice in range(limite):
        arco_actual = al.get_element(lista_arcos, indice)
        distancia_arco = arco_actual["distance"]
        
        if arco_actual["count"] > 0:
            tiempo_arco = round(arco_actual["time_sum"] / arco_actual["count"], 2)
        else:
            tiempo_arco = 0

        # --- Cálculo artesanal de la distancia ---
        if distancia_arco is not None:
            distancia_final = round(distancia_arco, 2)
        else:
            distancia_final = "Unknown"
            
        datos = {
            "origen": arco_actual["source"],
            "destino": arco_actual["target"],
            "cantidad_viajes": arco_actual["count"], # En build_edges usaste "count"
            "distancia": distancia_final,
            "tiempo_promedio": tiempo_arco
        }
        al.add_last(salida, datos)
        
    return salida

def comparar_arcos_req3(dato_1, dato_2):

    if dato_1["trips_count"] != dato_2["trips_count"]:
        return dato_1["trips_count"] > dato_2["trips_count"]

    if dato_1["source"] != dato_2["source"]:
        return dato_1["source"] < dato_2["source"]

    return dato_1["target"] < dato_2["target"]


def req_4(catalog):

    origen_id = catalog["req4_origen"]

    info_origen = mc.get(catalog["vertices_map"], origen_id)

    if info_origen is None:
        return {"error": f"La zona '{origen_id}' no existe"}

    visited_map = djk.dijkstra(catalog["g_distance"], origen_id)

    arcos = al.new_list()
    costo_total = 0

    vertices_list = mp.key_set(visited_map)

    for i in range(al.size(vertices_list)):
        vid = al.get_element(vertices_list, i)
        data = mp.get(visited_map, vid)

        if data is None:
            continue

        edge_from = data.get("edge_from")
        dist_to = data.get("dist_to", float("inf"))

        if edge_from is not None and dist_to != float("inf"):

            data_from = mp.get(visited_map, edge_from)
            peso = dist_to - data_from.get("dist_to", 0)

            arco = {
                "origen": edge_from,
                "destino": vid,
                "peso": round(peso, 2)
            }

            al.add_last(arcos, arco)
            costo_total += peso

    sort.merge_sort(arcos, comparar_arcos_req4, al)

    total_arcos = al.size(arcos)
    total_zonas = total_arcos + 1

    if total_arcos <= 10:
        indices = list(range(total_arcos))
    else:
        indices = list(range(5)) + list(range(total_arcos - 5, total_arcos))

    arcos_mostrar = al.new_list()
    for i in indices:
        al.add_last(arcos_mostrar, al.get_element(arcos, i))

    return {
        "origen": origen_id,
        "costo_total": round(costo_total, 2),
        "total_zonas": total_zonas,
        "total_arcos": total_arcos,
        "arcos": arcos_mostrar
    }


def comparar_arcos_req4(a, b):
    if str(a["origen"]) != str(b["origen"]):
        return str(a["origen"]) < str(b["origen"])
    return str(a["destino"]) < str(b["destino"])


def req_5(catalog, origen, destino):

    graph = catalog["g_distance"]

    if not G.contains_vertex(graph, origen):
        return {"error": "Origen no existe"}

    if not G.contains_vertex(graph, destino):
        return {"error": "Destino no existe"}

    search = bfs.dijkstra(graph, origen)

    if not bfs.has_path_to(destino, search):
        return {
            "existe_ruta": False
        }

    costo = bfs.dist_to(destino, search)
    path = bfs.path_to(destino, search)

    ruta = al.new_list()

    pos = al.size(path) - 1
    while pos >= 0:
        al.add_last(ruta, al.get_element(path, pos))
        pos -= 1

    return {
        "existe_ruta": True,
        "costo": round(costo, 2),
        "total": al.size(ruta),
        "ruta": ruta
    }



def construir_info_vertice_req5(catalog, ruta, posicion, total):
    identificador = al.get_element(ruta, posicion)
    # Cambiado mp por mc y corregido el nombre de las llaves internas según tu new_vertex
    info_vertice = mc.get(catalog["vertices_map"], identificador)
    cantidad_embarcaciones = al.size(info_vertice["mmsi"]) # En new_vertex usaste "mmsi"
    if posicion == total - 1:
        peso_siguiente = "N/A (destino final)"
    else:
        siguiente = al.get_element(ruta, posicion + 1)
        llave_arco = identificador + "-" + siguiente
        # Cambiado mp por mc y "edge_info_map" por "edges_map"
        informacion_arco = mc.get(catalog["edges_map"], llave_arco)
        if informacion_arco:
            peso_siguiente = round(informacion_arco["distance"], 2)
        else:
            peso_siguiente = "Unknown"
    if "lat" in info_vertice:
        latitud = info_vertice["lat"]
    else:
        latitud = "Unknown"
    if "lon" in info_vertice:
        longitud = info_vertice["lon"]
    else:
        longitud = "Unknown"
    return {
        "id": identificador,
        "lat": latitud,
        "lon": longitud,
        "num_embarcaciones": cantidad_embarcaciones,
        "peso_arco_sig": peso_siguiente
    }

def req_6(catalog):

    graph = catalog["g_distance"]
    vertices_keys = mc.key_set(catalog["vertices_map"])
    total = al.size(vertices_keys)

    # --- Paso 1: construir grafo no dirigido (solo arcos bidireccionales) ---
    # grafo_nd: vid -> array_list de vecinos bidireccionales
    grafo_nd = mc.new_map(total * 2, 0.5)

    for i in range(total):
        vid = al.get_element(vertices_keys, i)
        if not mc.contains(grafo_nd, vid):
            mc.put(grafo_nd, vid, al.new_list())

    for i in range(total):
        a = al.get_element(vertices_keys, i)

        if not G.contains_vertex(graph, a):
            continue

        adyacentes_a = G.adjacents(graph, a)  # retorna array_list de keys

        if adyacentes_a is None:
            continue

        for j in range(al.size(adyacentes_a)):
            b = al.get_element(adyacentes_a, j)

            if not G.contains_vertex(graph, b):
                continue

            # Verificar si existe B->A
            adyacentes_b = G.adjacents(graph, b)
            tiene_regreso = False

            if adyacentes_b is not None:
                for k in range(al.size(adyacentes_b)):
                    if al.get_element(adyacentes_b, k) == a:
                        tiene_regreso = True
                        break

            if tiene_regreso:
                lista_a = mc.get(grafo_nd, a)
                if lista_a is None:
                    lista_a = al.new_list()
                    mc.put(grafo_nd, a, lista_a)
                al.add_last(lista_a, b)

                lista_b = mc.get(grafo_nd, b)
                if lista_b is None:
                    lista_b = al.new_list()
                    mc.put(grafo_nd, b, lista_b)
                al.add_last(lista_b, a)

    # --- Paso 2: BFS sobre grafo no dirigido ---
    visitados = mc.new_map(total * 2, 0.5)
    componentes = al.new_list()

    for i in range(total):
        v = al.get_element(vertices_keys, i)

        if mc.get(visitados, v) is not None:
            continue

        cola = al.new_list()
        al.add_last(cola, v)
        mc.put(visitados, v, True)

        nodos = al.new_list()
        suma_vel = 0.0
        suma_reg = 0

        while al.size(cola) > 0:

            actual = al.get_element(cola, 0)

            nueva = al.new_list()
            for k in range(1, al.size(cola)):
                al.add_last(nueva, al.get_element(cola, k))
            cola = nueva

            al.add_last(nodos, actual)

            info = mc.get(catalog["vertices_map"], actual)
            if info is not None:
                suma_vel += info.get("avg_sog", 0)
                suma_reg += info.get("count", 0)

            vecinos = mc.get(grafo_nd, actual)
            if vecinos is None:
                continue

            for j in range(al.size(vecinos)):
                vecino = al.get_element(vecinos, j)
                if mc.get(visitados, vecino) is None:
                    mc.put(visitados, vecino, True)
                    al.add_last(cola, vecino)

        sort.merge_sort(nodos, comparar_ids_ascendente, al)

        size_nodos = al.size(nodos)
        if size_nodos > 0:
            promedio = round(suma_vel / size_nodos, 2)
        else:
            promedio = "Unknown"    
        if size_nodos > 0:
            min_id = al.get_element(nodos, 0)
        else:
            min_id = "0"
        comp = {
            "total_zonas": size_nodos,
            "nodos": nodos,
            "total_viajes": suma_reg,
            "velocidad_promedio": promedio,
            "min_id": min_id
        }

        al.add_last(componentes, comp)

    sort.merge_sort(componentes, comparar_req6, al)

    # --- Paso 3: respuesta ---
    respuesta = al.new_list()
    limite = min(5, al.size(componentes))

    for i in range(limite):
        c = al.get_element(componentes, i)
        al.add_last(respuesta, {
            "subred_id": i + 1,
            "total_subredes": al.size(componentes),
            "total_zonas": c["total_zonas"],
            "zonas_ids": c["nodos"],
            "total_viajes": c["total_viajes"],
            "velocidad_promedio": c["velocidad_promedio"]
        })

    return respuesta


def comparar_req6(a, b):

    if a["total_zonas"] != b["total_zonas"]:
        return a["total_zonas"] > b["total_zonas"]

    return str(a["min_id"]) < str(b["min_id"])


def comparar_ids_ascendente(valor_1, valor_2):

    return int(valor_1) < int(valor_2)


def comparar_subredes(red_1, red_2):

    if red_1["total_zonas"] != red_2["total_zonas"]:
        return red_1["total_zonas"] > red_2["total_zonas"]

    return red_1["min_vertex_id"] < red_2["min_vertex_id"]


def crear_grafo_no_dirigido(grafo_original, vertices, total, catalog):

    nuevo_grafo = G.new_graph(total)

    for indice in range(total):

        codigo = al.get_element(vertices, indice)

        informacion = mp.get(catalog["vertices_map"], codigo)

        G.insert_vertex(nuevo_grafo, codigo, informacion)

    for indice in range(total):

        vertice_actual = al.get_element(vertices, indice)
        lista_adyacentes = G.edges_vertex(grafo_original, vertice_actual)
        tamano_ady = al.size(lista_adyacentes)
       
        for pos in range(tamano_ady):
            arco_actual = al.get_element(lista_adyacentes, pos)
            vecino = edge.to(arco_actual)
            
            if vertice_actual != vecino:
                conexiones_regreso = G.edges_vertex(grafo_original, vecino)
                encontrado = False
                cantidad_regresos = al.size(conexiones_regreso)
                
                for k in range(cantidad_regresos):
                    arco_retorno = al.get_element(conexiones_regreso, k)
                    destino_retorno = edge.to(arco_retorno)
                    if destino_retorno == vertice_actual:
                        encontrado = True
                        break
                if encontrado == True:
                    G.add_edge(nuevo_grafo, vertice_actual, vecino, 1.0)
                    G.add_edge(nuevo_grafo, vecino, vertice_actual, 1.0)

    return nuevo_grafo


def procesar_subred(vertices, total_vertices, mapa_recorrido, mapa_visitados, catalog):

    lista_ids = al.new_list()
    acumulado_viajes = 0
    acumulado_velocidad = 0.0
    viajes_correctos = True
    velocidades_correctas = True

    for indice in range(total_vertices):
        id_actual = al.get_element(vertices, indice)
        if mp.contains(mapa_recorrido, id_actual):
            mp.put(mapa_visitados, id_actual, True)
            al.add_last(lista_ids, id_actual)
            info_actual = mp.get(catalog["vertices_map"], id_actual)
            if info_actual != None:
                if "records_count" in info_actual:
                    if info_actual["records_count"] != None:
                        acumulado_viajes += info_actual["records_count"]
                    else:
                        viajes_correctos = False
                else:
                    viajes_correctos = False
                if "avg_sog" in info_actual:
                    if info_actual["avg_sog"] != None:
                        acumulado_velocidad += info_actual["avg_sog"]
                    else:
                        velocidades_correctas = False
                else:
                    velocidades_correctas = False
            else:
                viajes_correctos = False
                velocidades_correctas = False

    al.merge_sort(lista_ids, comparar_ids_ascendente)
    cantidad_zonas = al.size(lista_ids)
    if cantidad_zonas > 0 and velocidades_correctas == True:
        promedio = round(acumulado_velocidad / cantidad_zonas, 2)
    else:
        promedio = "Unknown"
    if viajes_correctos == False:
        acumulado_viajes = "Unknown"
    if cantidad_zonas > 0:
        menor_id = int(al.get_element(lista_ids, 0))
    else:
        menor_id = float('inf')
    return {
        "total_zonas": cantidad_zonas,
        "nodos": lista_ids,
        "total_viajes": acumulado_viajes,
        "velocidad_promedio": promedio,
        "min_vertex_id": menor_id
    }

# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
