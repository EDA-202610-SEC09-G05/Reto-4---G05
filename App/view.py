import sys
from tabulate import tabulate
from App import logic as l
import DataStructures.Map.map_separate_chaining as mc
import DataStructures.List.array_list as al
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

    # ===== RESUMEN =====
    total_vertices = l.G.order(catalog["g_distance"])
    total_edges = l.G.size(catalog["g_distance"])

    print("\n========== RESULTADOS ==========\n")
    print(f"Tiempo de carga: {round(tiempo, 2)} ms")
    print(f"Total de registros: {catalog['total_records']}")
    print(f"Total de vértices: {total_vertices}")
    print(f"Total de arcos: {total_edges}")

    # ===== PRIMEROS Y ÚLTIMOS =====
    print("\nPrimeros 5 vértices:")
    show_vertices(catalog, 0, 5)

    print("\nÚltimos 5 vértices:")
    size = l.al.size(catalog["creation_order"])
    show_vertices(catalog, size-5, size)
    
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
    catalog = control["catalog"]
    lista_top = l.req_3(catalog)
    
    # Función artesanal para formatear decimales a string
    def formatear(valor):
        # Si el valor es inválido, retorna el texto requerido
        if valor == None:
            return "Unknown"
            
        # Multiplicamos por 100 para trabajar con enteros
        temp = int(valor * 100)
        
        # Obtenemos la parte entera y la parte decimal de dos dígitos
        entero = temp // 100
        decimal = temp % 100
        
        # Convertimos a texto manualmente
        entero_str = str(entero)
        decimal_str = str(decimal)
        
        # Si el decimal es menor a 10, le ponemos el cero faltante
        if decimal < 10:
            decimal_str = "0" + decimal_str
            
        return entero_str + "." + decimal_str

    # Recorrido recursivo artesanal
    def imprimir_recursivo(i):
        # Usamos el tamaño de tu lista
        if i < al.size(lista_top):
            conexion = al.get_element(lista_top, i)
            
            # Acceso directo a los valores
            origen = conexion["source"]
            destino = conexion["target"]
            viajes = conexion["trips_count"]
            distancia = conexion["distance"]
            tiempo = conexion["avg_time"]
            
            # Impresión paso a paso
            print("Zona de origen: " + str(origen))
            print("Zona de destino: " + str(destino))
            print("Número total de viajes: " + str(viajes))
            print("Distancia: " + formatear(distancia))
            print("Tiempo promedio: " + formatear(tiempo))
            print("------------------------------")
            
            imprimir_recursivo(i + 1)
            
    imprimir_recursivo(0)
    
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

    origen = input("Origen: ")
    destino = input("Destino: ")

    r = l.req_5(control, origen, destino)

    if "error" in r:
        print(r["error"])
        return

    if not r["existe_ruta"]:
        print("\nNo existe ruta\n")
        return

    print("\nRUTA ENCONTRADA\n")
    print(f"Costo: {r['costo']}")
    print(f"Nodos: {r['total']}\n")

    for i in range(l.al.size(r["ruta"])):
        print(l.al.get_element(r["ruta"], i))
        
        
def print_req_6(control):

    start = l.get_time()

    resultado = l.req_6(control)

    end = l.get_time()

    size = l.al.size(resultado)

    if size == 0:
        print("\nNo se encontraron subredes\n")
        return

    total = l.al.get_element(resultado, 0)["total_subred"]

    print("\n" + "="*60)
    print("REQ. 6 — Subredes de navegación")
    print("="*60)
    print(f"Total de subredes: {total}")
    print(f"Tiempo ejecución: {round(l.delta_time(start, end), 2)} ms")
    print("="*60 + "\n")

    filas = []

    for i in range(size):

        r = l.al.get_element(resultado, i)
        nodos = r["zonas_ids"]

        if len(nodos) <= 6:
            ids = ", ".join(nodos)
        else:
            ids = ", ".join(nodos[:3]) + ", ..., " + ", ".join(nodos[-3:])

        filas.append({
            "Subred": r["subred_id"],
            "Zonas": r["total_zonas"],
            "IDs": ids,
            "Velocidad prom": r["velocidad_promedio"],
            "Total viajes": r["total_viajes"]
        })

    print(tabulate(filas, headers="keys", tablefmt="grid"))
    
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
