import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from config import CONFIG_TABLAS

class RecintoView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.widgets = {}
        self.img_label = None
        self.ruta_imagen_actual = None
        self.crear_widgets()

    def crear_widgets(self):
        config = CONFIG_TABLAS['recintos']
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

        # Frame para preview de imagen
        self.preview_frame = ttk.LabelFrame(contenido_frame, text="🖼️ VISTA PREVIA", padding="15")
        self.preview_frame.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0), pady=5)
        self.preview_frame.configure(width=300)

        inner_frame = ttk.Frame(self.preview_frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.img_label = ttk.Label(inner_frame, text="Imagen no seleccionada",
                                   background='white', anchor='center', justify='center',
                                   font=('Arial', 9))
        self.img_label.pack(fill=tk.BOTH, expand=True)

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

    def seleccionar_imagen(self, entry_widget):
        ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar imagen",
            filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif *.bmp")]
        )
        if ruta_imagen:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, ruta_imagen)
            self.mostrar_imagen(ruta_imagen)

    def mostrar_imagen(self, ruta_imagen):
        try:
            imagen = Image.open(ruta_imagen)
            imagen.thumbnail((280, 280), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)
            self.img_label.configure(image=foto, text="")
            self.img_label.image = foto
            self.ruta_imagen_actual = ruta_imagen
        except Exception as e:
            self.img_label.configure(image=None, text="Error al cargar la imagen")

    def obtener_valores(self):
        valores = {}
        for campo, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry):
                valores[campo] = widget.get()
            elif isinstance(widget, tk.Text):
                valores[campo] = widget.get("1.0", tk.END).strip()
        return valores

    def limpiar_formulario(self):
        for campo, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)
        if self.img_label:
            self.img_label.configure(image=None, text="Imagen no seleccionada")
            self.ruta_imagen_actual = None

    def mostrar_datos(self, recinto):
        # recinto: (id_recinto, nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas)
        self.widgets['nombre'].delete(0, tk.END)
        self.widgets['nombre'].insert(0, recinto[1] if recinto[1] else "")

        self.widgets['foto'].delete(0, tk.END)
        if recinto[2]:
            self.widgets['foto'].insert(0, recinto[2])
            self.mostrar_imagen(recinto[2])

        self.widgets['ubicacion'].delete(0, tk.END)
        self.widgets['ubicacion'].insert(0, recinto[3] if recinto[3] else "")

        self.widgets['capacidad'].delete(0, tk.END)
        self.widgets['capacidad'].insert(0, str(recinto[4]) if recinto[4] else "")

        self.widgets['tipo'].delete(0, tk.END)
        self.widgets['tipo'].insert(0, recinto[5] if recinto[5] else "")

        self.widgets['tarifa_hora'].delete(0, tk.END)
        self.widgets['tarifa_hora'].insert(0, str(recinto[6]) if recinto[6] else "")

        self.widgets['caracteristicas'].delete(1.0, tk.END)
        if recinto[7]:
            self.widgets['caracteristicas'].insert(1.0, recinto[7])

    def ventana_buscar(self):
        ventana_buscar = tk.Toplevel(self.parent)
        ventana_buscar.title("Buscar Recinto")
        ventana_buscar.geometry("500x300")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.parent)
        ventana_buscar.grab_set()

        ttk.Label(ventana_buscar, text="Ingrese el nombre del recinto:",
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
            self.controller.buscar_recintos(nombre, listbox)

        def seleccionar_recinto(event):
            if not listbox.curselection():
                return
            index = listbox.curselection()[0]
            recinto = listbox.resultados[index]
            self.controller.mostrar_recinto(recinto)
            ventana_buscar.destroy()

        entry_nombre.bind('<KeyRelease>', realizar_busqueda)
        listbox.bind('<Double-Button-1>', seleccionar_recinto)

        btn_cerrar = ttk.Button(ventana_buscar, text="Cerrar",
                                command=ventana_buscar.destroy)
        btn_cerrar.pack(pady=10)

        return ventana_buscar, entry_nombre, listbox
