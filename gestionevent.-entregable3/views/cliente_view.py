import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
from config import CONFIG_TABLAS

class ClienteView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.widgets = {}
        self.img_label = None
        self.ruta_imagen_actual = None
        self.crear_widgets()

    def crear_widgets(self):
        config = CONFIG_TABLAS['clientes']
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
        return valores

    def limpiar_formulario(self):
        for widget in self.widgets.values():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
        if self.img_label:
            self.img_label.configure(image=None, text="Imagen no seleccionada")
            self.ruta_imagen_actual = None

    def mostrar_datos(self, cliente):
        # cliente: (id_cliente, identificacion, foto, nombre, telefono, email, direccion)
        self.widgets['identificacion'].delete(0, tk.END)
        self.widgets['identificacion'].insert(0, cliente[1] if cliente[1] else "")

        self.widgets['foto'].delete(0, tk.END)
        if cliente[2]:
            self.widgets['foto'].insert(0, cliente[2])
            self.mostrar_imagen(cliente[2])

        self.widgets['nombre'].delete(0, tk.END)
        self.widgets['nombre'].insert(0, cliente[3] if cliente[3] else "")

        self.widgets['telefono'].delete(0, tk.END)
        self.widgets['telefono'].insert(0, cliente[4] if cliente[4] else "")

        self.widgets['email'].delete(0, tk.END)
        self.widgets['email'].insert(0, cliente[5] if cliente[5] else "")

        self.widgets['direccion'].delete(0, tk.END)
        self.widgets['direccion'].insert(0, cliente[6] if cliente[6] else "")

    def ventana_buscar(self):
        ventana_buscar = tk.Toplevel(self.parent)
        ventana_buscar.title("Buscar Cliente")
        ventana_buscar.geometry("400x150")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.parent)
        ventana_buscar.grab_set()

        ttk.Label(ventana_buscar, text="Ingrese la identificación del cliente:",
                  style='Header.TLabel').pack(pady=10)

        entry_identificacion = ttk.Entry(ventana_buscar, width=30, font=('Arial', 12))
        entry_identificacion.pack(pady=10)
        entry_identificacion.focus()

        return ventana_buscar, entry_identificacion