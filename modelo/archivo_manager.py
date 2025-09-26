"""
Modelo - Maneja la carga y guardado de archivos de configuración
"""

import re

class ArchivoManager:
    @staticmethod
    def parsear_configuracion_completa(contenido):
        """
        Parsea configuración completa desde texto.
        Formato: 1. Hormiga, 2. Meta, 3+ Venenos
        """
        coordenadas = ArchivoManager.extraer_coordenadas_del_texto(contenido)
        
        if len(coordenadas) < 2:
            return None
        
        inicio = coordenadas[0]
        meta = coordenadas[1]
        venenos = coordenadas[2:] if len(coordenadas) > 2 else []
        
        return {
            'inicio': inicio,
            'meta': meta,
            'venenos': venenos
        }
    
    @staticmethod
    def extraer_coordenadas_del_texto(contenido):
        """Extrae todas las coordenadas del texto en orden"""
        coordenadas = []
        lineas = contenido.split('\n')
        
        for linea in lineas:
            linea = linea.strip()
            if not linea or linea.startswith('#'):
                continue
            
            coord = ArchivoManager.extraer_primera_coordenada(linea)
            if coord:
                coordenadas.append(coord)
        
        return coordenadas
    
    @staticmethod
    def extraer_primera_coordenada(texto):
        """Extrae la primera coordenada encontrada en un texto"""
        patrones = [
            r'$$\s*(\d+)\s*,\s*(\d+)\s*$$',  # (x,y)
            r'(\d+)\s*,\s*(\d+)',            # x,y
            r'(\d+)\s+(\d+)'                 # x y
        ]
        
        for patron in patrones:
            match = re.search(patron, texto)
            if match:
                try:
                    x, y = int(match.group(1)), int(match.group(2))
                    return (x, y)
                except ValueError:
                    continue
        
        return None
    
    @staticmethod
    def crear_archivo_ejemplo(filas, columnas):
        """Crea contenido de ejemplo para archivo de configuración"""
        return f"""# Archivo de configuración para Hormiga vs Venenos
# Formato: (fila, columna) donde las coordenadas empiezan desde (0, 0)
# 
# ORDEN OBLIGATORIO:
# 1. Primera coordenada: Posición inicial de la hormiga
# 2. Segunda coordenada: Posición de la meta
# 3. Coordenadas siguientes: Posiciones de los venenos
#
# Ejemplo para tablero {filas}x{columnas}:

# Posición inicial de la hormiga
(0, 0)

# Posición de la meta
({filas-1}, {columnas-1})

# Posiciones de los venenos
(1, 0)
(2, 0)
(1, 3)
(3, 1)
(4, 2)

# También puedes usar otros formatos:
# 1, 2
# 2 3
# (3, 4)

# Líneas que empiecen con # son comentarios y se ignoran
# Las coordenadas deben estar dentro del rango del tablero actual
"""
