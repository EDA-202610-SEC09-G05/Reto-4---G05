import sys
from tabulate import tabulate
import logic as l 
import DataStructures.Map.map_linear_probing as mc
from logic import print_vertice, print_menu

def new_logic():
    """
    Se crea una instancia del controlador inicializando las estructuras del grafo y mapas.
    """
    return l.new_logic()

def load_data(control):
    """
    Carga los datos
    """
    #TODO: Realizar la carga de datos
    numero_data = input("Ingrese el número de datos a cargar entre 20, 40, 60, 80, 100: ")
    while numero_data not in ["20", "40", "60", "80", "100"]:
        print("Número de datos no válido")
        numero_data = input("Ingrese el número de datos a cargar entre 20, 40, 60, 80, 100: ")
        
    input_file = f"ais_maritime_traffic_{numero_data}pct.csv"
    datos = l.load_data(control, input_file)
    
    print(f"\nTiempo de carga: {datos['tiempo']} ms")
    print(f"Total de embarcaciones: {datos['total_vessels']}")
    print(f"Total de registros: {datos['total_records']}")
    print(f"Total de vértices: {datos['total_vertices']}")
    print(f"Total de arcos: {datos['total_arcos']}")
    
    print("\nPrimeros 5 vértices:")
    primeros_5 = []
    
    for i in range(len(datos["primeros_5"])):
        vertice = datos["primeros_5"][i]
        vertice_info = print_vertice(vertice)
        primeros_5.append(vertice_info)
    print(tabulate(primeros_5, headers="keys", tablefmt="fancy_grid"))
    
    print("\nÚltimos 5 vértices:")
    ultimos_5 = []
    
    for i in range(len(datos["ultimos_5"])):
        vertice = datos["ultimos_5"][i]
        vertice_info = print_vertice(vertice)
        ultimos_5.append(vertice_info)
    print(tabulate(ultimos_5, headers="keys", tablefmt="fancy_grid"))
    
    print("\nDatos cargados exitosamente\n")

def print_data(control, id_zona):
    """
    Busca y muestra la información detallada de un vértice (zona) por su ID.
    """
    # Accedemos al mapa de vértices desde el control
    # Nota: Asegúrate de que 'vertices_map' sea el nombre de la llave en tu catálogo

    
    vertice_entry = mc.get(control["vertices_map"], id_zona)
    
    if vertice_entry is None:
        print(f"\n[!] Error: No se encontró la zona con ID: {id_zona}")
        return

    # Extraemos el valor real del vértice
    # (Ajusta ['value'] según cómo devuelva los datos tu implementación de mapa)
    v = vertice_entry['value']
    
    print(f"\n--- INFORMACIÓN DE LA ZONA {id_zona} ---")
    info = [
        ["ID", v.get("id", id_zona)],
        ["Latitud", v.get("lat")],
        ["Longitud", v.get("lon")],
        ["Total Registros", v.get("records_count")],
        ["SOG Promedio", v.get("avg_sog")],
        ["Cant. Embarcaciones", v.get("mmsi_list_size")] 
    ]
    
    print(tabulate(info, headers=["Atributo", "Valor"], tablefmt="fancy_grid"))

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

# main del ejercicio
import sys

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
