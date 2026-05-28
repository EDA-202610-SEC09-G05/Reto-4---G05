import os
import csv
import time
import math
from datetime import datetime
from tabulate import tabulate
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Map import map_separate_chaining as mc
from DataStructures.Map import map_linear_probing as mp

from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as G
csv.field_size_limit(2147483647)

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos del Reto 4.
    Se usan mapas y grafos del paquete DataStructures.
    """
    catalog = {
        # Mapa: DEST_CLUSTER -> Diccionario con la información agregada de la zona
        "vertices_map": mc.new_map(200, 0.5), 
        
        # Mapa: MMSI -> Priority Queue (orientada a menor por BASEDATETIME)
        "mmsi_records_map": mc.new_map(500, 0.5), 
        
        # Mapa: 'A_B' (Origen_Destino) -> Diccionario con distancias, tiempos y conteos
        "edge_info_map": mc.new_map(500, 0.5),
        
        # TODO: Instanciar el grafo dirigido (G_distancia) usando tu módulo de grafos
        "G_distancia": None # ej: graph.new_directed_graph()
    }
    return catalog



# --- FUNCIONES AUXILIARES ---

def compare_by_datetime(registro_a, registro_b):
    """
    Compara dos registros para la cola de prioridad basándose en BASEDATETIME.
    Retorna negativo si A es anterior a B (orientado a menor).
    """
    formato = "%Y-%m-%dT%H:%M:%S" # Ajustar según el formato real del CSV
    fecha_a = datetime.strptime(registro_a["BASEDATETIME"], formato)
    fecha_b = datetime.strptime(registro_b["BASEDATETIME"], formato)
    return (fecha_a - fecha_b).total_seconds()

def haversine_distance(lat1, lon1, lat2, lon2):
    """Calcula la distancia Haversine en kilómetros."""
    R = 6371.0 # Radio de la Tierra en km
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def add_unique(lista, valor):
    """Añade un valor a una ArrayList solo si no existe previamente."""
    # Asume que al.contains(lista, valor) existe en tu módulo
    if valor and not al.contains(lista, valor):
        al.add_last(lista, valor)

def safe_float(value):
    return float(value) if value else 0.0

# --- LÓGICA PRINCIPAL ---

def new_logic():
    """
    Inicializa el catálogo maestro que contiene las estructuras de datos 
    para la gestión de tráfico marítimo (nodos, aristas y registros).
    """

    grafo = G.new_graph(size=2000) 

    catalog = {
        "vertices_map": mc.new_map(1000, 0.5),     
        "mmsi_records_map": mc.new_map(5000, 0.5),  
        "edge_info_map": mc.new_map(2000, 0.5),     
        "G_distancia": grafo                        
    }
    return catalog

def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    analyzer = {}
    capacity = 1000000 # revisar el numero
    load_factor = 0.5
    analyzer["vertices_map"] = mp.new_map(capacity, load_factor) #HECHO
    analyzer["mmsi_records_map"] = mp.new_map(capacity, load_factor)
    analyzer["edge_info_map"] = mp.new_map(capacity, load_factor)
    analyzer["g_distance"] = G.new_graph(capacity)  
    analyzer["g_time"] = G.new_graph(capacity) 
    analyzer["total_records"] = 0
    analyzer["total_vessels"] = 0
    analyzer["creation_orden"] = al.new_list()

    return analyzer


# Funciones para la carga de datos
def new_cluster(dest_cluster):
    cluster = {
        "id": dest_cluster,

        "lat_sum": 0.0,
        "lon_sum": 0.0,
        "sog_sum": 0.0,
        "length_sum": 0.0,
        "width_sum": 0.0,
        "draft_sum": 0.0,

        "records_count": 0,

        "mmsi_list": al.new_list(),
        "mmsi_set": mp.new_map(100, 0.5),
        "vessel_names": al.new_list(),
        "vessel_names_set": mp.new_map(100, 0.5),
        "vessel_types": al.new_list(),
        "vessel_types_set": mp.new_map(100, 0.5),
        "cargo_types": al.new_list(),
        "cargo_types_set": mp.new_map(100, 0.5),
        "speed_categories": al.new_list(),
        "speed_categories_set": mp.new_map(100, 0.5),
        "records": al.new_list(),

        "lat": None,
        "lon": None,
        "avg_sog": None,
        "avg_length": None,
        "avg_width": None,
        "avg_draft": None
    }
    return cluster

def compare_elements(element_a, element_b):
    if str(element_a).strip() == str(element_b).strip():
        return 0
    return -1

def add_record_to_cluster(cluster, record):
    cluster["lat_sum"] += float(record["LAT"])
    cluster["lon_sum"] += float(record["LON"])
    cluster["sog_sum"] += float(record["SOG"])
    
    if record["LENGTH"] != "":
        cluster["length_sum"] += float(record["LENGTH"]) 
    if record["WIDTH"] != "":
        cluster["width_sum"] += float(record["WIDTH"])
    if record["DRAFT"] != "":
        cluster["draft_sum"] += float(record["DRAFT"])
    
    cluster["records_count"] += 1

    al.add_last(cluster["records"], record)
    
    mmsi = record["MMSI"]
    if not mp.contains(cluster["mmsi_set"], mmsi):
        mp.put(cluster["mmsi_set"], mmsi, True)
        al.add_last(cluster["mmsi_list"], mmsi)
        
    vessel_name = record["VESSELNAME"]
    if not mp.contains(cluster["vessel_names_set"], vessel_name):
        mp.put(cluster["vessel_names_set"], vessel_name, True)
        al.add_last(cluster["vessel_names"], vessel_name)
    
    vessel_type = record["VESSELTYPE"]
    if not mp.contains(cluster["vessel_types_set"], vessel_type):
        mp.put(cluster["vessel_types_set"], vessel_type, True)
        al.add_last(cluster["vessel_types"], vessel_type)
    
    cargo_type = record["CARGO"]
    if not mp.contains(cluster["cargo_types_set"], cargo_type):
        mp.put(cluster["cargo_types_set"], cargo_type, True)
        al.add_last(cluster["cargo_types"], cargo_type)
    
    speed_category = record["SPEED_CATEGORY"]
    if not mp.contains(cluster["speed_categories_set"], speed_category):
        mp.put(cluster["speed_categories_set"], speed_category, True)
        al.add_last(cluster["speed_categories"], speed_category)

def calculate_cluster_averages(cluster):
    if cluster["records_count"] > 0:
        cluster["lat"] = cluster["lat_sum"] / cluster["records_count"]
        cluster["lon"] = cluster["lon_sum"] / cluster["records_count"]
        cluster["avg_sog"] = round(cluster["sog_sum"] / cluster["records_count"], 2)
        cluster["avg_length"] = round(cluster["length_sum"] / cluster["records_count"], 2)
        cluster["avg_width"] = round(cluster["width_sum"] / cluster["records_count"], 2)
        cluster["avg_draft"] = round(cluster["draft_sum"] / cluster["records_count"], 2)

def add_record_to_mmsi_map(catalog, record):
    
    mmsi = record["MMSI"]
    records_list = mp.get(catalog["mmsi_records_map"], mmsi)
    
    if records_list is None:
        records_list = al.new_list()
    mp.put(catalog["mmsi_records_map"], mmsi, records_list)
    
    al.add_last(records_list, record)

def new_edge_info(source, target, distance):
    
    edge_info = {
        "source": source,
        "target": target,
        "trips_count": 0,
        "distance": distance,
        "times" : al.new_list(),
        "trip_mmsi_list": al.new_list(),
        "trip_speed_categories": al.new_list(),
        "avg_time": None
    }
    return edge_info

def add_trip_to_edge_info(edge_info, trip_time, mmsi, speed_category):
    edge_info["trips_count"] += 1
    al.add_last(edge_info["times"], trip_time)
    al.add_last(edge_info["trip_mmsi_list"], mmsi)
    al.add_last(edge_info["trip_speed_categories"], speed_category)

def build_edges_info_map(catalog):
    mmsi_map = catalog["mmsi_records_map"]
    mmsi_keys = mp.key_set(mmsi_map)
    total_keys = al.size(mmsi_keys)
    
    for i in range(total_keys):
        mmsi = al.get_element(mmsi_keys, i)
        sort_records = mp.get(mmsi_map, mmsi)
        
        if sort_records is not None:
            total_records = al.size(sort_records)    
        for j in range(total_records-1):
            record_a = al.get_element(sort_records, j)
            record_b = al.get_element(sort_records, j+1)
            
            source = record_a["DEST_CLUSTER"].strip()
            target = record_b["DEST_CLUSTER"].strip()
            
            if source != target:
                edge_id = source + "-" + target
                trip_time = calculate_time_difference(record_a["BASEDATETIME"], record_b["BASEDATETIME"])
                speed_category = record_b["SPEED_CATEGORY"]
                
                edge_info = mp.get(catalog["edge_info_map"], edge_id)
                
                if edge_info is None:
                    source_vertex = mp.get(catalog["vertices_map"], source)
                    target_vertex = mp.get(catalog["vertices_map"], target)
                  
                    if source_vertex is not None and target_vertex is not None:
                        distance = haversine_distance(source_vertex["lat"], source_vertex["lon"], target_vertex["lat"], target_vertex["lon"])        
                        edge_info = new_edge_info(source, target, distance)
                        mp.put(catalog["edge_info_map"], edge_id, edge_info)
                    
                if edge_info is not None:
                    add_trip_to_edge_info(edge_info, trip_time, mmsi, speed_category)
                
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)*2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)*2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_earth_km = 6371
    distance = radius_earth_km * c
    return distance

def calculate_time_difference(datetime_a, datetime_b):
    date_format = "%Y-%m-%d %H:%M:%S"
    dt_a = datetime.strptime(datetime_a, date_format)
    dt_b = datetime.strptime(datetime_b, date_format)
    time_dif = dt_b - dt_a
    return time_dif.total_seconds()

def calculate_edges_avg_time(catalog):
    edge_info_map = catalog["edge_info_map"]
    edge_keys = mp.key_set(edge_info_map)
    total_edges = al.size(edge_keys)
    
    for i in range(total_edges):
        edge_id = al.get_element(edge_keys, i)
        edge_info = mp.get(edge_info_map, edge_id)
        
        if edge_info is not None:
            times = edge_info["times"]
            total_times = al.size(times)
        
            if total_times > 0:
                total = 0
                for j in range(total_times):
                    total += al.get_element(times, j)
                avg = total / total_times
                edge_info["avg_time"] = round(avg, 2)
        
def build_graphs(catalog):
    vertices_map = catalog["vertices_map"]
    vertices_keys = mp.key_set(vertices_map)
    total_vertices = al.size(vertices_keys)
    
    for i in range(total_vertices):
        vertex_id = al.get_element(vertices_keys, i)
        vertex_info = mp.get(vertices_map, vertex_id)
        
        G.insert_vertex(catalog["g_distance"], vertex_id, vertex_info)
        G.insert_vertex(catalog["g_time"], vertex_id, vertex_info)
        
    edge_info_map = catalog["edge_info_map"]
    edge_keys = mp.key_set(edge_info_map)
    total_edges = al.size(edge_keys)
    
    for i in range(total_edges):
        edge_id = al.get_element(edge_keys, i)
        edge_info = mp.get(edge_info_map, edge_id)
        
        if edge_info is not None and edge_info["avg_time"] is not None:
            source = edge_info["source"]
            target = edge_info["target"]
            distance = edge_info["distance"]
            avg_time = edge_info["avg_time"]
            G.add_edge(catalog["g_distance"], source, target, distance)
            G.add_edge(catalog["g_time"], source, target, avg_time)


data_dir = "./data/"

def load_data(catalog, filename):
    print("DEBUG: Entrando a load_data...") # PASO 1
    start_time = get_time()
    computer_file = data_dir + filename
    
    print(f"DEBUG: Abriendo archivo: {computer_file}") # PASO 2
    file = open(computer_file, encoding="utf-8")
    input_file = csv.DictReader(file)
    
    contador = 0
    for record in input_file:
        contador += 1
        if contador % 1000 == 0: # Imprime un aviso cada 1000 filas
            print(f"DEBUG: Procesando fila {contador}...")
    start_time = get_time()
    computer_file = os.path.join(data_dir, filename)
    
    # Esto te dirá en la consola si el archivo existe antes de intentar abrirlo
    if not os.path.exists(computer_file):
        print(f"¡ERROR! No se encuentra el archivo en: {os.path.abspath(computer_file)}")
        return None
    file = open(computer_file, encoding="utf-8")
    input_file = csv.DictReader(file)
    
    for record in input_file:
        cluster_id = record["DEST_CLUSTER"].strip()
        cluster = mp.get(catalog["vertices_map"], cluster_id)
        
        if cluster is None:
            cluster = new_cluster(cluster_id)
            mp.put(catalog["vertices_map"], cluster_id, cluster)
            al.add_last(catalog["creation_orden"], cluster_id)
        
        add_record_to_cluster(cluster, record)
        add_record_to_mmsi_map(catalog, record)
        catalog["total_records"] += 1
    
    file.close()
    
    vertex_keys = mp.key_set(catalog["vertices_map"])
    for i in range(al.size(vertex_keys)):
        vertex_id = al.get_element(vertex_keys, i)
        cluster = mp.get(catalog["vertices_map"], vertex_id)
        calculate_cluster_averages(cluster)
    
    build_edges_info_map(catalog)
    calculate_edges_avg_time(catalog)
    build_graphs(catalog)
    
    catalog["total_vessels"] = al.size(mp.key_set(catalog["mmsi_records_map"]))
    
    total_vertices = G.order(catalog["g_distance"])
    total_arcos = G.size(catalog["g_distance"])
    
    primeros_5 = []
    ultimos_5 = []
    
    lista_ordenada = catalog["creation_orden"]
    total = al.size(lista_ordenada)
    
    for i in range(5):
        vertex_id = al.get_element(lista_ordenada, i)
        vertex_info = mp.get(catalog["vertices_map"], vertex_id)
        primeros_5.append(vertex_info)
    
    for i in range(total - 5, total):
        vertex_id = al.get_element(lista_ordenada, i)
        vertex_info = mp.get(catalog["vertices_map"], vertex_id)
        ultimos_5.append(vertex_info)
    
    end_time = get_time()
    tiempo = delta_time(start_time, end_time)
    
    return  {
        "tiempo": tiempo,
        "total_vessels": catalog["total_vessels"],
        "total_records": catalog["total_records"],
        "total_vertices": total_vertices,
        "total_arcos": total_arcos,
        "primeros_5": primeros_5,
        "ultimos_5": ultimos_5
    }
def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    pass


def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


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
