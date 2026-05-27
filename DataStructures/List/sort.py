
def default_sort_criteria(element_1, element_2):
    """
    Función de comparación por defecto para ordenar elementos.

    Compara dos elementos y retorna True si el primer elemento debe ir
    antes que el segundo (orden ascendente).

    Parameters
    ----------
    element_1 : any
        Primer elemento a comparar.
    element_2 : any
        Segundo elemento a comparar.

    Returns
    -------
    bool
        True si element_1 < element_2, False en caso contrario.
    """
    return element_1 < element_2


def selection_sort(my_list, sort_crit, dslist):
    """
    Ordena una lista usando Selection Sort.

    Esta función es genérica y funciona con array_list o single_linked_list,
    siempre que se pase el módulo correspondiente en dslist.

    Parameters
    ----------
    my_list : dict
        Lista a ordenar.
    sort_crit : function
        Función de comparación (retorna True/False).
    dslist : module
        Módulo de implementación de lista (array_list o single_linked_list).

    Returns
    -------
    dict
        Lista ordenada.
    """
    n = dslist.size(my_list)

    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if sort_crit(dslist.get_element(my_list, j), dslist.get_element(my_list, min_idx)):
                min_idx = j
        if min_idx != i:
            dslist.exchange(my_list, i, min_idx)

    return my_list


def insertion_sort(my_list, sort_crit, dslist):
    """
    Ordena una lista usando Insertion Sort.

    Parameters
    ----------
    my_list : dict
        Lista a ordenar.
    sort_crit : function
        Función de comparación (retorna True/False).
    dslist : module
        Módulo de implementación de lista (array_list o single_linked_list).

    Returns
    -------
    dict
        Lista ordenada.
    """
    n = dslist.size(my_list)

    for i in range(1, n):
        key = dslist.get_element(my_list, i)
        j = i - 1

        while j >= 0 and sort_crit(key, dslist.get_element(my_list, j)):
            dslist.change_info(my_list, j + 1, dslist.get_element(my_list, j))
            j -= 1

        dslist.change_info(my_list, j + 1, key)

    return my_list


def shell_sort(my_list, sort_crit, dslist):
    """
    Ordena una lista usando Shell Sort.

    Parameters
    ----------
    my_list : dict
        Lista a ordenar.
    sort_crit : function
        Función de comparación (retorna True/False).
    dslist : module
        Módulo de implementación de lista (array_list o single_linked_list).

    Returns
    -------
    dict
        Lista ordenada.
    """
    n = dslist.size(my_list)
    gap = n // 2

    while gap > 0:
        for i in range(gap, n):
            temp = dslist.get_element(my_list, i)
            j = i

            while j >= gap and sort_crit(temp, dslist.get_element(my_list, j - gap)):
                dslist.change_info(my_list, j, dslist.get_element(my_list, j - gap))
                j -= gap

            dslist.change_info(my_list, j, temp)

        gap //= 2

    return my_list


def _merge_py_lists(left, right, sort_crit):
    """
    Mezcla dos listas Python ordenadas en una sola lista ordenada.

    Parameters
    ----------
    left : list
        Sublista izquierda ordenada.
    right : list
        Sublista derecha ordenada.
    sort_crit : function
        Función de comparación.

    Returns
    -------
    list
        Lista resultante ordenada.
    """
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if sort_crit(left[i], right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    while i < len(left):
        result.append(left[i])
        i += 1

    while j < len(right):
        result.append(right[j])
        j += 1

    return result


def _merge_sort_py(py_list, sort_crit):
    """
    Implementación recursiva de Merge Sort sobre lista Python.

    Parameters
    ----------
    py_list : list
        Lista Python a ordenar.
    sort_crit : function
        Función de comparación.

    Returns
    -------
    list
        Lista Python ordenada.
    """
    if len(py_list) <= 1:
        return py_list

    mid = len(py_list) // 2
    left = _merge_sort_py(py_list[:mid], sort_crit)
    right = _merge_sort_py(py_list[mid:], sort_crit)

    return _merge_py_lists(left, right, sort_crit)


def merge_sort(my_list, sort_crit, dslist):
    """
    Ordena una lista usando Merge Sort.

    Convierte la lista a lista Python, aplica merge sort y luego
    sobrescribe los elementos en la lista original.

    Parameters
    ----------
    my_list : dict
        Lista a ordenar.
    sort_crit : function
        Función de comparación (retorna True/False).
    dslist : module
        Módulo de implementación de lista (array_list o single_linked_list).

    Returns
    -------
    dict
        Lista ordenada.
    """
    py_list = dslist.to_py_list(my_list)
    sorted_list = _merge_sort_py(py_list, sort_crit)

    for i, elem in enumerate(sorted_list):
        dslist.change_info(my_list, i, elem)

    return my_list


def _quick_sort_py(py_list, sort_crit):
    """
    Implementación recursiva de Quick Sort sobre lista Python.

    Parameters
    ----------
    py_list : list
        Lista Python a ordenar.
    sort_crit : function
        Función de comparación.

    Returns
    -------
    list
        Lista Python ordenada.
    """
    if len(py_list) <= 1:
        return py_list

    pivot = py_list[len(py_list) // 2]
    left = []
    equal = []
    right = []

    for elem in py_list:
        if sort_crit(elem, pivot):
            left.append(elem)
        elif sort_crit(pivot, elem):
            right.append(elem)
        else:
            equal.append(elem)

    return _quick_sort_py(left, sort_crit) + equal + _quick_sort_py(right, sort_crit)


def quick_sort(my_list, sort_crit, dslist):
    """
    Ordena una lista usando Quick Sort.

    Convierte la lista a lista Python, aplica quick sort y luego
    sobrescribe los elementos en la lista original.

    Parameters
    ----------
    my_list : dict
        Lista a ordenar.
    sort_crit : function
        Función de comparación (retorna True/False).
    dslist : module
        Módulo de implementación de lista (array_list o single_linked_list).

    Returns
    -------
    dict
        Lista ordenada.
    """
    py_list = dslist.to_py_list(my_list)
    sorted_list = _quick_sort_py(py_list, sort_crit)

    for i, elem in enumerate(sorted_list):
        dslist.change_info(my_list, i, elem)

    return my_list