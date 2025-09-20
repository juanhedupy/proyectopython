import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os


class SistemaFormulariosCompleto:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Eventos - Formularios Completos")
        self.root.geometry("1300x750")
        self.root.configure(bg='#f0f8ff')

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')

        # Diccionario de configuración COMPLETAMENTE ADAPTADO a tu BD
        self.config_tablas = {
            'clientes': {
                'campos': {
                    'identificacion': {'tipo': 'entry', 'label': 'Identificación *', 'editable': True},
                    'foto': {'tipo': 'imagen', 'label': 'Foto', 'editable': True},
                    'nombre': {'tipo': 'entry', 'label': 'Nombre Completo *', 'editable': True},
                    'telefono': {'tipo': 'entry', 'label': 'Teléfono', 'editable': True},
                    'email': {'tipo': 'entry', 'label': 'Email', 'editable': True},
                    'direccion': {'tipo': 'entry', 'label': 'Dirección', 'editable': True}
                },
                'titulo': '👥 GESTIÓN DE CLIENTES',
                'campos_ocultos': ['id_cliente']
            },
            'servicios': {
                'campos': {
                    'nombre': {'tipo': 'entry', 'label': 'Nombre del Servicio *', 'editable': True},
                    'descripcion': {'tipo': 'entry', 'label': 'Descripción *', 'editable': True}
                },
                'titulo': '🔧 GESTIÓN DE SERVICIOS',
                'campos_ocultos': ['id_servicio']
            },
            'proveedores': {
                'campos': {
                    'identificacion': {'tipo': 'entry', 'label': 'Identificación *', 'editable': True},
                    'nombre': {'tipo': 'entry', 'label': 'Nombre del Proveedor *', 'editable': True},
                    'telefono': {'tipo': 'entry', 'label': 'Teléfono', 'editable': True},
                    'email': {'tipo': 'entry', 'label': 'Email', 'editable': True}
                },
                'titulo': '🏢 GESTIÓN DE PROVEEDORES',
                'campos_ocultos': ['id_proveedor']
            },
            'servicio_proveedor': {
                'campos': {
                    'id_servicio': {'tipo': 'combobox', 'label': 'Servicio *', 'editable': True,
                                    'valores': []},  # Se llenará desde BD
                    'id_proveedor': {'tipo': 'combobox', 'label': 'Proveedor *', 'editable': True,
                                     'valores': []},  # Se llenará desde BD
                    'precio': {'tipo': 'entry', 'label': 'Precio ($) *', 'editable': True}
                },
                'titulo': '💰 SERVICIO - PROVEEDOR',
                'campos_ocultos': ['id_servicio_proveedor']
            },
            'recintos': {
                'campos': {
                    'nombre': {'tipo': 'entry', 'label': 'Nombre del Recinto *', 'editable': True},
                    'foto': {'tipo': 'imagen', 'label': 'Foto', 'editable': True},
                    'ubicacion': {'tipo': 'entry', 'label': 'Ubicación *', 'editable': True},
                    'capacidad': {'tipo': 'entry', 'label': 'Capacidad (personas) *', 'editable': True},
                    'tipo': {'tipo': 'entry', 'label': 'Tipo de Recinto *', 'editable': True},  # VARCHAR
                    'tarifa_hora': {'tipo': 'entry', 'label': 'Tarifa por Hora ($) *', 'editable': True},
                    'caracteristicas': {'tipo': 'text', 'label': 'Características', 'editable': True}  # TEXT
                },
                'titulo': '🏟️ GESTIÓN DE RECINTOS',
                'campos_ocultos': ['id_recinto']
            },
            'eventos': {
                'campos': {
                    'id_recinto': {'tipo': 'combobox', 'label': 'Recinto *', 'editable': True,
                                   'valores': []},  # Se llenará desde BD
                    'id_cliente': {'tipo': 'combobox', 'label': 'Cliente *', 'editable': True,
                                   'valores': []},  # Se llenará desde BD
                    'titulo': {'tipo': 'entry', 'label': 'Título del Evento *', 'editable': True},  # VARCHAR
                    'tipo': {'tipo': 'entry', 'label': 'Tipo de Evento *', 'editable': True},  # VARCHAR
                    'fecha_hora_inicio': {'tipo': 'datetime', 'label': 'Fecha/Hora Inicio *', 'editable': True},
                    # DATETIME
                    'fecha_hora_fin': {'tipo': 'datetime', 'label': 'Fecha/Hora Fin *', 'editable': True},  # DATETIME
                    'asistentes_estimados': {'tipo': 'entry', 'label': 'Asistentes Estimados', 'editable': True},  # INT
                    'estado': {'tipo': 'combobox', 'label': 'Estado *', 'editable': True,
                               'valores': ['Planificado', 'Confirmado', 'En curso', 'Completado', 'Cancelado']},
                    # VARCHAR con opciones
                    'descripcion': {'tipo': 'entry', 'label': 'Descripción', 'editable': True},  # VARCHAR(200)
                    'costo': {'tipo': 'entry', 'label': 'Costo Total ($) *', 'editable': True}  # DECIMAL
                },
                'titulo': '🎉 GESTIÓN DE EVENTOS',
                'campos_ocultos': ['id_evento']
            },
            'eventos_servicios': {
                'campos': {
                    'id_evento': {'tipo': 'combobox', 'label': 'Evento *', 'editable': True,
                                  'valores': []},  # Se llenará desde BD
                    'id_servicio_proveedor': {'tipo': 'combobox', 'label': 'Servicio-Proveedor *', 'editable': True,
                                              'valores': []}  # Se llenará desde BD
                },
                'titulo': '🔗 ASIGNAR SERVICIOS A EVENTOS',
                'campos_ocultos': []
            }
        }

        self.tabla_actual = None
        self.widgets = {}
        self.imagen_actual = None
        self.ruta_imagen_actual = None
        self.img_label = None  # Inicializar img_label como None

        self.crear_interfaz()

    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame de selección de tabla
        selector_frame = ttk.Frame(main_frame)
        selector_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(selector_frame, text="SELECCIONAR TABLA:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))

        self.tabla_var = tk.StringVar()
        tablas = list(self.config_tablas.keys())
        tabla_combo = ttk.Combobox(selector_frame, textvariable=self.tabla_var, values=tablas,
                                   state="readonly", width=25, font=('Arial', 10, 'bold'))
        tabla_combo.pack(side=tk.LEFT, padx=5)
        tabla_combo.bind('<<ComboboxSelected>>', self.cambiar_tabla)

        # Frame para formulario
        self.contenedor_formulario = ttk.Frame(main_frame)
        self.contenedor_formulario.pack(fill=tk.BOTH, expand=True)

        # Inicializar con la primera tabla
        if tablas:
            self.tabla_var.set(tablas[0])
            self.cambiar_tabla()

    def cambiar_tabla(self, event=None):
        # Limpiar contenedor anterior
        for widget in self.contenedor_formulario.winfo_children():
            widget.destroy()

        tabla = self.tabla_var.get()
        self.tabla_actual = tabla
        config = self.config_tablas[tabla]

        # Título
        titulo_frame = ttk.Frame(self.contenedor_formulario)
        titulo_frame.pack(fill=tk.X, pady=(0, 15))

        title_label = ttk.Label(titulo_frame, text=config['titulo'], style='Title.TLabel')
        title_label.pack()

        # Frame para contenido
        contenido_frame = ttk.Frame(self.contenedor_formulario)
        contenido_frame.pack(fill=tk.BOTH, expand=True)

        # Frame del formulario
        form_frame = ttk.LabelFrame(contenido_frame, text="📋 FORMULARIO", padding="15")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Frame para preview de imagen (solo para tablas con foto)
        self.preview_frame = ttk.LabelFrame(contenido_frame, text="🖼️ VISTA PREVIA", padding="15")
        if 'foto' in config['campos']:
            self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0), pady=5)
            self.preview_frame.configure(width=250)

            # Crear label para imagen
            self.img_label = ttk.Label(self.preview_frame, text="Imagen no seleccionada",
                                       background='white', anchor='center', justify='center',
                                       font=('Arial', 9))
            self.img_label.pack(fill=tk.BOTH, expand=True)
        else:
            # Ocultar frame de preview si no hay campo de imagen
            self.preview_frame.pack_forget()
            self.img_label = None  # Asegurar que img_label sea None

        # Crear campos del formulario
        self.widgets[tabla] = {}
        row = 0

        for campo, config_campo in config['campos'].items():
            campo_frame = ttk.Frame(form_frame)
            campo_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=3)

            # Label
            label = ttk.Label(campo_frame, text=config_campo['label'] + ":", width=22, anchor='e',
                              font=('Arial', 10))
            label.pack(side=tk.LEFT, padx=(0, 10))

            # Widget según el tipo
            if config_campo['tipo'] == 'entry':
                widget = ttk.Entry(campo_frame, width=32, font=('Arial', 10))
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

            elif config_campo['tipo'] == 'combobox':
                valores = config_campo.get('valores', [])
                widget = ttk.Combobox(campo_frame, values=valores, width=30,
                                      state="readonly", font=('Arial', 10))
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

            elif config_campo['tipo'] == 'datetime':
                widget = DateEntry(campo_frame, width=29, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',
                                   font=('Arial', 10))
                widget.pack(side=tk.LEFT)

            elif config_campo['tipo'] == 'text':
                widget = tk.Text(campo_frame, width=32, height=4, font=('Arial', 10))
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

            elif config_campo['tipo'] == 'imagen':
                btn_frame = ttk.Frame(campo_frame)
                btn_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

                widget = ttk.Entry(btn_frame, width=22, font=('Arial', 10))
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

                btn_buscar = ttk.Button(btn_frame, text="Examinar",
                                        command=lambda w=widget: self.seleccionar_imagen(w))
                btn_buscar.pack(side=tk.LEFT)

            self.widgets[tabla][campo] = widget
            row += 1

        # Frame de botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        # Botones (solo visuales, sin funcionalidad aún)
        botones = [
            ("💾 GUARDAR", "#27ae60", self.guardar),
            ("🔄 ACTUALIZAR", "#3498db", self.actualizar),
            ("🔍 BUSCAR", "#f39c12", self.buscar),
            ("🗑️ ELIMINAR", "#e74c3c", self.eliminar),
            ("🧹 LIMPIAR", "#95a5a6", self.limpiar_formulario)
        ]

        for i, (texto, color, comando) in enumerate(botones):
            btn = tk.Button(button_frame, text=texto, bg=color, fg='white',
                            font=('Arial', 10, 'bold'), padx=12, pady=6,
                            relief=tk.RAISED, bd=2, cursor='hand2')
            btn.grid(row=0, column=i, padx=5)
            btn.bind('<Button-1>', lambda e, cmd=comando: cmd())

    def seleccionar_imagen(self, entry_widget):
        # Función placeholder para selección de imagen (sin implementar)
        messagebox.showinfo("Seleccionar Imagen", "Función de selección de imagen será implementada")
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, "ruta/a/imagen.jpg")
        self.mostrar_imagen("ruta/a/imagen.jpg")

    def mostrar_imagen(self, ruta_imagen):
        # Función placeholder para mostrar imagen (sin implementar)
        if self.img_label:
            self.img_label.configure(text="Imagen: " + os.path.basename(ruta_imagen))

    def guardar(self):
        # Función placeholder para guardar (sin implementar)
        messagebox.showinfo("Guardar", f"Función guardar para {self.tabla_actual} será implementada")

    def actualizar(self):
        # Función placeholder para actualizar (sin implementar)
        messagebox.showinfo("Actualizar", f"Función actualizar para {self.tabla_actual} será implementada")

    def buscar(self):
        # Función placeholder para buscar (sin implementar)
        messagebox.showinfo("Buscar", f"Función buscar para {self.tabla_actual} será implementada")

    def eliminar(self):
        # Función placeholder para eliminar (sin implementar)
        messagebox.showinfo("Eliminar", f"Función eliminar para {self.tabla_actual} será implementada")

    def limpiar_formulario(self):
        # Limpiar todos los campos del formulario actual
        tabla = self.tabla_actual
        for campo, widget in self.widgets[tabla].items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, DateEntry):
                widget.set_date(None)  # Limpiar fecha
            elif isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)

        # Solo limpiar imagen si existe el label y la tabla tiene campo de foto
        if self.img_label and 'foto' in self.config_tablas[tabla]['campos']:
            self.img_label.configure(image='', text="Imagen no seleccionada")
            self.ruta_imagen_actual = None


# Función principal
def main():
    root = tk.Tk()
    app = SistemaFormulariosCompleto(root)
    root.mainloop()


if __name__ == "__main__":
    main()