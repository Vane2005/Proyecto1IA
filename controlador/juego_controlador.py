"""
Controlador - Coordina la interacción entre el modelo y la vista
"""

import time
from threading import Thread
from modelo.tablero_modelo import TableroModelo
from modelo.archivo_manager import ArchivoManager

class JuegoControlador:
    def __init__(self, vista):
        self.vista = vista
        self.modelo = TableroModelo()
        self.archivo_manager = ArchivoManager()
    
    def inicializar_interfaz(self):
        """Inicializa la interfaz después de que el controlador esté asignado"""
        self.vista.crear_interfaz(self.modelo.filas, self.modelo.columnas)
        self.actualizar_vista()
    
    def actualizar_vista(self):
        """Actualiza la vista con el estado actual del modelo"""
        estado = self.modelo.obtener_estado_tablero()
        self.vista.actualizar_tablero(estado)
    
    def mover_hormiga(self, delta_fila, delta_col):
        """Maneja el movimiento de la hormiga"""
        resultado = self.modelo.mover_hormiga(delta_fila, delta_col)
        
        if resultado == 'invalido':
            self.vista.mostrar_mensaje('warning', "Movimiento inválido", "No puedes salir del tablero!")
            return False
        elif resultado == 'veneno':
            self.vista.mostrar_mensaje('error', "¡Game Over!", "¡La hormiga tocó veneno! 💀")
            self.reiniciar_juego()
            return False
        elif resultado == 'meta':
            self.actualizar_vista()
            self.vista.mostrar_mensaje('info', "¡Felicidades!", "¡La hormiga llegó a la meta! 🎉")
            return True
        else:  # exito
            self.actualizar_vista()
            return True
    
    def reiniciar_juego(self):
        """Reinicia el juego a la posición inicial"""
        self.modelo.reiniciar_posicion_hormiga()
        self.actualizar_vista()
    
    def abrir_configurador(self):
        """Abre el configurador de tamaño del tablero"""
        def callback_cambio_tamaño(nuevas_filas, nuevas_cols):
            self.modelo.cambiar_tamaño(nuevas_filas, nuevas_cols)
            self.vista.recrear_tablero(nuevas_filas, nuevas_cols)
            self.actualizar_vista()
        
        self.vista.abrir_configurador_tamaño(
            self.modelo.filas, 
            self.modelo.columnas, 
            callback_cambio_tamaño
        )
    
    def generar_tablero_aleatorio(self):
        """Genera un tablero aleatorio"""
        self.modelo.generar_tablero_aleatorio()
        self.actualizar_vista()
        self.vista.mostrar_mensaje('info', "Tablero Generado", 
                                 f"Nuevo tablero aleatorio {self.modelo.filas}x{self.modelo.columnas} generado!")
    
    def cargar_desde_archivo(self):
        """Carga configuración desde archivo"""
        archivo = self.vista.abrir_dialogo_archivo('abrir')
        if not archivo:
            return
        
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            configuracion = self.archivo_manager.parsear_configuracion_completa(contenido)
            
            if not configuracion:
                self.vista.mostrar_mensaje('error', "Error", "No se pudo parsear el archivo. Verifica el formato.")
                return
            
            # Validar coordenadas
            coordenadas_validas, coordenadas_invalidas = self._validar_configuracion(configuracion)
            
            if not coordenadas_validas:
                self.vista.mostrar_mensaje('error', "Error", "No hay coordenadas válidas en el archivo.")
                return
            
            # Aplicar configuración
            self.modelo.aplicar_configuracion_desde_archivo(coordenadas_validas)
            self.actualizar_vista()
            
            # Mostrar resultado
            mensaje = f"Configuración cargada exitosamente!\n\n"
            mensaje += f"🐜 Hormiga: {tuple(coordenadas_validas['inicio'])}\n"
            mensaje += f"🍃 Meta: {tuple(coordenadas_validas['meta'])}\n"
            mensaje += f"☠️ Venenos: {len(coordenadas_validas['venenos'])} posiciones\n"
            
            if coordenadas_invalidas > 0:
                mensaje += f"⚠️ Coordenadas inválidas ignoradas: {coordenadas_invalidas}"
            
            self.vista.mostrar_mensaje('info', "Carga Completada", mensaje)
            
        except Exception as e:
            self.vista.mostrar_mensaje('error', "Error", f"Error al cargar el archivo:\n{str(e)}")
    
    def _validar_configuracion(self, configuracion):
        """Valida las coordenadas de la configuración"""
        coordenadas_validas = {
            'inicio': None,
            'meta': None,
            'venenos': []
        }
        coordenadas_invalidas = 0
        
        # Validar inicio
        if self.modelo.es_coordenada_valida(configuracion['inicio']):
            coordenadas_validas['inicio'] = configuracion['inicio']
        else:
            return None, 0
        
        # Validar meta
        if self.modelo.es_coordenada_valida(configuracion['meta']):
            coordenadas_validas['meta'] = configuracion['meta']
        else:
            return None, 0
        
        # Validar venenos
        for veneno in configuracion['venenos']:
            if (self.modelo.es_coordenada_valida(veneno) and 
                veneno != configuracion['inicio'] and 
                veneno != configuracion['meta']):
                coordenadas_validas['venenos'].append(veneno)
            else:
                coordenadas_invalidas += 1
        
        return coordenadas_validas, coordenadas_invalidas
    
    def crear_archivo_ejemplo(self):
        """Crea un archivo de ejemplo"""
        archivo = self.vista.abrir_dialogo_archivo('guardar')
        if not archivo:
            return
        
        try:
            contenido_ejemplo = self.archivo_manager.crear_archivo_ejemplo(
                self.modelo.filas, self.modelo.columnas
            )
            
            with open(archivo, 'w', encoding='utf-8') as f:
                f.write(contenido_ejemplo)
            
            self.vista.mostrar_mensaje('info', "Archivo Creado", f"Archivo de ejemplo creado en:\n{archivo}")
            
        except Exception as e:
            self.vista.mostrar_mensaje('error', "Error", f"Error al crear el archivo:\n{str(e)}")
    
    def click_celda(self, fila, col):
        """Maneja el click en una celda (para futuras funcionalidades)"""
        # Placeholder para funcionalidades futuras como edición manual
        pass
    
    def simular_ruta_ejemplo(self):
        """Simula una ruta de ejemplo"""
        def encontrar_ruta_simple():
            """Encuentra una ruta simple evitando venenos"""
            ruta = []
            pos_actual = self.modelo.pos_hormiga.copy()
            
            # Movimiento simple: primero horizontal, luego vertical
            while pos_actual[1] < self.modelo.pos_meta[1]:
                if (pos_actual[1] + 1 < self.modelo.columnas and 
                    self.modelo.tablero[pos_actual[0]][pos_actual[1] + 1] != 'veneno'):
                    pos_actual[1] += 1
                    ruta.append((0, 1))  # Mover derecha
                else:
                    break
            
            while pos_actual[0] < self.modelo.pos_meta[0]:
                if (pos_actual[0] + 1 < self.modelo.filas and 
                    self.modelo.tablero[pos_actual[0] + 1][pos_actual[1]] != 'veneno'):
                    pos_actual[0] += 1
                    ruta.append((1, 0))  # Mover abajo
                else:
                    break
            
            return ruta
        
        def ejecutar_ruta():
            """Ejecuta la ruta encontrada"""
            self.reiniciar_juego()
            time.sleep(1)
            
            ruta_ejemplo = encontrar_ruta_simple()
            
            for delta_fila, delta_col in ruta_ejemplo:
                # Usar after para ejecutar en el hilo principal
                self.vista.root.after(0, lambda df=delta_fila, dc=delta_col: self.mover_hormiga(df, dc))
                time.sleep(0.8)
        
        # Ejecutar en hilo separado
        thread = Thread(target=ejecutar_ruta)
        thread.daemon = True
        thread.start()
    
    def simular_movimientos_automaticos(self, lista_movimientos):
        """
        Método para integrar lógica de backend.
        Recibe lista de tuplas (delta_fila, delta_col)
        """
        def ejecutar_movimientos():
            for delta_fila, delta_col in lista_movimientos:
                if not self.mover_hormiga(delta_fila, delta_col):
                    break
                time.sleep(0.5)
        
        thread = Thread(target=ejecutar_movimientos)
        thread.daemon = True
        thread.start()
    
    def obtener_movimientos_posibles(self):
        """Retorna movimientos posibles (para algoritmos de pathfinding)"""
        return self.modelo.obtener_movimientos_posibles()
    
    def obtener_posicion_hormiga(self):
        """Retorna posición actual de la hormiga"""
        return self.modelo.pos_hormiga.copy()
    
    def obtener_estado_completo(self):
        """Retorna estado completo del juego"""
        return self.modelo.obtener_estado_tablero()
