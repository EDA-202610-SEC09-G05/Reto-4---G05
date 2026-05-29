import sys
from tabulate import tabulate
from App import logic as l
import DataStructures.Map.map_separate_chaining as mc
import DataStructures.List.array_list as al
from tabulate import tabulate
from App import logic as l
from DataStructures.List import array_list as al
from App.logic import get_time, delta_time

def new_logic():
    """
    Se crea una instancia del controlador inicializando las estructuras del grafo y mapas.
    """
    return l.new_logic()

def load_data(control):

    numero_data = input("Ingrese el tamaño de datos (20, 40, 60, 80, 100): ")

    while numero_data not in ["20", "40", "60", "80", "100"]:
        print("Valor inválido")
        numero_data = input("Ingrese el tamaño de datos (20, 40, 60, 80, 100): ")

    filename = f"ais_maritime_traffic_{numero_data}pct.csv"

    catalog, tiempo = l.load_data(control, filename)

    total_vertices = l.G.order(catalog["g_distance"])
    total_edges = l.G.size(catalog["g_distance"])
    total_mmsi = l.mc.size(catalog["mmsi_map"])

    reporte = [
        ["Total de embarcaciones reconocidas", total_mmsi],
        ["Total de registros cargados", catalog["total_records"]],
        ["Total de vertices del grafo", total_vertices],
        ["Total de arcos del grafo de distancia", total_edges],
        ["Tiempo de ejecución (ms)", round(tiempo, 2)]
    ]

    print("\nReporte de la carga de datos:\n")
    print(tabulate(reporte, headers=["Metrica", "Valor"], tablefmt="grid"))

    print("\nPrimeros y últimos vértices creados:")

    show_vertices(catalog, 0, 5)

    size = l.al.size(catalog["creation_order"])
    show_vertices(catalog, size - 5, size)

    return catalog



def show_vertices(catalog, start, end):

    data = []
    order = catalog["creation_order"]

    for i in range(start, end):

        vid = l.al.get_element(order, i)
        v = mc.get(catalog["vertices_map"], vid)

        data.append({
            "ID": v["id"],
            "Lat": v["lat"],             
            "Lon": v["lon"],                 
            "Reg.": v["count"],             
            "Vel.": v["avg_sog"],           
            "3 MMSI": l.get_first_3_mmsi(v["mmsi"])  
        })

    print(tabulate(data, headers="keys", tablefmt="grid", floatfmt=".15f"))


def print_data(control, id_zona):

    entry = mc.get(control["vertices_map"], id_zona)

    if entry is None:
        print("Zona no encontrada")
        return

    v = entry["value"]

    info = [
        ["ID", v["id"]],
        ["Lat", v.get("lat")],
        ["Lon", v.get("lon")],
        ["Total registros", v["count"]],
        ["Velocidad promedio", v.get("avg_sog")],
        ["# embarcaciones", l.al.size(v["mmsi"])]
    ]

    print(tabulate(info, headers=["Campo", "Valor"], tablefmt="fancy_grid"))


def print_req_1(control):
    
    origen = input("Ingrese el ID de la zona de origen: ").strip()
    destino = input("Ingrese el ID de la zona de destino: ").strip()

    control["req1_origen"] = origen
    control["req1_destino"] = destino

    resultado = l.req_1(control)

    print("\n========== REQ 1: TRAYECTORIA ENTRE ZONAS ==========\n")

    if "error" in resultado:
        print(resultado["error"])
        return

    if not resultado["existe_trayectoria"]:
        print(resultado["mensaje"])
        return

    print(f"Zona origen:   {resultado['origen']}")
    print(f"Zona destino:  {resultado['destino']}")
    print(f"Total zonas:   {resultado['total_zonas']}")
    print(f"Total arcos:   {resultado['total_arcos']}")

    vertices = resultado["vertices"]
    data = []

    for i in range(al.size(vertices)):
        v = al.get_element(vertices, i)
        data.append({
            "ID Zona":         v["id"],
            "Lat":             v["lat"],
            "Lon":             v["lon"],
            "# Embarcaciones": v["num_embarcaciones"],
            "Nombres":         v["nombres"]
        })

    print(tabulate(data, headers="keys", tablefmt="grid"))
   
    pass

def print_req_2(control):

    start = l.get_time()

    cluster = input("Ingrese el identificador de la zona: ").strip()
    radio = float(input("Ingrese el radio (km): "))

    r = l.req_2(control, cluster, radio)

    end = l.get_time()

    if "error" in r:
        print("\nError:", r["error"])
        return

    print("\n" + "="*60)
    print("REQ. 2 — Área de influencia de una zona")
    print("="*60)
    print(f"Zona origen: {r['zona_origen']}")
    print(f"Radio: {r['radio']} km")
    print(f"Total zonas encontradas: {r['total_zonas']}")
    print(f"Tiempo ejecución: {round(l.delta_time(start, end), 2)} ms")
    print("="*60 + "\n")

    filas = []

    zonas = r["zonas"]

    for i in range(l.al.size(zonas)):
        z = l.al.get_element(zonas, i)

        filas.append({
            "ID": z["id"],
            "Lat": z["lat"],
            "Lon": z["lon"],
            "Registros": z["reg"],
            "Velocidad": z["vel"],
            "Distancia": z["distancia"]
        })

    print(tabulate(filas, headers="keys", tablefmt="grid", floatfmt=".5f"))


def print_req_3(control):

    n = int(input("Ingrese el número de conexiones: "))

    lista_top = l.req_3(control, n)

    print("\n========== REQ 3: CONEXIONES MÁS FRECUENTES ==========\n")

    filas = []

    for i in range(al.size(lista_top)):
        arc = al.get_element(lista_top, i)

        filas.append({
            "Origen": arc.get("origen"),
            "Destino": arc.get("destino"),
            "Viajes": arc.get("cantidad_viajes"),
            "Distancia": arc.get("distancia"),
            "Tiempo Prom": arc.get("tiempo_promedio")
        })

    print(tabulate(filas, headers="keys", tablefmt="grid"))
    
def print_req_4(control):

    origen = input("Ingrese el ID de la zona de origen: ").strip()
    control["req4_origen"] = origen

    resultado = l.req_4(control)

    print("\n========== REQ 4: RED DE NAVEGACIÓN ÓPTIMA ==========\n")

    if "error" in resultado:
        print(resultado["error"])
        return

    print(f"Zona origen:  {resultado['origen']}")
    print(f"Costo total:  {resultado['costo_total']} km")
    print(f"Total zonas:  {resultado['total_zonas']}")
    print(f"Total arcos:  {resultado['total_arcos']}")

    arcos = resultado["arcos"]
    data = []

    for i in range(al.size(arcos)):
        a = al.get_element(arcos, i)
        data.append({
            "Zona Origen":  a["origen"],
            "Zona Destino": a["destino"],
            "Peso (km)":    a["peso"]
        })

    print(tabulate(data, headers="keys", tablefmt="grid"))
    
    
def print_req_5(control):

    print("\n========== REQ 5: RUTA MÁS EFICIENTE ==========\n")

    origen = input("Identificador zona origen: ").strip()
    destino = input("Identificador zona destino: ").strip()

    start = get_time()

    r = l.req_5(control, origen, destino)

    end = get_time()

    if "error" in r:
        print("\nX", r["error"])
        return

    if not r["existe_ruta"]:
        print("\nNo existe ruta entre las zonas indicadas.")
        print("Tiempo de ejecución (ms):", round(delta_time(start, end), 2))
        return

    print("\n Existe ruta entre las zonas\n")

    print("Costo total de la ruta:", round(r["costo"], 2), "km")
    print("Total de zonas:", r["total"])
    print("Total de arcos:", r["total"] - 1)

    ruta = r["ruta"]
    total = al.size(ruta)

    if total <= 10:
        indices = list(range(total))
    else:
        indices = list(range(5)) + list(range(total - 5, total))

    tabla = []

    for i in indices:

        info = l.construir_info_vertice_req5(control, ruta, i, total)

        fila = [
            info["id"],
            round(info["lat"], 2) if isinstance(info["lat"], float) else "Unknown",
            round(info["lon"], 2) if isinstance(info["lon"], float) else "Unknown",
            info["num_embarcaciones"] if info["num_embarcaciones"] is not None else "Unknown",
            info["peso_arco_sig"]
        ]

        tabla.append(fila)

    headers = [
        "ID Zona",
        "Latitud",
        "Longitud",
        "# Embarcaciones",
        "Peso hacia siguiente (km)"
    ]

    print("\nDetalle de la ruta (primeros y últimos vértices):\n")
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

    print("\nTiempo de ejecución (ms):", round(delta_time(start, end), 2))


        
        
def print_req_6(control):

    print("\n========== REQ 6: CONECTIVIDAD BIDIRECCIONAL ==========\n")

    start = get_time()

    resultado = l.req_6(control)

    end = get_time()

    if resultado is None or al.size(resultado) == 0:
        print("No se encontraron subredes.")
        return

    total = al.get_element(resultado, 0)["total_subredes"]

    print("Total de subredes:", total)

    tabla = []

    for i in range(al.size(resultado)):
        dato = al.get_element(resultado, i)

        nodos = dato["zonas_ids"]
        total_nodos = al.size(nodos)

        mostrar = []

        if total_nodos <= 6:
            for j in range(total_nodos):
                mostrar.append(al.get_element(nodos, j))
        else:
            for j in range(3):
                mostrar.append(al.get_element(nodos, j))
            for j in range(total_nodos - 3, total_nodos):
                mostrar.append(al.get_element(nodos, j))

        fila = [
            dato["subred_id"],
            dato["total_zonas"],
            ", ".join(mostrar),
            dato["total_viajes"],
            dato["velocidad_promedio"]
        ]

        tabla.append(fila)

    headers = [
        "ID Subred",
        "Total Zonas",
        "Zonas (IDs)",
        "Total Viajes",
        "Velocidad Promedio"
    ]

    print("\nSubredes más grandes:\n")
    print(tabulate(tabla, headers=headers, tablefmt="grid"))

    print("\nTiempo de ejecución (ms):", round(delta_time(start, end), 2))
    
# Se crea la lógica asociado a la vista
control = new_logic()

def print_menu():
    print("\n========================")
    print("0. Cargar datos")
    print("1. Req 1")
    print("2. Req 2")
    print("3. Req 3")
    print("4. Req 4")
    print("5. Req 5")
    print("6. Req 6")
    print("7. Salir")
    print("========================")

def main():
    """
    Menú principal con control de errores y flujo robusto.
    """
    control = new_logic()  # Inicializamos las estructuras aquí
    working = True
    
    while working:
        print_menu()
        inputs = input('Seleccione una opción para continuar: ').strip()
        
        # Validación: solo permite números y previene el error de VS Code
        if not inputs.isdigit():
            print("Entrada inválida. Por favor, ingrese un número del 0 al 7.\n")
            continue
            
        opcion = int(inputs)
        
        if opcion == 0:
            print("Cargando información de los archivos ....\n")
            # Actualizamos 'control' con los datos cargados
            control = load_data(control)
            
        elif opcion == 1:
            print_req_1(control)
        elif opcion == 2:
            print_req_2(control)
        elif opcion == 3:
            print_req_3(control)
        elif opcion == 4:
            print_req_4(control)
        elif opcion == 5:
            print_req_5(control)
        elif opcion == 6:  # Corrección: aquí debe ir la opción 6
            print_req_6(control)
        elif opcion == 7:
            working = False
            print("\nGracias por utilizar el programa.")
        else:
            print("Opción errónea, vuelva a elegir.\n")
            
    sys.exit(0)
