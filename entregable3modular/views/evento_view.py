import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, date
from config import CONFIG_TABLAS

class EventoView:
    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.widgets = {}
        self.crear_widgets()

    def crear_widgets(self):
        config = CONFIG_TABLAS['eventos']
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

            elif config_campo['tipo'] == 'combobox':
                valores = config_campo.get('valores', [])
                widget = ttk.Combobox(campo_frame, values=valores, width=30,
                                      state="readonly", font=('Arial', 10))
                widget.pack(side=tk.LEFT, fill=tk.X, expand=True)

            elif config_campo['tipo'] == 'datetime':
                # CAMBIO: Patrón solo fecha, sin hora (válido en tkcalendar)
                widget = DateEntry(campo_frame, width=29, background='darkblue',
                                   foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd',  # ← CAMBIO CLAVE
                                   font=('Arial', 10))
                widget.pack(side=tk.LEFT)

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
            # Asumiendo que ya corregiste el split()[1] del error anterior
            btn = tk.Button(button_frame, text=texto,
                            bg=self.controller.get_color_boton(texto.split()[1].lower()),
                            fg='white', font=('Arial', 10, 'bold'), padx=12, pady=6,
                            relief=tk.RAISED, bd=2, cursor='hand2')
            btn.grid(row=0, column=i, padx=5)
            btn.config(command=comando)

    def obtener_valores(self):
        valores = {}
        for campo, widget in self.widgets.items():
            if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Combobox):
                valores[campo] = widget.get()
            elif isinstance(widget, DateEntry):
                fecha = widget.get_date()
                if fecha:
                    # CAMBIO: Concatenar ' 00:00:00' para formar DATETIME completo
                    valores[campo] = fecha.strftime('%Y-%m-%d') + ' 00:00:00'
                else:
                    valores[campo] = ''
        return valores

    def limpiar_formulario(self):
        for campo, widget in self.widgets.items():
            if isinstance(widget, (ttk.Entry, ttk.Combobox)):
                widget.set('') if isinstance(widget, ttk.Combobox) else widget.delete(0, tk.END)
            elif isinstance(widget, DateEntry):
                # Establecer fecha actual por defecto para eventos
                ahora = date.today()  # Solo fecha
                widget.set_date(ahora)
        self.controller.cargar_recintos()  # Recargar combobox al limpiar

    def mostrar_datos(self, evento):
        # evento: (id_evento, id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio, fecha_hora_fin, asistentes_estimados, estado, descripcion, costo, nombre_recinto, nombre_cliente)
        widgets = self.widgets

        # Recinto
        recinto_str = f"{evento[1]} - {evento[11]}" if evento[11] else ""
        widgets['id_recinto'].set(recinto_str)

        # Cliente (identificación)
        identificacion_cliente = ""
        try:
            cliente_data = self.controller.cliente_model.obtener_cliente_por_id(evento[2])
            if cliente_data:
                identificacion_cliente = cliente_data[0][1]  # identificacion
        except:
            pass
        widgets['identificacion_cliente'].delete(0, tk.END)
        widgets['identificacion_cliente'].insert(0, identificacion_cliente)

        widgets['titulo'].delete(0, tk.END)
        widgets['titulo'].insert(0, evento[3] if evento[3] else "")

        widgets['tipo'].delete(0, tk.END)
        widgets['tipo'].insert(0, evento[4] if evento[4] else "")

        # Fechas (CAMBIO: Solo setear la fecha, ignorar hora)
        if evento[5]:  # fecha_hora_inicio
            if isinstance(evento[5], datetime):
                widgets['fecha_hora_inicio'].set_date(evento[5].date())  # ← Extraer solo fecha
            else:
                try:
                    fecha_inicio = datetime.strptime(str(evento[5]), '%Y-%m-%d %H:%M:%S').date()
                    widgets['fecha_hora_inicio'].set_date(fecha_inicio)
                except:
                    pass

        if evento[6]:  # fecha_hora_fin
            if isinstance(evento[6], datetime):
                widgets['fecha_hora_fin'].set_date(evento[6].date())  # ← Extraer solo fecha
            else:
                try:
                    fecha_fin = datetime.strptime(str(evento[6]), '%Y-%m-%d %H:%M:%S').date()
                    widgets['fecha_hora_fin'].set_date(fecha_fin)
                except:
                    pass

        widgets['asistentes_estimados'].delete(0, tk.END)
        widgets['asistentes_estimados'].insert(0, str(evento[7]) if evento[7] else "")

        widgets['estado'].set(evento[8] if evento[8] else "")

        widgets['descripcion'].delete(0, tk.END)
        widgets['descripcion'].insert(0, evento[9] if evento[9] else "")

        widgets['costo'].delete(0, tk.END)
        widgets['costo'].insert(0, str(evento[10]) if evento[10] else "")

    def ventana_buscar(self):
        ventana_buscar = tk.Toplevel(self.parent)
        ventana_buscar.title("Buscar Eventos por Identificación del Cliente")
        ventana_buscar.geometry("600x400")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.parent)
        ventana_buscar.grab_set()

        ttk.Label(ventana_buscar, text="Ingrese la identificación del cliente:",
                  style='Header.TLabel').pack(pady=10)

        entry_identificacion = ttk.Entry(ventana_buscar, width=40, font=('Arial', 12))
        entry_identificacion.pack(pady=10)
        entry_identificacion.focus()

        frame_boton = ttk.Frame(ventana_buscar)
        frame_boton.pack(pady=5)

        # Listbox para resultados
        frame_resultados = ttk.Frame(ventana_buscar)
        frame_resultados.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(frame_resultados)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        listbox = tk.Listbox(frame_resultados, yscrollcommand=scrollbar.set,
                             font=('Arial', 11), selectmode=tk.SINGLE)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar.config(command=listbox.yview)

        def realizar_busqueda():
            identificacion = entry_identificacion.get().strip()
            if not identificacion:
                from tkinter import messagebox
                messagebox.showwarning("Advertencia", "Por favor ingrese una identificación")
                return
            self.controller.buscar_eventos_por_cliente(identificacion, listbox)

        def seleccionar_evento(event):
            if not listbox.curselection():
                return
            index = listbox.curselection()[0]
            evento = listbox.resultados[index]
            self.controller.mostrar_evento(evento)
            ventana_buscar.destroy()

        # Activar búsqueda solo con Enter en el Entry y doble clic en listbox
        entry_identificacion.bind('<Return>', lambda event: realizar_busqueda())
        listbox.bind('<Double-Button-1>', seleccionar_evento)

        # Botón Cerrar
        btn_cerrar = ttk.Button(frame_boton, text="Cerrar", command=ventana_buscar.destroy)
        btn_cerrar.pack(side=tk.LEFT, padx=5)

        return ventana_buscar, entry_identificacion, listbox
