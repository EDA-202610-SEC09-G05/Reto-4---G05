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

from DataStructures.List import array_list as al
from DataStructures.Graph import digraph as G
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
    entry = mc.get(catalog["vertices_map"], cid)

    if entry is None:
        vertex = new_vertex(cid)
        mc.put(catalog["vertices_map"], cid, vertex)
        al.add_last(catalog["creation_order"], cid)
    else:
        vertex = entry["value"]

    update_vertex(vertex, record)

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

        entry = mc.get(catalog["vertices_map"], cid)
        v = entry["value"]   

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

        entry = mc.get(catalog["mmsi_map"], mmsi)
        records = entry["value"]

        sort.merge_sort(records, compare_time, al)

        for j in range(al.size(records)-1):

            a = al.get_element(records, j)
            b = al.get_element(records, j+1)

            if a["cluster"] != b["cluster"]:
                add_edge_info(catalog, a, b)
                
def compare_time(a, b):
    return a["time"] < b["time"]

def add_edge_info(catalog, a, b):

    key = a["cluster"] + "-" + b["cluster"]

    edge_entry = mc.get(catalog["edges_map"], key)

    if edge_entry is None:

        v1_entry = mc.get(catalog["vertices_map"], a["cluster"])
        v2_entry = mc.get(catalog["vertices_map"], b["cluster"])

        v1 = v1_entry["value"]  
        v2 = v2_entry["value"]  

        dist = haversine(v1["lat"], v1["lon"], v2["lat"], v2["lon"])

        edge = {
            "source": a["cluster"],
            "target": b["cluster"],
            "distance": dist,
            "count": 0,
            "time_sum": 0
        }

        mc.put(catalog["edges_map"], key, edge)

    else:
        edge = edge_entry["value"]  # ✅

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

        G.insert_vertex(catalog["g_distance"], vid, vid)
        G.insert_vertex(catalog["g_time"], vid, vid)

    ekeys = mc.key_set(catalog["edges_map"])

    for i in range(al.size(ekeys)):

        k = al.get_element(ekeys, i)

        entry = mc.get(catalog["edges_map"], k)
        e = entry["value"]

        avg_time = e["time_sum"] / e["count"]

        G.add_edge(catalog["g_distance"], e["source"], e["target"], e["distance"])
        G.add_edge(catalog["g_time"], e["source"], e["target"], avg_time)
        




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
