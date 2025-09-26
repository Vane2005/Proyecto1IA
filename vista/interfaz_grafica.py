"""
Vista - Maneja la interfaz gráfica y la presentación visual
"""

import tkinter as tk
from tkinter import messagebox, ttk, filedialog

class InterfazGrafica:
    def __init__(self):
        self.controlador = None
        self.root = tk.Tk()
        self.root.title("Hormiga vs Venenos - Interfaz MVC")
        self.root.configure(bg='#f0f0f0')
        
        # Colores y símbolos
        self.colores = {
            'inicio': '#FFA500',    # Naranja
            'libre': '#FFFFFF',     # Blanco
            'veneno': '#FF0000',    # Rojo
            'meta': '#00FF00',      # Verde
            'hormiga': '#8B4513'    # Marrón para la hormiga
        }
        
        self.simbolos = {
            'inicio': '🐜',
            'libre': '',
            'veneno': '☠️',
            'meta': '🍃',
            'hormiga': '🐜'
        }
        
        self.botones = []
        self.frame_tablero = None
        self.label_estado = None
    
    def asignar_controlador(self, controlador):
        """Asigna el controlador a la vista"""
        self.controlador = controlador
        
    def crear_interfaz(self, filas, columnas):
        """Crea la interfaz gráfica completa"""
        # Configurar ventana
        tamaño_celda = max(60, min(100, 500 // max(filas, columnas)))
        ancho_ventana = max(600, columnas * tamaño_celda + 100)
        alto_ventana = max(700, filas * tamaño_celda + 400)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")
        
        # Título
        titulo = tk.Label(self.root, 
                         text=f"Hormiga vs Venenos - Tablero {filas}x{columnas}", 
                         font=('Arial', 16, 'bold'), bg='#f0f0f0')
        titulo.pack(pady=10)
        
        # Frame de configuración
        self._crear_frame_configuracion()
        
        # Frame del tablero
        self._crear_frame_tablero(filas, columnas)
        
        # Frame de controles
        self._crear_frame_controles()
        
        # Estado
        self.label_estado = tk.Label(self.root, text="", 
                                   font=('Arial', 11), bg='#f0f0f0')
        self.label_estado.pack(pady=10)
        
        # Leyenda
        self._crear_leyenda()
    
    def _crear_frame_configuracion(self):
        """Crea el frame con botones de configuración"""
        frame_config = tk.Frame(self.root, bg='#f0f0f0')
        frame_config.pack(pady=5)
        
        botones_config = [
            ("Configurar Tablero", lambda: self.controlador.abrir_configurador() if self.controlador else None, '#2196F3'),
            ("Tablero Aleatorio", lambda: self.controlador.generar_tablero_aleatorio() if self.controlador else None, '#FF9800'),
            ("Cargar Configuración", lambda: self.controlador.cargar_desde_archivo() if self.controlador else None, '#9C27B0'),
            ("Crear Ejemplo", lambda: self.controlador.crear_archivo_ejemplo() if self.controlador else None, '#607D8B')
        ]
        
        for texto, comando, color in botones_config:
            tk.Button(frame_config, text=texto, command=comando,
                     bg=color, fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    
    def _crear_frame_tablero(self, filas, columnas):
        """Crea el frame del tablero con botones"""
        if self.frame_tablero:
            self.frame_tablero.destroy()
        
        self.frame_tablero = tk.Frame(self.root, bg='#f0f0f0')
        self.frame_tablero.pack(pady=10)
        
        self.botones = []
        for i in range(filas):
            fila_botones = []
            for j in range(columnas):
                btn = tk.Button(self.frame_tablero, 
                              width=max(4, 8-max(filas, columnas)//2), 
                              height=max(2, 4-max(filas, columnas)//3),
                              font=('Arial', max(8, 14-max(filas, columnas)//2)),
                              relief='solid',
                              borderwidth=2,
                              command=lambda r=i, c=j: self.controlador.click_celda(r, c) if self.controlador else None)
                btn.grid(row=i, column=j, padx=1, pady=1)
                fila_botones.append(btn)
            self.botones.append(fila_botones)
    
    def _crear_frame_controles(self):
        """Crea el frame con controles de movimiento"""
        frame_controles = tk.Frame(self.root, bg='#f0f0f0')
        frame_controles.pack(pady=20)
        
        # Movimiento manual
        tk.Label(frame_controles, text="Movimiento Manual:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack()
        
        frame_direcciones = tk.Frame(frame_controles, bg='#f0f0f0')
        frame_direcciones.pack(pady=10)
        
        # Botones direccionales
        tk.Button(frame_direcciones, text="↑", 
                 command=lambda: self.controlador.mover_hormiga(-1, 0) if self.controlador else None,
                 width=3, height=1, font=('Arial', 14)).grid(row=0, column=1)
        tk.Button(frame_direcciones, text="←", 
                 command=lambda: self.controlador.mover_hormiga(0, -1) if self.controlador else None,
                 width=3, height=1, font=('Arial', 14)).grid(row=1, column=0)
        tk.Button(frame_direcciones, text="→", 
                 command=lambda: self.controlador.mover_hormiga(0, 1) if self.controlador else None,
                 width=3, height=1, font=('Arial', 14)).grid(row=1, column=2)
        tk.Button(frame_direcciones, text="↓", 
                 command=lambda: self.controlador.mover_hormiga(1, 0) if self.controlador else None,
                 width=3, height=1, font=('Arial', 14)).grid(row=2, column=1)
        
        # Separador
        tk.Label(frame_controles, text="", bg='#f0f0f0').pack(pady=5)
        
        # Simulación automática
        tk.Label(frame_controles, text="Simulación Automática:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack()
        
        frame_auto = tk.Frame(frame_controles, bg='#f0f0f0')
        frame_auto.pack(pady=10)
        
        tk.Button(frame_auto, text="Ejemplo de Ruta", 
                 command=lambda: self.controlador.simular_ruta_ejemplo() if self.controlador else None,
                 bg='#4CAF50', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_auto, text="Reiniciar", 
                 command=lambda: self.controlador.reiniciar_juego() if self.controlador else None,
                 bg='#f44336', fg='white', font=('Arial', 10)).pack(side=tk.LEFT, padx=5)
    
    def _crear_leyenda(self):
        """Crea la leyenda de colores"""
        frame_leyenda = tk.Frame(self.root, bg='#f0f0f0')
        frame_leyenda.pack(pady=10)
        
        tk.Label(frame_leyenda, text="Leyenda:", font=('Arial', 12, 'bold'), bg='#f0f0f0').pack()
        
        leyenda_items = [
            ("🐜 Inicio (Hormiga)", '#FFA500'),
            ("🍃 Meta (Hoja)", '#00FF00'),
            ("☠️ Obstáculo (Veneno)", '#FF0000')
        ]
        
        for texto, color in leyenda_items:
            frame_item = tk.Frame(frame_leyenda, bg='#f0f0f0')
            frame_item.pack(side=tk.LEFT, padx=10)
            
            tk.Label(frame_item, text="  ", bg=color, relief='solid', borderwidth=1).pack(side=tk.LEFT)
            tk.Label(frame_item, text=texto, font=('Arial', 9), bg='#f0f0f0').pack(side=tk.LEFT, padx=5)
    
    def actualizar_tablero(self, estado_tablero):
        """Actualiza la visualización del tablero"""
        filas = estado_tablero['filas']
        columnas = estado_tablero['columnas']
        tablero = estado_tablero['tablero']
        pos_hormiga = estado_tablero['pos_hormiga']
        
        for i in range(filas):
            for j in range(columnas):
                tipo_celda = tablero[i][j]
                btn = self.botones[i][j]
                
                # Si la hormiga está en esta posición
                if [i, j] == pos_hormiga:
                    btn.configure(
                        bg=self.colores['hormiga'],
                        text=self.simbolos['hormiga'],
                        fg='white'
                    )
                else:
                    btn.configure(
                        bg=self.colores[tipo_celda],
                        text=self.simbolos[tipo_celda],
                        fg='black' if tipo_celda != 'veneno' else 'white'
                    )
        
        # Actualizar estado
        fila, col = pos_hormiga
        self.label_estado.configure(text=f"Posición de la hormiga: ({fila}, {col})")
    
    def recrear_tablero(self, filas, columnas):
        """Recrea el tablero con nuevo tamaño"""
        # Actualizar título
        self.root.title(f"Hormiga vs Venenos - Tablero {filas}x{columnas}")
        
        # Recrear frame del tablero
        self._crear_frame_tablero(filas, columnas)
        
        # Redimensionar ventana
        tamaño_celda = max(60, min(100, 500 // max(filas, columnas)))
        ancho_ventana = max(600, columnas * tamaño_celda + 100)
        alto_ventana = max(700, filas * tamaño_celda + 400)
        self.root.geometry(f"{ancho_ventana}x{alto_ventana}")
    
    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """Muestra mensajes al usuario"""
        if tipo == 'info':
            messagebox.showinfo(titulo, mensaje)
        elif tipo == 'warning':
            messagebox.showwarning(titulo, mensaje)
        elif tipo == 'error':
            messagebox.showerror(titulo, mensaje)
    
    def abrir_dialogo_archivo(self, modo='abrir'):
        """Abre diálogo para seleccionar archivo"""
        if modo == 'abrir':
            return filedialog.askopenfilename(
                title="Seleccionar archivo de configuración",
                filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
            )
        else:  # guardar
            return filedialog.asksaveasfilename(
                title="Guardar archivo de ejemplo",
                defaultextension=".txt",
                filetypes=[("Archivos de texto", "*.txt")]
            )
    
    def abrir_configurador_tamaño(self, filas_actual, columnas_actual, callback):
        """Abre ventana de configuración de tamaño"""
        config_window = tk.Toplevel(self.root)
        config_window.title("Configurar Tablero")
        config_window.geometry("400x300")
        config_window.configure(bg='#f0f0f0')
        
        # Configuración de tamaño
        tk.Label(config_window, text="Tamaño del Tablero:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=10)
        
        frame_tamaño = tk.Frame(config_window, bg='#f0f0f0')
        frame_tamaño.pack(pady=5)
        
        tk.Label(frame_tamaño, text="Filas:", bg='#f0f0f0').pack(side=tk.LEFT)
        filas_var = tk.StringVar(value=str(filas_actual))
        tk.Entry(frame_tamaño, textvariable=filas_var, width=5).pack(side=tk.LEFT, padx=5)
        
        tk.Label(frame_tamaño, text="Columnas:", bg='#f0f0f0').pack(side=tk.LEFT, padx=(10,0))
        cols_var = tk.StringVar(value=str(columnas_actual))
        tk.Entry(frame_tamaño, textvariable=cols_var, width=5).pack(side=tk.LEFT, padx=5)
        
        # Botones predefinidos
        tk.Label(config_window, text="Tamaños Predefinidos:", 
                font=('Arial', 12, 'bold'), bg='#f0f0f0').pack(pady=(20,5))
        
        frame_predefinidos = tk.Frame(config_window, bg='#f0f0f0')
        frame_predefinidos.pack(pady=5)
        
        tamaños = [(3,3), (4,4), (5,5), (6,6), (8,8), (10,10)]
        for i, (f, c) in enumerate(tamaños):
            if i % 3 == 0:
                fila_frame = tk.Frame(frame_predefinidos, bg='#f0f0f0')
                fila_frame.pack(pady=2)
            
            tk.Button(fila_frame, text=f"{f}x{c}", 
                     command=lambda ff=f, cc=c: [filas_var.set(str(ff)), cols_var.set(str(cc))],
                     width=6).pack(side=tk.LEFT, padx=2)
        
        # Botón aplicar
        def aplicar_cambios():
            try:
                nuevas_filas = int(filas_var.get())
                nuevas_cols = int(cols_var.get())
                
                if 2 <= nuevas_filas <= 20 and 2 <= nuevas_cols <= 20:
                    callback(nuevas_filas, nuevas_cols)
                    config_window.destroy()
                else:
                    messagebox.showerror("Error", "El tamaño debe estar entre 2x2 y 20x20")
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa números válidos")
        
        tk.Button(config_window, text="Aplicar Cambios", 
                 command=aplicar_cambios,
                 bg='#4CAF50', fg='white', font=('Arial', 12)).pack(pady=20)
    
    def ejecutar(self):
        """Inicia la aplicación"""
        self.root.mainloop()
