import tkinter as tk
from tkinter import ttk
from config import CONFIG_TABLAS

class ServicioView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.widgets = {}
        self.crear_widgets()

    def crear_widgets(self):
        config = CONFIG_TABLAS['servicios']
        row = 0

        # Título
        titulo_frame = ttk.Frame(self.parent)
        titulo_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(titulo_frame, text=config['titulo'], style='Title.TLabel').pack()

        # Frame para contenido
        contenido_frame = ttk.Frame(self.parent)
        contenido_frame.pack(fill=tk.BOTH, expand=True)

        # Frame del formulario
        form_frame = ttk.LabelFrame(contenido_frame, text="📋 FORMULARIO", padding="15")
        form_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Crear campos
        self.widgets = {}
        for campo, config_campo in config['campos'].items():
            campo_frame = ttk.Frame(form_frame)
            campo_frame.grid(row=row, column=0, columnspan=2, sticky='ew', pady=3)

            label = ttk.Label(campo_frame, text=config_campo['label'] + ":", width=22, anchor='e',
                              font=('Arial', 10))
            label.pack(side=tk.LEFT, padx=(0, 10))

            if config_campo['tipo'] == 'entry':
                widget = ttk.Entry(campo_frame, width=32, font=('Arial', 10))
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

            self.widgets[campo] = widget
            row += 1

        # Frame de botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        botones = [
            ("💾 GUARDAR", self.controller.guardar),
            ("🔄 ACTUALIZAR", self.controller.actualizar),
            ("🔍 BUSCAR", self.controller.buscar),
            ("🗑️ ELIMINAR", self.controller.eliminar),
            ("🧹 LIMPIAR", self.controller.limpiar),
            ("📊 EXPORTAR EXCEL", self.controller.exportar_excel)
        ]

        for i, (texto, comando) in enumerate(botones):
            btn = tk.Button(button_frame, text=texto, bg=self.controller.get_color_boton(texto.split()[1].lower()),
                            fg='white', font=('Arial', 10, 'bold'), padx=12, pady=6,
                            relief=tk.RAISED, bd=2, cursor='hand2')
            btn.grid(row=0, column=i, padx=5)
            btn.config(command=comando)

    def obtener_valores(self):
        valores = {}
        for campo, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry):
                valores[campo] = widget.get()
        return valores

    def limpiar_formulario(self):
        for widget in self.widgets.values():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)

    def mostrar_datos(self, servicio):
        # servicio: (id_servicio, nombre, descripcion)
        self.widgets['nombre'].delete(0, tk.END)
        self.widgets['nombre'].insert(0, servicio[1] if servicio[1] else "")

        self.widgets['descripcion'].delete(0, tk.END)
        self.widgets['descripcion'].insert(0, servicio[2] if servicio[2] else "")

    def ventana_buscar(self):
        ventana_buscar = tk.Toplevel(self.parent)
        ventana_buscar.title("Buscar Servicio")
        ventana_buscar.geometry("500x300")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.parent)
        ventana_buscar.grab_set()

        ttk.Label(ventana_buscar, text="Ingrese el nombre del servicio:",
                  style='Header.TLabel').pack(pady=10)

        entry_nombre = ttk.Entry(ventana_buscar, width=40, font=('Arial', 12))
        entry_nombre.pack(pady=10)
        entry_nombre.focus()

        # Listbox para resultados
        frame_resultados = ttk.Frame(ventana_buscar)
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame_resultados)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame_resultados, yscrollcommand=scrollbar.set,
                             font=('Arial', 11), selectmode=tk.SINGLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=listbox.yview)

        def realizar_busqueda(event=None):
            nombre = entry_nombre.get().strip()
            if not nombre:
                return
            self.controller.buscar_servicios(nombre, listbox)

        def seleccionar_servicio(event):
            if not listbox.curselection():
                return
            index = listbox.curselection()[0]
            servicio = listbox.resultados[index]
            self.controller.mostrar_servicio(servicio)
            ventana_buscar.destroy()

        entry_nombre.bind('<KeyRelease>', realizar_busqueda)
        listbox.bind('<Double-Button-1>', seleccionar_servicio)

        btn_cerrar = ttk.Button(ventana_buscar, text="Cerrar",
                                command=ventana_buscar.destroy)
        btn_cerrar.pack(pady=10)

        return ventana_buscar, entry_nombre, listbox
