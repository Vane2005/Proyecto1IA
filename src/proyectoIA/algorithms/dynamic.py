import heapq

def manhattan(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def generar_sucesores(posicion, n, obstaculos):
    movimientos = [(1,0), (-1,0), (0,1), (0,-1)]
    sucesores = []
    for dx, dy in movimientos:
        nx, ny = posicion[0] + dx, posicion[1] + dy
        if 0 <= nx < n and 0 <= ny < n and (nx, ny) not in obstaculos:
            sucesores.append((nx, ny))
    return sucesores

def dynamic_weighting_search(n, inicio, meta, obstaculos, epsilon=3):
    
    # Convertir obstaculos a set para búsquedas O(1)
    if not isinstance(obstaculos, set):
        obstaculos = set(obstaculos)
    
    # N = total de nodos posibles (usado para normalizar la profundidad)
    N = n * n
    
    # Cola de prioridad: (f_score, posición, profundidad)
    open_list = []
    heapq.heappush(open_list, (0, inicio, 0))
    
    # Diccionario para reconstruir el camino
    came_from = {inicio: None}
    
    # Diccionario con el costo real desde el inicio
    g_score = {inicio: 0}
    
    # Set de nodos ya procesados (optimización importante)
    closed_set = set()
    
    # Contador de nodos explorados (para estadísticas)
    nodos_explorados = 0
    
    while open_list:
        # Extraer el nodo con menor f_score
        f_actual, actual, depth = heapq.heappop(open_list)
        
        # Si ya procesamos este nodo, saltar (evita duplicados en el heap)
        if actual in closed_set:
            continue
        
        # Marcar como procesado
        closed_set.add(actual)
        nodos_explorados += 1
        
        # ¿Llegamos a la meta?
        if actual == meta:
            # Reconstruir el camino
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = came_from[actual]
            
            camino.reverse()  # Invertir para tener inicio → meta
            
            # Información opcional de depuración
            print(f"Camino encontrado en {nodos_explorados} nodos explorados")
            print(f"Longitud del camino: {len(camino)}")
            
            return camino
        
        # Expandir sucesores
        for sucesor in generar_sucesores(actual, n, obstaculos):
            # Si ya fue procesado, saltar
            if sucesor in closed_set:
                continue
            
            # Calcular costo tentativo
            tentative_g = g_score[actual] + 1
            
            # Solo procesar si es un camino nuevo o mejor
            if sucesor not in g_score or tentative_g < g_score[sucesor]:
                # Actualizar información del nodo
                g_score[sucesor] = tentative_g
                came_from[sucesor] = actual
                
                # Calcular heurística
                h = manhattan(sucesor, meta)
                
                # FÓRMULA DYNAMIC WEIGHTING:
                # f = g + h + ε × (1 - depth/N) × h
                # 
                # Componentes:
                # - g: costo real acumulado
                # - h: heurística (estimación hasta meta)
                # - ε × (1 - depth/N) × h: peso dinámico que decrece con profundidad
                #
                # Al inicio (depth=0): peso máximo → búsqueda agresiva
                # Al final (depth≈N): peso≈0 → como A* estándar
                
                peso_dinamico = epsilon * (1 - (depth / N)) * h
                f = tentative_g + h + peso_dinamico
                
                # Agregar a la cola de prioridad
                heapq.heappush(open_list, (f, sucesor, depth + 1))
    
    # No se encontró camino
    print(f"No hay camino. Se exploraron {nodos_explorados} nodos")
    return None