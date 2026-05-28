import sys
from tabulate import tabulate
from App import logic as l
import DataStructures.Map.map_linear_probing as mc

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

        entry = mc.get(catalog["vertices_map"], vid)
        v = entry["value"]

        data.append({
            "ID": v["id"],
            "Lat": round(v["lat"], 2) if v.get("lat") else "Unknown",
            "Lon": round(v["lon"], 2) if v.get("lon") else "Unknown",
            "Registros": v["count"],
            "Velocidad Prom": v.get("avg_sog"),
            "Embarcaciones": l.al.size(v["mmsi"])
        })

    print(tabulate(data, headers="keys", tablefmt="fancy_grid"))

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
    """
        Función que imprime la solución del Requerimiento 1 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 1
    pass


def print_req_2(control):
    """
        Función que imprime la solución del Requerimiento 2 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 2
    pass


def print_req_3(control):
    """
        Función que imprime la solución del Requerimiento 3 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 3
    pass


def print_req_4(control):
    """
        Función que imprime la solución del Requerimiento 4 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 4
    pass


def print_req_5(control):
    """
        Función que imprime la solución del Requerimiento 5 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 5
    pass


def print_req_6(control):
    """
        Función que imprime la solución del Requerimiento 6 en consola
    """
    # TODO: Imprimir el resultado del requerimiento 6
    pass

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
