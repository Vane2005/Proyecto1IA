import heapq
import time  

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

def dynamic_weighting_search(n, inicio, meta, obstaculos, epsilon=1.5):
    N = n * n 
    open_list = []
    heapq.heappush(open_list, (0, inicio, 0))  
    came_from = {inicio: None}
    g_score = {inicio: 0}

    while open_list:
        f_actual, actual, depth = heapq.heappop(open_list)

        if actual == meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = came_from[actual]
            return camino[::-1]  

        for sucesor in generar_sucesores(actual, n, obstaculos):
            tentative_g = g_score[actual] + 1
            if sucesor not in g_score or tentative_g < g_score[sucesor]:
                g_score[sucesor] = tentative_g
                h = manhattan(sucesor, meta)
               
                f = tentative_g + h + epsilon * (1 - (depth / N)) * h
               
                heapq.heappush(open_list, (f, sucesor, depth + 1))
                came_from[sucesor] = actual
    return None
# prueba del algoritmo

if __name__ == "__main__":
 

    n = 5
    inicio = (0, 0)
    meta = (4, 4)
    obstaculos = [(1,1), (2,0), (2,3), (3,1), (4,2)]

    camino = dynamic_weighting_search(n, inicio, meta, obstaculos)

    if camino:
        print("Camino encontrado:")
        for i, pos in enumerate(camino):
            print(f"Paso {i + 1}: la hormiga se mueve a {pos}")
            time.sleep(0.5) #para simular la animación
        print(f"\nLongitud total: {len(camino)} pasos")
    else:
        print("No se encontró un camino hacia la meta.")

