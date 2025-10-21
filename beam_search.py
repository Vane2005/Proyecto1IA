# Calcula la distancia manhattan entre 2 puntos
def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# Aplicación de los operadores
def moverArriba(tupla_x_y):
    return (tupla_x_y[0] - 1, tupla_x_y[1])

def moverAbajo(tupla_x_y):
    return (tupla_x_y[0] + 1, tupla_x_y[1])

def moverIzquierda(posicion):
    return (posicion[0], posicion[1] - 1)

def moverDerecha(posicion):
    return (posicion[0], posicion[1] + 1)


# Determinar posibilidad de un movimiento
def isPosibleArriba(posicion):
    return posicion[0] - 1 >= 0

def isPosibleAbajo(posicion, n):
    return posicion[0] + 1 < n

def isPosibleIzquierda(posicion):
    return posicion[1] - 1 >= 0

def isPosibleDerecha(posicion, n):
    return posicion[1] + 1 < n

def isNodoMeta(meta, posicion):
    return meta[0] == posicion[0] and meta[1] == posicion[1]


def calcular_beam_width(n, num_obstaculos):
    """
    n: tamaño del tablero (nxn)
    num_obstaculos: cantidad de obstáculos en el tablero
    """
    densidad = num_obstaculos / (n * n)
    
    if n <= 10:
        base = 5
    elif n <= 30:
        base = 4
    elif n <= 50:
        base = 3
    else:
        base = 3
    
    # Ajustar por densidad de obstáculos
    if densidad > 0.4:  # Muchos obstáculos
        multiplicador = 1.5
    elif densidad > 0.2:  # Obstáculos moderados
        multiplicador = 1.2
    else:  # Pocos obstáculos
        multiplicador = 1.0
    
    beam_width = int(base * multiplicador)
    
    return max(3, min(beam_width, 10))


def expandir_nodo(nodo_actual, meta, obstaculos, n, indice_padre):
    """
    Expande un nodo generando todos sus sucesores válidos
    Retorna una lista de tuplas: (indice_padre, posicion, g_n, h_n, f_n)
    """
    posicion_actual = nodo_actual[0]
    g_actual = nodo_actual[2]
    
    sucesores = []
    
    # Definir movimientos posibles
    movimientos = [
        (isPosibleArriba(posicion_actual), moverArriba, "arriba"),
        (isPosibleAbajo(posicion_actual, n), moverAbajo, "abajo"),
        (isPosibleIzquierda(posicion_actual), moverIzquierda, "izquierda"),
        (isPosibleDerecha(posicion_actual, n), moverDerecha, "derecha")
    ]
    
    for es_posible, mover, direccion in movimientos:
        if es_posible:
            nueva_posicion = mover(posicion_actual)
            
            # Calcular costos
            costo_movimiento = 3 if nueva_posicion in obstaculos else 1
            g_n = g_actual + costo_movimiento
            h_n = manhattan(nueva_posicion, meta)
            f_n = g_n + h_n
            
            sucesores.append((indice_padre, nueva_posicion, g_n, h_n, f_n))
    
    return sucesores


def reconstruir_camino(closedList, indice_meta):
    """
    Reconstruye el camino desde el inicio hasta la meta
    siguiendo los índices de padres
    """
    camino = []
    indice_actual = indice_meta
    
    while indice_actual is not None:
        nodo = closedList[indice_actual]
        camino.append(nodo[0])  # Agregar la posición
        indice_actual = nodo[1]  # Moverse al padre
    
    camino.reverse()  # Invertir para tener el camino de inicio a meta
    return camino


def beam_search(n, inicio, meta, obstaculos):
    
    # Convertir obstáculos a set para búsquedas O(1)
    obstaculos_set = set(obstaculos) if not isinstance(obstaculos, set) else obstaculos
    
    beamWidth = calcular_beam_width(n, len(obstaculos))
    
    # closedList: [posicion, indice_padre, g_n, h_n]
    closedList = []
    
    visitados = set()
    visitados.add(inicio)
    
    h_inicial = manhattan(inicio, meta)
    closedList.append([inicio, None, 0, h_inicial])
    
    if inicio == meta:
        return [inicio]
    
    openList = [0]
    iteracion = 0
    max_iteraciones = n * n * 2
    
    # Detección de estancamiento
    mejor_h_previo = h_inicial
    iteraciones_sin_mejora = 0
    
    while openList and iteracion < max_iteraciones:
        iteracion += 1
        todos_sucesores = []
        
        # Expandir beam actual
        for indice_nodo in openList:
            nodo = closedList[indice_nodo]
            sucesores = expandir_nodo(nodo, meta, obstaculos_set, n, indice_nodo)
            
            for sucesor in sucesores:
                indice_padre, posicion, g_n, h_n, f_n = sucesor
                
                if posicion == meta:
                    closedList.append([posicion, indice_padre, g_n, h_n])
                    return reconstruir_camino(closedList, len(closedList) - 1)
                
                if posicion not in visitados:
                    todos_sucesores.append((posicion, indice_padre, g_n, h_n, f_n))
                    visitados.add(posicion)
        
        if not todos_sucesores:
            return None
        
        todos_sucesores.sort(key=lambda x: x[4])
        
        # Seleccionar los w mejores
        mejores_sucesores = todos_sucesores[:beamWidth]
        
        mejor_h_actual = min(s[3] for s in mejores_sucesores)
        if mejor_h_actual >= mejor_h_previo:
            iteraciones_sin_mejora += 1
            if iteraciones_sin_mejora > beamWidth * 2:
                return None  # Probablemente no hay camino
        else:
            iteraciones_sin_mejora = 0
            mejor_h_previo = mejor_h_actual
        
        # Actualizar openList
        openList = []
        for posicion, indice_padre, g_n, h_n, f_n in mejores_sucesores:
            closedList.append([posicion, indice_padre, g_n, h_n])
            openList.append(len(closedList) - 1)
    
    return None
