from DataStructures.List import list_node as ln


def new_list():
    """
    Crea una lista enlazada simple (single_linked_list) vacía.

    La lista se representa con un diccionario con las llaves:
    - "size": número de elementos
    - "first": referencia al primer nodo
    - "last": referencia al último nodo

    Returns
    -------
    dict
        Lista vacía con la estructura:
        {"size": 0, "first": None, "last": None}
    """
    return {"size": 0, "first": None, "last": None}


def is_empty(my_list):
    """
    Verifica si la lista está vacía.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a verificar.

    Returns
    -------
    bool
        True si la lista está vacía, False en caso contrario.
    """
    return my_list["size"] == 0


def size(my_list):
    """
    Retorna el tamaño de la lista.

    Parameters
    ----------
    my_list : dict
        Lista enlazada de referencia.

    Returns
    -------
    int
        Número de elementos de la lista.
    """
    return my_list["size"]


def add_first(my_list, element):
    """
    Agrega un elemento al inicio de la lista.

    Si la lista está vacía, el nuevo nodo pasa a ser tanto el primero
    como el último.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    element : any
        Elemento a insertar.

    Returns
    -------
    dict
        Lista con el elemento agregado al inicio.
    """
    new_node = ln.new_single_node(element)
    if is_empty(my_list):
        my_list["first"] = new_node
        my_list["last"] = new_node
    else:
        new_node["next"] = my_list["first"]
        my_list["first"] = new_node
    my_list["size"] += 1
    return my_list


def add_last(my_list, element):
    """
    Agrega un elemento al final de la lista.

    Si la lista está vacía, el nuevo nodo pasa a ser tanto el primero
    como el último.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    element : any
        Elemento a insertar.

    Returns
    -------
    dict
        Lista con el elemento agregado al final.
    """
    new_node = ln.new_single_node(element)
    if is_empty(my_list):
        my_list["first"] = new_node
        my_list["last"] = new_node
    else:
        my_list["last"]["next"] = new_node
        my_list["last"] = new_node
    my_list["size"] += 1
    return my_list


def first_element(my_list):
    """
    Retorna el primer elemento de una lista no vacía.

    Parameters
    ----------
    my_list : dict
        Lista enlazada de referencia.

    Returns
    -------
    any
        Información almacenada en el primer nodo.

    Raises
    ------
    IndexError
        Si la lista está vacía, lanza:
        IndexError("list index out of range")
    """
    if is_empty(my_list):
        raise IndexError("list index out of range")
    return my_list["first"]["info"]


def last_element(my_list):
    """
    Retorna el último elemento de una lista no vacía.

    Parameters
    ----------
    my_list : dict
        Lista enlazada de referencia.

    Returns
    -------
    any
        Información almacenada en el último nodo.

    Raises
    ------
    IndexError
        Si la lista está vacía, lanza:
        IndexError("list index out of range")
    """
    if is_empty(my_list):
        raise IndexError("list index out of range")
    return my_list["last"]["info"]


def get_element(my_list, pos):
    """
    Retorna el elemento en la posición dada.

    La posición debe cumplir: 0 <= pos < size(my_list)

    Parameters
    ----------
    my_list : dict
        Lista enlazada de referencia.
    pos : int
        Posición del elemento a obtener.

    Returns
    -------
    any
        Elemento en la posición solicitada.

    Raises
    ------
    IndexError
        Si la posición no es válida, lanza:
        IndexError("list index out of range")
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")
    current = my_list["first"]
    i = 0
    while i < pos:
        current = current["next"]
        i += 1
    return current["info"]


def delete_element(my_list, pos):
    """
    Elimina el elemento en la posición dada.

    La posición debe cumplir: 0 <= pos < size(my_list)

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    pos : int
        Posición del elemento a eliminar.

    Returns
    -------
    dict
        Lista con el elemento eliminado.

    Raises
    ------
    IndexError
        Si la posición no es válida, lanza:
        IndexError("list index out of range")
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")

    if pos == 0:
        my_list["first"] = my_list["first"]["next"]
        my_list["size"] -= 1
        if my_list["size"] == 0:
            my_list["last"] = None
        return my_list

    prev = my_list["first"]
    i = 0
    while i < pos - 1:
        prev = prev["next"]
        i += 1

    to_delete = prev["next"]
    prev["next"] = to_delete["next"]

    if pos == my_list["size"] - 1:
        my_list["last"] = prev

    my_list["size"] -= 1
    return my_list


def remove_first(my_list):
    """
    Elimina y retorna el primer elemento de la lista.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.

    Returns
    -------
    any
        Elemento eliminado del inicio.

    Raises
    ------
    IndexError
        Si la lista está vacía, lanza:
        IndexError("list index out of range")
    """
    if is_empty(my_list):
        raise IndexError("list index out of range")

    info = my_list["first"]["info"]
    my_list["first"] = my_list["first"]["next"]
    my_list["size"] -= 1

    if my_list["size"] == 0:
        my_list["last"] = None

    return info


def remove_last(my_list):
    """
    Elimina y retorna el último elemento de la lista.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.

    Returns
    -------
    any
        Elemento eliminado del final.

    Raises
    ------
    IndexError
        Si la lista está vacía, lanza:
        IndexError("list index out of range")
    """
    if is_empty(my_list):
        raise IndexError("list index out of range")

    if my_list["size"] == 1:
        info = my_list["first"]["info"]
        my_list["first"] = None
        my_list["last"] = None
        my_list["size"] = 0
        return info

    prev = my_list["first"]
    while prev["next"] != my_list["last"]:
        prev = prev["next"]

    info = my_list["last"]["info"]
    prev["next"] = None
    my_list["last"] = prev
    my_list["size"] -= 1
    return info


def insert_element(my_list, element, pos):
    """
    Inserta un elemento en la posición dada.

    La posición debe cumplir: 0 <= pos <= size(my_list)

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    element : any
        Elemento a insertar.
    pos : int
        Posición donde se insertará el elemento.

    Returns
    -------
    dict
        Lista con el elemento insertado.

    Raises
    ------
    IndexError
        Si la posición no es válida, lanza:
        IndexError("list index out of range")
    """
    if pos < 0 or pos > size(my_list):
        raise IndexError("list index out of range")

    if pos == 0:
        return add_first(my_list, element)

    if pos == size(my_list):
        return add_last(my_list, element)

    new_node = ln.new_single_node(element)
    prev = my_list["first"]
    i = 0
    while i < pos - 1:
        prev = prev["next"]
        i += 1

    new_node["next"] = prev["next"]
    prev["next"] = new_node
    my_list["size"] += 1
    return my_list


def default_function(element_1, element_2):
    """
    Función de comparación por defecto.

    Compara dos elementos y retorna:
    - 1 si element_1 > element_2
    - -1 si element_1 < element_2
    - 0 si son iguales

    Parameters
    ----------
    element_1 : any
        Primer elemento a comparar.
    element_2 : any
        Segundo elemento a comparar.

    Returns
    -------
    int
        Resultado de la comparación.
    """
    if element_1 > element_2:
        return 1
    elif element_1 < element_2:
        return -1
    else:
        return 0


def is_present(my_list, element, cmp_function=default_function):
    """
    Verifica si un elemento está presente en la lista.

    La comparación se realiza usando la función cmp_function.

    Parameters
    ----------
    my_list : dict
        Lista enlazada donde se buscará.
    element : any
        Elemento a buscar.
    cmp_function : function, optional
        Función de comparación. Debe retornar 0 si son iguales.

    Returns
    -------
    int
        Posición del elemento si está presente, -1 en caso contrario.
    """
    current = my_list["first"]
    pos = 0
    while current is not None:
        if cmp_function(element, current["info"]) == 0:
            return pos
        current = current["next"]
        pos += 1
    return -1


def change_info(my_list, pos, new_info):
    """
    Cambia la información de un elemento en la posición dada.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    pos : int
        Posición del elemento a cambiar.
    new_info : any
        Nueva información a almacenar.

    Returns
    -------
    dict
        Lista con la información modificada.

    Raises
    ------
    IndexError
        Si la posición no es válida, lanza:
        IndexError("list index out of range")
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")

    current = my_list["first"]
    i = 0
    while i < pos:
        current = current["next"]
        i += 1

    current["info"] = new_info
    return my_list

def add_number(my_list, pos, number):
    """
    Agrega un número a la información de un elemento en la posición dada.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    number : int | float
        Número a agregar a la información actual.
    pos : int
        Posición del elemento a modificar.

    Returns
    -------
    dict
        Lista con la información modificada.

    Raises
    ------
    IndexError
        Si la posición no es válida, lanza:
        IndexError("list index out of range")
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")

    current = my_list["first"]
    i = 0
    while i < pos:
        current = current["next"]
        i += 1

    current["info"] += number
    return my_list


def exchange(my_list, pos_1, pos_2):
    """
    Intercambia la información de dos elementos en las posiciones dadas.

    Parameters
    ----------
    my_list : dict
        Lista enlazada a modificar.
    pos_1 : int
        Posición del primer elemento.
    pos_2 : int
        Posición del segundo elemento.

    Returns
    -------
    dict
        Lista con los elementos intercambiados.

    Raises
    ------
    IndexError
        Si alguna posición no es válida, lanza:
        IndexError("list index out of range")
    """
    if pos_1 < 0 or pos_1 >= size(my_list) or pos_2 < 0 or pos_2 >= size(my_list):
        raise IndexError("list index out of range")

    if pos_1 == pos_2:
        return my_list

    if pos_1 > pos_2:
        pos_1, pos_2 = pos_2, pos_1

    current = my_list["first"]
    i = 0
    node_1 = None
    node_2 = None

    while current is not None:
        if i == pos_1:
            node_1 = current
        if i == pos_2:
            node_2 = current
            break
        current = current["next"]
        i += 1

    node_1["info"], node_2["info"] = node_2["info"], node_1["info"]
    return my_list


def sub_list(my_list, pos, num_elements):
    """
    Retorna una sublista de la lista original.

    La sublista comienza en la posición `pos` y contiene hasta `num_elements`
    elementos (o menos si se llega al final de la lista).

    Parameters
    ----------
    my_list : dict
        Lista enlazada original.
    pos : int
        Posición inicial de la sublista.
    num_elements : int
        Número de elementos a incluir.

    Returns
    -------
    dict
        Nueva lista enlazada con la sublista.

    Raises
    ------
    IndexError
        Si `pos` es inválida o `num_elements` es negativo, lanza:
        IndexError("list index out of range")
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")

    if num_elements < 0:
        raise IndexError("list index out of range")

    result = new_list()
    current = my_list["first"]
    i = 0

    while i < pos:
        current = current["next"]
        i += 1

    count = 0
    while current is not None and count < num_elements:
        add_last(result, current["info"])
        current = current["next"]
        count += 1

    return result


def adjacents(my_list, element):
    """
    Retorna una lista Python con el elemento siguiente al elemento dado.

    Comportamiento según la guía de single_linked_list:
    - Si el elemento existe y tiene siguiente, retorna [siguiente]
    - Si el elemento existe y es el último, retorna []
    - Si el elemento no existe, retorna None

    Parameters
    ----------
    my_list : dict
        Lista enlazada a examinar.
    element : any
        Elemento de referencia.

    Returns
    -------
    list | None
        Lista Python con el siguiente elemento, lista vacía si es el último,
        o None si no existe.
    """
    current = my_list["first"]

    while current is not None:
        if current["info"] == element:
            if current["next"] is None:
                return []
            return [current["next"]["info"]]
        current = current["next"]

    return None


def to_py_list(my_list):
    """
    Convierte la lista enlazada a una lista Python.

    Los elementos se retornan en el mismo orden en que aparecen en la lista.

    Parameters
    ----------
    my_list : dict
        Lista enlazada de referencia.

    Returns
    -------
    list
        Lista Python con los elementos de la lista enlazada.
    """
    py_list = []
    current = my_list["first"]

    while current is not None:
        py_list.append(current["info"])
        current = current["next"]

    return py_list

def to_sl_list(py_list):
    """
    Convierte una lista Python a una lista enlazada simple.

    Los elementos se insertan en el mismo orden en que aparecen en la lista.

    Parameters
    ----------
    py_list : list
        Lista Python de referencia.

    Returns
    -------
    dict
        Lista enlazada con los elementos de la lista Python.
    """
    sl_list = new_list()
    for element in py_list:
        add_last(sl_list, element)
    return sl_list