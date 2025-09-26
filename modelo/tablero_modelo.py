"""
Modelo - Maneja la lógica del juego y el estado del tablero
"""

class TableroModelo:
    def __init__(self, filas=5, columnas=5):
        self.filas = filas
        self.columnas = columnas
        self.tablero = []
        self.pos_hormiga = [0, 0]
        self.pos_meta = [0, 0]
        self.inicializar_tablero()
    
    def inicializar_tablero(self):
        """Inicializa el tablero con configuración por defecto"""
        if self.filas == 5 and self.columnas == 5:
            # Configuración original de 5x5
            self.tablero = [
                ['inicio', 'libre', 'libre', 'libre', 'libre'],
                ['veneno', 'libre', 'libre', 'libre', 'libre'],
                ['veneno', 'libre', 'libre', 'veneno', 'libre'],
                ['libre', 'veneno', 'libre', 'libre', 'libre'],
                ['libre', 'libre', 'veneno', 'libre', 'meta']
            ]
            self.pos_hormiga = [0, 0]
            self.pos_meta = [4, 4]
        else:
            # Configuración automática para otros tamaños
            self.tablero = [['libre' for _ in range(self.columnas)] for _ in range(self.filas)]
            self.pos_hormiga = [0, 0]
            self.pos_meta = [self.filas-1, self.columnas-1]
            
            # Colocar inicio y meta
            self.tablero[0][0] = 'inicio'
            self.tablero[self.filas-1][self.columnas-1] = 'meta'
            
            # Agregar algunos venenos aleatorios
            self._generar_venenos_aleatorios()
    
    def _generar_venenos_aleatorios(self):
        """Genera venenos aleatorios en el tablero"""
        import random
        total_celdas = self.filas * self.columnas
        num_venenos = max(1, total_celdas // 5)
        
        venenos_colocados = 0
        while venenos_colocados < num_venenos:
            fila = random.randint(0, self.filas-1)
            col = random.randint(0, self.columnas-1)
            
            if self.tablero[fila][col] == 'libre':
                self.tablero[fila][col] = 'veneno'
                venenos_colocados += 1
    
    def cambiar_tamaño(self, nuevas_filas, nuevas_cols):
        """Cambia el tamaño del tablero"""
        self.filas = nuevas_filas
        self.columnas = nuevas_cols
        self.inicializar_tablero()
    
    def aplicar_configuracion_desde_archivo(self, configuracion):
        """Aplica configuración cargada desde archivo"""
        # Limpiar tablero
        for i in range(self.filas):
            for j in range(self.columnas):
                self.tablero[i][j] = 'libre'
        
        # Aplicar configuración
        inicio_x, inicio_y = configuracion['inicio']
        meta_x, meta_y = configuracion['meta']
        
        self.tablero[inicio_x][inicio_y] = 'inicio'
        self.pos_hormiga = [inicio_x, inicio_y]
        
        self.tablero[meta_x][meta_y] = 'meta'
        self.pos_meta = [meta_x, meta_y]
        
        # Colocar venenos
        for veneno_x, veneno_y in configuracion['venenos']:
            self.tablero[veneno_x][veneno_y] = 'veneno'
    
    def generar_tablero_aleatorio(self):
        """Genera un nuevo tablero aleatorio"""
        import random
        
        # Limpiar tablero
        self.tablero = [['libre' for _ in range(self.columnas)] for _ in range(self.filas)]
        
        # Posiciones disponibles
        posiciones_disponibles = [(i, j) for i in range(self.filas) for j in range(self.columnas)]
        
        # Colocar inicio
        inicio_pos = random.choice(posiciones_disponibles)
        self.pos_hormiga = list(inicio_pos)
        self.tablero[inicio_pos[0]][inicio_pos[1]] = 'inicio'
        posiciones_disponibles.remove(inicio_pos)
        
        # Colocar meta
        meta_pos = random.choice(posiciones_disponibles)
        self.pos_meta = list(meta_pos)
        self.tablero[meta_pos[0]][meta_pos[1]] = 'meta'
        posiciones_disponibles.remove(meta_pos)
        
        # Colocar venenos
        total_celdas = len(posiciones_disponibles)
        num_venenos = random.randint(total_celdas//5, total_celdas//3)
        
        venenos_pos = random.sample(posiciones_disponibles, min(num_venenos, len(posiciones_disponibles)))
        for pos in venenos_pos:
            self.tablero[pos[0]][pos[1]] = 'veneno'
    
    def mover_hormiga(self, delta_fila, delta_col):
        """
        Mueve la hormiga y retorna el resultado del movimiento
        Returns: ('exito', 'veneno', 'meta', 'invalido')
        """
        nueva_fila = self.pos_hormiga[0] + delta_fila
        nueva_col = self.pos_hormiga[1] + delta_col
        
        # Verificar límites
        if not (0 <= nueva_fila < self.filas and 0 <= nueva_col < self.columnas):
            return 'invalido'
        
        # Verificar veneno
        if self.tablero[nueva_fila][nueva_col] == 'veneno':
            return 'veneno'
        
        # Mover hormiga
        self.pos_hormiga = [nueva_fila, nueva_col]
        
        # Verificar meta
        if self.pos_hormiga == self.pos_meta:
            return 'meta'
        
        return 'exito'
    
    def obtener_movimientos_posibles(self):
        """Retorna movimientos válidos desde la posición actual"""
        movimientos = []
        direcciones = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for delta_fila, delta_col in direcciones:
            nueva_fila = self.pos_hormiga[0] + delta_fila
            nueva_col = self.pos_hormiga[1] + delta_col
            
            if (0 <= nueva_fila < self.filas and 
                0 <= nueva_col < self.columnas and 
                self.tablero[nueva_fila][nueva_col] != 'veneno'):
                movimientos.append((delta_fila, delta_col))
        
        return movimientos
    
    def reiniciar_posicion_hormiga(self):
        """Reinicia la hormiga a la posición inicial"""
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.tablero[i][j] == 'inicio':
                    self.pos_hormiga = [i, j]
                    return
    
    def obtener_estado_tablero(self):
        """Retorna el estado completo del tablero"""
        return {
            'filas': self.filas,
            'columnas': self.columnas,
            'tablero': [fila.copy() for fila in self.tablero],
            'pos_hormiga': self.pos_hormiga.copy(),
            'pos_meta': self.pos_meta.copy()
        }
    
    def es_coordenada_valida(self, coord):
        """Verifica si una coordenada está dentro del tablero"""
        if not coord:
            return False
        x, y = coord
        return 0 <= x < self.filas and 0 <= y < self.columnas
