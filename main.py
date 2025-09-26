"""
Punto de entrada principal - Inicializa la aplicación usando el patrón MVC
"""

from vista.interfaz_grafica import InterfazGrafica
from controlador.juego_controlador import JuegoControlador

def main():
    """Función principal que inicializa la aplicación"""
    print("Iniciando Hormiga vs Venenos con arquitectura MVC...")
    
    vista = InterfazGrafica()
    
    controlador = JuegoControlador(vista)
    
    vista.asignar_controlador(controlador)
    
    controlador.inicializar_interfaz()
    
    # Ejecutar aplicación
    vista.ejecutar()

if __name__ == "__main__":
    main()
