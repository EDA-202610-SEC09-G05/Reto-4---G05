def new_list():
    """
    Crea una lista (de tipo array_list) vacía.

    Returns
    -------
    dict
        Lista vacía con la estructura:
        {'size': 0, 'elements': []}

    Examples
    --------
    >>> lista = new_list()
    >>> lista
    {'size': 0, 'elements': []}
    """
    return {'size': 0, 'elements': []}


def is_empty(my_list):
    """
    Verifica si la lista está vacía.

    Parameters
    ----------
    my_list : dict
        Lista a verificar.

    Returns
    -------
    bool
        True si la lista está vacía, False en caso contrario.
    """
    if my_list["size"] == 0:
        return True
    else:
        return False
    

def size(my_list):
    """
    Retorna el tamaño de la lista.

    Parameters
    ----------
    my_list : dict
        Lista de la cual se obtiene el tamaño.

    Returns
    -------
    int
        Tamaño actual de la lista.
    """
    return my_list["size"]


def add_first(my_list, element):
    """
    Agrega un elemento al inicio de la lista.

    Parameters
    ----------
    my_list : dict
        Lista a la cual se agregará el elemento.
    element : any
        Elemento a agregar.

    Returns
    -------
    dict
        Lista con el elemento agregado al inicio.
    """
    my_list["elements"].insert(0,element)
    my_list["size"] += 1
    return my_list


def add_last(my_list, element):
    """
    Agrega un elemento al final de la lista.

    Parameters
    ----------
    my_list : dict
        Lista a la cual se agregará el elemento.
    element : any
        Elemento a agregar.

    Returns
    -------
    dict
        Lista con el elemento agregado al final.
    """
    my_list["elements"].append(element)
    my_list["size"] += 1
    return my_list


def first_element(my_list):
    """
    Retorna el primer elemento de la lista.

    Parameters
    ----------
    my_list : dict
        Lista de la cual se obtiene el primer elemento.

    Returns
    -------
    any
        Primer elemento de la lista.

    Raises
    ------
    IndexError
        Si la lista está vacía.
    """
    if is_empty(my_list):
        raise IndexError("empty list")
    return my_list["elements"][0]


def last_element(my_list):
    """
    Retorna el último elemento de la lista.

    Parameters
    ----------
    my_list : dict
        Lista de la cual se obtiene el último elemento.

    Returns
    -------
    any
        Último elemento de la lista.

    Raises
    ------
    IndexError
        Si la lista está vacía.
    """
    if is_empty(my_list):
        raise IndexError("empty list")
    return my_list["elements"][-1]


def get_element(my_list, pos):
    """
    Retorna el elemento en la posición dada.

    Parameters
    ----------
    my_list : dict
        Lista de referencia.
    pos : int
        Posición del elemento a obtener.

    Returns
    -------
    any
        Elemento almacenado en la posición indicada.

    Raises
    ------
    Exception
        Si la posición no es válida.
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")
    return my_list["elements"][pos]


def delete_element(my_list, pos):
    """
    Elimina el elemento en la posición dada.

    Parameters
    ----------
    my_list : dict
        Lista de la cual se eliminará el elemento.
    pos : int
        Posición del elemento a eliminar.

    Returns
    -------
    dict
        Lista con el elemento eliminado.

    Raises
    ------
    IndexError
        Si la posición no es válida.
    """
    if pos < 0 or pos >= size(my_list):
        raise IndexError("list index out of range")
    my_list["elements"].pop(pos)
    my_list["size"] -= 1
    return my_list


def remove_first(my_list):
    """
    Elimina el primer elemento de la lista.

    Parameters
    ----------
    my_list : dict
        Lista de la cual se eliminará el primer elemento.

    Returns
    -------
    any
        Elemento eliminado.

    Raises
    ------
    IndexError
        Si la lista está vacía.
    """
    if is_empty(my_list):
        raise IndexError("empty list")
    elem = my_list["elements"].pop(0)
    my_list["size"] -= 1
    return elem


def remove_last(my_list):
    """
    Elimina el último elemento de la lista.

    Parameters
    ----------
    my_list : dict
        Lista de la cual se eliminará el último elemento.

    Returns
    -------
    any
        Elemento eliminado.

    Raises
    ------
    IndexError
        Si la lista está vacía.
    """
    if is_empty(my_list):
        raise IndexError("empty list")
    elem = my_list["elements"].pop()
    my_list["size"] -= 1
    return elem


def insert_element(my_list, element, pos):
    """
    Inserta un elemento en la posición dada.

    Parameters
    ----------
    my_list : dict
        Lista en la cual se insertará el elemento.
    element : any
        Elemento a insertar.
    pos : int
        Posición en la cual se insertará.

    Returns
    -------
    dict
        Lista con el elemento insertado.
    """
    if pos < 0 or pos > size(my_list):
        raise IndexError("list index out of range")
    my_list["elements"].insert(pos,element)
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
        Primer elemento.
    element_2 : any
        Segundo elemento.

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

    Parameters
    ----------
    my_list : dict
        Lista en la cual se buscará el elemento.
    element : any
        Elemento a buscar.
    cmp_function : function, optional
        Función de comparación. Por defecto usa default_function.

    Returns
    -------
    int
        Posición del elemento si está presente, -1 en caso contrario.
    """
    for i, j in enumerate(my_list["elements"]):
        if cmp_function(element, j) == 0:
            return i
    return -1


def change_info(my_list, pos, new_info):
    """
    Cambia la información de un elemento en la posición dada.

    Parameters
    ----------
    my_list : dict
        Lista de referencia.
    pos : int
        Posición del elemento a reemplazar.
    new_info : any
        Nueva información a guardar.

    Returns
    -------
    dict
        Lista con la información modificada.

    Raises
    ------
    IndexError
        Si la posición no es válida.
    """
    if pos < 0 or pos > size(my_list):
        raise IndexError("list index out of range")
    my_list["elements"][pos] = new_info
    return my_list


def exchange(my_list, pos_1, pos_2):
    """
    Intercambia los elementos en las posiciones dadas.

    Parameters
    ----------
    my_list : dict
        Lista de referencia.
    pos_1 : int
        Primera posición.
    pos_2 : int
        Segunda posición.

    Returns
    -------
    dict
        Lista con los elementos intercambiados.

    Raises
    ------
    IndexError
        Si alguna posición no es válida.
    """
    if pos_1 < 0 or pos_1 > size(my_list):
        raise IndexError("list index pos_1 out of range")
    if pos_2 < 0 or pos_2 > size(my_list):
        raise IndexError("list index pos_2 out of range")
    lista = my_list["elements"]
    lista[pos_1], lista[pos_2] = lista[pos_2], lista[pos_1]
    return my_list


def sub_list(my_list, pos_i, num_elements):
    """
    Retorna una sublista a partir de una posición inicial y una cantidad de elementos.

    Parameters
    ----------
    my_list : dict
        Lista original.
    pos_i : int
        Posición inicial de la sublista.
    num_elements : int
        Número de elementos a incluir.

    Returns
    -------
    dict
        Nueva lista (array_list) con la porción solicitada.
    """
    if pos_i < 0 or pos_i >= size(my_list):
        raise IndexError("list index out of range")

    lista = new_list()
    lista["elements"] = my_list["elements"][pos_i:pos_i+num_elements]
    lista["size"] = len(lista["elements"])
    return lista


def adjacents(my_list, element):
    """
    Retorna una lista Python con los elementos adyacentes a un elemento dado.

    Los adyacentes son:
    - el elemento anterior (si existe)
    - el elemento siguiente (si existe)

    Si el elemento no existe en la lista, retorna None.

    Parameters
    ----------
    my_list : dict
        Lista a examinar.
    element : any
        Elemento de referencia.

    Returns
    -------
    list | None
        Lista Python con los adyacentes, o None si el elemento no existe.
    """
    pos = is_present(my_list, element)
    if pos == -1:
        return None

    adjs = []
    if pos - 1 >= 0:
        adjs.append(my_list["elements"][pos - 1])
    if pos + 1 < len(my_list["elements"]):
        adjs.append(my_list["elements"][pos + 1])
    return adjs


def to_py_list(my_list):
    """
    Retorna los elementos de la lista en una lista Python.

    Parameters
    ----------
    my_list : dict
        Array list de referencia.

    Returns
    -------
    list
        Lista Python con los elementos en el mismo orden de aparición.
    """
    return my_list["elements"]

def join_lists(list_1, list_2):
    """
    Retorna una nueva lista que es la concatenación de las dos listas dadas.

    Parameters
    ----------
    list_1 : dict
        Primera lista (array_list).
    list_2 : dict
        Segunda lista (array_list).

    Returns
    -------
    dict
        Nueva lista (array_list) con los elementos de ambas listas.
    """
    for element in list_2["elements"]:
        add_last(list_1, element)
    return list_1