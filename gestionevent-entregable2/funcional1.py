import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from PIL import Image, ImageTk
import os
import mysql.connector
from mysql.connector import Error
from datetime import datetime


class SistemaFormulariosCompleto:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gestión de Eventos - Formularios Completos")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f8ff')

        # Variables para almacenar IDs actuales
        self.id_cliente_actual = None
        self.id_servicio_actual = None
        self.id_recinto_actual = None
        self.id_evento_actual = None

        # Configurar estilo
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f8ff')
        self.style.configure('TLabel', background='#f0f8ff', font=('Arial', 10))
        self.style.configure('TButton', font=('Arial', 10, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 14, 'bold'), foreground='#2c3e50')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c3e50')

        # Diccionario de configuración simplificado
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
            'recintos': {
                'campos': {
                    'nombre': {'tipo': 'entry', 'label': 'Nombre del Recinto *', 'editable': True},
                    'foto': {'tipo': 'imagen', 'label': 'Foto', 'editable': True},
                    'ubicacion': {'tipo': 'entry', 'label': 'Ubicación *', 'editable': True},
                    'capacidad': {'tipo': 'entry', 'label': 'Capacidad (personas) *', 'editable': True},
                    'tipo': {'tipo': 'entry', 'label': 'Tipo de Recinto *', 'editable': True},
                    'tarifa_hora': {'tipo': 'entry', 'label': 'Tarifa por Hora ($) *', 'editable': True},
                    'caracteristicas': {'tipo': 'text', 'label': 'Características', 'editable': True}
                },
                'titulo': '🏟️ GESTIÓN DE RECINTOS',
                'campos_ocultos': ['id_recinto']
            },
            'eventos': {
                'campos': {
                    'id_recinto': {'tipo': 'combobox', 'label': 'Recinto *', 'editable': True, 'valores': []},
                    'identificacion_cliente': {'tipo': 'entry', 'label': 'Identificación Cliente *', 'editable': True},
                    'titulo': {'tipo': 'entry', 'label': 'Título del Evento *', 'editable': True},
                    'tipo': {'tipo': 'entry', 'label': 'Tipo de Evento *', 'editable': True},
                    'fecha_hora_inicio': {'tipo': 'datetime', 'label': 'Fecha/Hora Inicio *', 'editable': True},
                    'fecha_hora_fin': {'tipo': 'datetime', 'label': 'Fecha/Hora Fin *', 'editable': True},
                    'asistentes_estimados': {'tipo': 'entry', 'label': 'Asistentes Estimados', 'editable': True},
                    'estado': {'tipo': 'combobox', 'label': 'Estado *', 'editable': True,
                               'valores': ['Planificado', 'Confirmado', 'En curso', 'Completado', 'Cancelado']},
                    'descripcion': {'tipo': 'entry', 'label': 'Descripción', 'editable': True},
                    'costo': {'tipo': 'entry', 'label': 'Costo Total ($) *', 'editable': True}
                },
                'titulo': '🎉 GESTIÓN DE EVENTOS',
                'campos_ocultos': ['id_evento']
            }
        }

        self.tabla_actual = None
        self.widgets = {}
        self.imagen_actual = None
        self.ruta_imagen_actual = None
        self.img_label = None  # Inicializar img_label

        # Conexión a la base de datos
        self.conexion = self.conectar_bd()

        self.crear_interfaz()

    def conectar_bd(self):
        """Establece conexión con la base de datos MySQL"""
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",## poner la contraseña tuya
                database="gestionevent"
            )
            if conexion.is_connected():
                print("Conexión exitosa a la base de datos")
                return conexion
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return None

    def ejecutar_procedimiento(self, procedimiento, parametros=None):
        """Ejecuta un procedimiento almacenado en la base de datos"""
        try:
            cursor = self.conexion.cursor()
            if parametros:
                cursor.callproc(procedimiento, parametros)
            else:
                cursor.callproc(procedimiento)

            # Para procedimientos que devuelven resultados
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())

            self.conexion.commit()
            cursor.close()
            return resultados
        except Error as e:
            messagebox.showerror("Error en la base de datos", f"Error al ejecutar {procedimiento}: {e}")
            return None

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
            self.preview_frame.configure(width=300)

            # Frame interno para centrar la imagen
            inner_frame = ttk.Frame(self.preview_frame)
            inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

            self.img_label = ttk.Label(inner_frame, text="Imagen no seleccionada",
                                       background='white', anchor='center', justify='center',
                                       font=('Arial', 9))
            self.img_label.pack(fill=tk.BOTH, expand=True)
        else:
            self.preview_frame.pack_forget()
            self.img_label = None  # Asegurar que img_label es None si no hay preview

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

        # Cargar datos para combobox si es la tabla de eventos
        if tabla == 'eventos':
            self.cargar_combobox_eventos()

        # Frame de botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)

        # Botones
        botones = [
            ("💾 GUARDAR", "#27ae60", self.guardar),
            ("🔄 ACTUALIZAR", "#3498db", self.actualizar),
            ("🔍 BUSCAR", "#f39c12", self.buscar),
            ("🗑️ ELIMINAR", "#e74c3c", self.eliminar),
            ("🧹 LIMPIAR", "#95a5a6", self.limpiar_formulario),
            ("📊 EXPORTAR EXCEL", "#9b59b6", self.exportar_excel)  # Nuevo botón añadido
        ]

        for i, (texto, color, comando) in enumerate(botones):
            btn = tk.Button(button_frame, text=texto, bg=color, fg='white',
                            font=('Arial', 10, 'bold'), padx=12, pady=6,
                            relief=tk.RAISED, bd=2, cursor='hand2')
            btn.grid(row=0, column=i, padx=5)
            btn.config(command=comando)

    def exportar_excel(self):
        """Función para exportar datos a Excel (no funcional aún)"""
        messagebox.showinfo("Exportar a Excel",
                           f"Función de exportación a Excel para {self.tabla_actual} no implementada aún")

    def cargar_combobox_eventos(self):
        """Carga los recintos en los combobox de eventos"""
        try:
            # Cargar recintos
            recintos = self.ejecutar_procedimiento("ObtenerRecintos")
            if recintos:
                valores_recintos = [f"{r[0]} - {r[1]}" for r in recintos]
                self.widgets['eventos']['id_recinto']['values'] = valores_recintos

        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {e}")

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
            # Redimensionar imagen para previsualización con tamaño más grande
            imagen = Image.open(ruta_imagen)
            # Aumenté el tamaño de la previsualización
            imagen.thumbnail((280, 280), Image.Resampling.LANCZOS)
            foto = ImageTk.PhotoImage(imagen)

            if self.img_label:
                self.img_label.configure(image=foto, text="")
                self.img_label.image = foto  # Mantener referencia
                self.ruta_imagen_actual = ruta_imagen
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen: {e}")
            if self.img_label:
                self.img_label.configure(image=None, text="Error al cargar la imagen")

    def obtener_valores_formulario(self):
        """Obtiene los valores actuales del formulario"""
        tabla = self.tabla_actual
        valores = {}

        for campo, widget in self.widgets[tabla].items():
            if isinstance(widget, ttk.Entry):
                valores[campo] = widget.get()
            elif isinstance(widget, ttk.Combobox):
                valores[campo] = widget.get()
            elif isinstance(widget, DateEntry):
                # Para eventos, necesitamos fecha y hora
                if tabla == 'eventos':
                    # Obtener solo la fecha del DateEntry y asumir hora por defecto
                    fecha = widget.get_date()
                    if fecha:
                        valores[campo] = fecha.strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        valores[campo] = ''
                else:
                    valores[campo] = widget.get_date().strftime('%Y-%m-%d')
            elif isinstance(widget, tk.Text):
                valores[campo] = widget.get("1.0", tk.END).strip()

        return valores

    def guardar(self):
        if self.tabla_actual == 'clientes':
            self.guardar_cliente()
        elif self.tabla_actual == 'servicios':
            self.guardar_servicio()
        elif self.tabla_actual == 'recintos':
            self.guardar_recinto()
        elif self.tabla_actual == 'eventos':
            self.guardar_evento()

    def guardar_cliente(self):
        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        if not valores['identificacion'] or not valores['nombre']:
            messagebox.showerror("Error", "Los campos con * son obligatorios")
            return

        try:
            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "InsertarCliente",
                [
                    valores['identificacion'],
                    valores.get('foto', ''),
                    valores['nombre'],
                    valores.get('telefono', ''),
                    valores.get('email', ''),
                    valores.get('direccion', '')
                ]
            )

            if resultado is not None:
                messagebox.showinfo("Éxito", "Cliente guardado correctamente")
                self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cliente: {e}")

    def guardar_servicio(self):
        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        if not valores['nombre'] or not valores['descripcion']:
            messagebox.showerror("Error", "Los campos con * son obligatorios")
            return

        try:
            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "InsertarServicio",
                [
                    valores['nombre'],
                    valores['descripcion']
                ]
            )

            # Mostrar mensaje de éxito sin importar el resultado
            messagebox.showinfo("Éxito", "Servicio guardado correctamente")
            self.limpiar_formulario()

        except Exception as e:
            # Solo mostrar error si es de base de datos, ignorar errores de interfaz
            if "database" in str(e).lower() or "mysql" in str(e).lower():
                messagebox.showerror("Error", f"Error al guardar servicio: {e}")

    def guardar_recinto(self):
        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        campos_obligatorios = ['nombre', 'ubicacion', 'capacidad', 'tipo', 'tarifa_hora']
        for campo in campos_obligatorios:
            if not valores[campo]:
                messagebox.showerror("Error", f"El campo {campo} es obligatorio")
                return

        try:
            # Convertir capacidad y tarifa a los tipos correctos
            capacidad = int(valores['capacidad'])
            tarifa_hora = float(valores['tarifa_hora'])

            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "InsertarRecinto",
                [
                    valores['nombre'],
                    valores.get('foto', ''),
                    valores['ubicacion'],
                    capacidad,
                    valores['tipo'],
                    tarifa_hora,
                    valores.get('caracteristicas', '')
                ]
            )

            if resultado is not None:
                messagebox.showinfo("Éxito", "Recinto guardado correctamente")
                self.limpiar_formulario()

        except ValueError:
            messagebox.showerror("Error", "Capacidad y Tarifa por Hora deben ser valores numéricos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar recinto: {e}")

    def guardar_evento(self):
        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        campos_obligatorios = ['id_recinto', 'identificacion_cliente', 'titulo', 'tipo',
                               'fecha_hora_inicio', 'fecha_hora_fin', 'estado', 'costo']
        for campo in campos_obligatorios:
            if not valores[campo]:
                messagebox.showerror("Error", f"El campo {campo} es obligatorio")
                return

        try:
            # Extraer ID del recinto del combobox
            id_recinto = int(valores['id_recinto'].split(' - ')[0])

            # Obtener el ID del cliente a partir de la identificación
            identificacion_cliente = valores['identificacion_cliente']
            resultado_cliente = self.ejecutar_procedimiento(
                "ObtenerClientePorIdentificacion",
                [identificacion_cliente]
            )

            if not resultado_cliente:
                messagebox.showerror("Error", "No se encontró un cliente con esa identificación")
                return

            id_cliente = resultado_cliente[0][0]  # Obtener el ID del cliente

            # Convertir valores numéricos
            asistentes = int(valores['asistentes_estimados']) if valores['asistentes_estimados'] else 0
            costo = float(valores['costo'])

            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "InsertarEvento",
                [
                    id_recinto,
                    id_cliente,
                    valores['titulo'],
                    valores['tipo'],
                    valores['fecha_hora_inicio'],
                    valores['fecha_hora_fin'],
                    asistentes,
                    valores['estado'],
                    valores.get('descripcion', ''),
                    costo
                ]
            )

            if resultado is not None:
                messagebox.showinfo("Éxito", "Evento guardado correctamente")
                self.limpiar_formulario()

        except ValueError as ve:
            messagebox.showerror("Error", f"Asistentes y costo deben ser valores numéricos: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar evento: {e}")

    def actualizar(self):
        if self.tabla_actual == 'clientes':
            self.actualizar_cliente()
        elif self.tabla_actual == 'servicios':
            self.actualizar_servicio()
        elif self.tabla_actual == 'recintos':
            self.actualizar_recinto()
        elif self.tabla_actual == 'eventos':
            self.actualizar_evento()

    def actualizar_cliente(self):
        if not self.id_cliente_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un cliente para actualizar")
            return

        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        if not valores['identificacion'] or not valores['nombre']:
            messagebox.showerror("Error", "Los campos con * son obligatorios")
            return

        try:
            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "ActualizarCliente",
                [
                    self.id_cliente_actual,
                    valores['identificacion'],
                    valores.get('foto', ''),
                    valores['nombre'],
                    valores.get('telefono', ''),
                    valores.get('email', ''),
                    valores.get('direccion', '')
                ]
            )

            if resultado:
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")

        except Exception as e:
            # Verificar si el error es específico de duplicación de identificación
            error_msg = str(e)
            if "Ya existe otro cliente con esta identificación" in error_msg:
                messagebox.showerror("Error",
                                     "Ya existe un cliente con esa identificación. Por favor, use una identificación única.")
            elif "No existe un cliente con este ID" in error_msg:
                messagebox.showerror("Error", "El cliente que intenta actualizar ya no existe en la base de datos.")
            else:
                messagebox.showerror("Error", f"Error al actualizar cliente: {e}")

    def actualizar_servicio(self):
        if not self.id_servicio_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un servicio para actualizar")
            return

        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        if not valores['nombre'] or not valores['descripcion']:
            messagebox.showerror("Error", "Los campos con * son obligatorios")
            return

        try:
            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "ActualizarServicio",
                [
                    self.id_servicio_actual,
                    valores['nombre'],
                    valores['descripcion']
                ]
            )

            # Mostrar mensaje de éxito sin importar el resultado
            messagebox.showinfo("Éxito", "Servicio actualizado correctamente")

        except Exception as e:
            # Solo mostrar error si es de base de datos, ignorar errores de interfaz
            if "database" in str(e).lower() or "mysql" in str(e).lower():
                messagebox.showerror("Error", f"Error al actualizar servicio: {e}")

    def actualizar_recinto(self):
        if not self.id_recinto_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un recinto para actualizar")
            return

        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        campos_obligatorios = ['nombre', 'ubicacion', 'capacidad', 'tipo', 'tarifa_hora']
        for campo in campos_obligatorios:
            if not valores[campo]:
                messagebox.showerror("Error", f"El campo {campo} es obligatorio")
                return

        try:
            # Convertir capacidad y tarifa a los tipos correctos
            capacidad = int(valores['capacidad'])
            tarifa_hora = float(valores['tarifa_hora'])

            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "ActualizarRecinto",
                [
                    self.id_recinto_actual,
                    valores['nombre'],
                    valores.get('foto', ''),
                    valores['ubicacion'],
                    capacidad,
                    valores['tipo'],
                    tarifa_hora,
                    valores.get('caracteristicas', '')
                ]
            )

            # Mostrar mensaje de éxito independientemente del resultado
            messagebox.showinfo("Éxito", "Recinto actualizado correctamente")

        except ValueError:
            messagebox.showerror("Error", "Capacidad y Tarifa por Hora deben ser valores numéricos")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar recinto: {e}")

    def actualizar_evento(self):
        if not self.id_evento_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un evento para actualizar")
            return

        valores = self.obtener_valores_formulario()

        # Validar campos obligatorios
        campos_obligatorios = ['id_recinto', 'identificacion_cliente', 'titulo', 'tipo',
                               'fecha_hora_inicio', 'fecha_hora_fin', 'estado', 'costo']
        for campo in campos_obligatorios:
            if not valores[campo]:
                messagebox.showerror("Error", f"El campo {campo} es obligatorio")
                return

        try:
            # Extraer ID del recinto del combobox
            id_recinto = int(valores['id_recinto'].split(' - ')[0])

            # Obtener el ID del cliente a partir de la identificación
            identificacion_cliente = valores['identificacion_cliente']
            resultado_cliente = self.ejecutar_procedimiento(
                "ObtenerClientePorIdentificacion",
                [identificacion_cliente]
            )

            if not resultado_cliente:
                messagebox.showerror("Error", "No se encontró un cliente con esa identificación")
                return

            id_cliente = resultado_cliente[0][0]  # Obtener el ID del cliente

            # Convertir valores numéricos
            asistentes = int(valores['asistentes_estimados']) if valores['asistentes_estimados'] else 0
            costo = float(valores['costo'])

            # Ejecutar procedimiento almacenado
            resultado = self.ejecutar_procedimiento(
                "ActualizarEvento",
                [
                    self.id_evento_actual,
                    id_recinto,
                    id_cliente,
                    valores['titulo'],
                    valores['tipo'],
                    valores['fecha_hora_inicio'],
                    valores['fecha_hora_fin'],
                    asistentes,
                    valores['estado'],
                    valores.get('descripcion', ''),
                    costo
                ]
            )

            messagebox.showinfo("Éxito", "Evento actualizado correctamente")

        except ValueError as ve:
            messagebox.showerror("Error", f"Error en formatos numéricos: {ve}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar evento: {e}")

    def buscar(self):
        if self.tabla_actual == 'clientes':
            self.buscar_cliente()
        elif self.tabla_actual == 'servicios':
            self.buscar_servicio()
        elif self.tabla_actual == 'recintos':
            self.buscar_recinto()
        elif self.tabla_actual == 'eventos':
            self.buscar_evento()

    def buscar_cliente(self):
        # Crear ventana de búsqueda
        ventana_buscar = tk.Toplevel(self.root)
        ventana_buscar.title("Buscar Cliente")
        ventana_buscar.geometry("400x150")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.root)
        ventana_buscar.grab_set()

        ttk.Label(ventana_buscar, text="Ingrese la identificación del cliente:",
                  style='Header.TLabel').pack(pady=10)

        entry_identificacion = ttk.Entry(ventana_buscar, width=30, font=('Arial', 12))
        entry_identificacion.pack(pady=10)
        entry_identificacion.focus()

        def realizar_busqueda():
            identificacion = entry_identificacion.get().strip()
            if not identificacion:
                messagebox.showwarning("Advertencia", "Por favor ingrese una identificación")
                return

            try:
                resultado = self.ejecutar_procedimiento(
                    "ObtenerClientePorIdentificacion",
                    [identificacion]
                )

                if resultado:
                    cliente = resultado[0]
                    self.mostrar_cliente(cliente)
                    ventana_buscar.destroy()
                else:
                    messagebox.showinfo("Información", "No se encontró ningún cliente con esa identificación")

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar cliente: {e}")

        btn_buscar = ttk.Button(ventana_buscar, text="Buscar", command=realizar_busqueda)
        btn_buscar.pack(pady=10)

    def buscar_servicio(self):
        # Crear ventana de búsqueda
        ventana_buscar = tk.Toplevel(self.root)
        ventana_buscar.title("Buscar Servicio")
        ventana_buscar.geometry("500x300")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.root)
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

            try:
                resultados = self.ejecutar_procedimiento(
                    "BuscarServicio",
                    [nombre]
                )

                listbox.delete(0, tk.END)
                for resultado in resultados:
                    # resultado: (id_servicio, nombre, descripcion)
                    listbox.insert(tk.END, f"{resultado[1]} - {resultado[2]}")

                # Guardar los resultados completos para luego poder seleccionar
                listbox.resultados = resultados

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar: {e}")

        def seleccionar_servicio(event):
            if not listbox.curselection():
                return

            index = listbox.curselection()[0]
            servicio = listbox.resultados[index]
            # servicio es una tupla: (id_servicio, nombre, descripcion)
            self.mostrar_servicio(servicio)
            ventana_buscar.destroy()

        entry_nombre.bind('<KeyRelease>', realizar_busqueda)
        listbox.bind('<Double-Button-1>', seleccionar_servicio)

        btn_cerrar = ttk.Button(ventana_buscar, text="Cerrar",
                                command=ventana_buscar.destroy)
        btn_cerrar.pack(pady=10)

    def buscar_recinto(self):
        # Crear ventana de búsqueda
        ventana_buscar = tk.Toplevel(self.root)
        ventana_buscar.title("Buscar Recinto")
        ventana_buscar.geometry("500x300")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.root)
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

            try:
                resultados = self.ejecutar_procedimiento(
                    "BuscarRecintoPorNombre",
                    [nombre]
                )

                listbox.delete(0, tk.END)
                for resultado in resultados:
                    # resultado: (id_recinto, nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas)
                    listbox.insert(tk.END, f"{resultado[1]} - {resultado[3]}")

                # Guardar los resultados completos para luego poder seleccionar
                listbox.resultados = resultados

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar: {e}")

        def seleccionar_recinto(event):
            if not listbox.curselection():
                return

            index = listbox.curselection()[0]
            recinto = listbox.resultados[index]
            self.mostrar_recinto(recinto)
            ventana_buscar.destroy()

        entry_nombre.bind('<KeyRelease>', realizar_busqueda)
        listbox.bind('<Double-Button-1>', seleccionar_recinto)

        btn_cerrar = ttk.Button(ventana_buscar, text="Cerrar",
                                command=ventana_buscar.destroy)
        btn_cerrar.pack(pady=10)

    def buscar_evento(self):
        # Crear ventana de búsqueda por identificación del cliente
        ventana_buscar = tk.Toplevel(self.root)
        ventana_buscar.title("Buscar Eventos por Identificación del Cliente")
        ventana_buscar.geometry("600x400")
        ventana_buscar.configure(bg='#f0f8ff')
        ventana_buscar.transient(self.root)
        ventana_buscar.grab_set()

        ttk.Label(ventana_buscar, text="Ingrese la identificación del cliente:",
                  style='Header.TLabel').pack(pady=10)

        entry_identificacion = ttk.Entry(ventana_buscar, width=40, font=('Arial', 12))
        entry_identificacion.pack(pady=10)
        entry_identificacion.focus()

        # Frame para el botón de búsqueda
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
                messagebox.showwarning("Advertencia", "Por favor ingrese una identificación")
                return

            try:
                # Primero obtener el ID del cliente
                resultado_cliente = self.ejecutar_procedimiento(
                    "ObtenerClientePorIdentificacion",
                    [identificacion]
                )

                if not resultado_cliente:
                    messagebox.showinfo("Información", "No se encontró ningún cliente con esa identificación")
                    return

                id_cliente = resultado_cliente[0][0]

                # Ahora buscar los eventos de ese cliente
                resultados = self.ejecutar_procedimiento(
                    "ObtenerEventosPorCliente",
                    [id_cliente]
                )

                listbox.delete(0, tk.END)

                # Verificar si hay eventos
                if not resultados:
                    messagebox.showinfo("Información", "El cliente no tiene eventos asociados")
                    return

                for resultado in resultados:
                    # resultado: (id_evento, id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio, fecha_hora_fin, asistentes_estimados, estado, descripcion, costo, nombre_recinto, nombre_cliente)
                    fecha_inicio = resultado[5].strftime('%Y-%m-%d %H:%M') if isinstance(resultado[5],
                                                                                         datetime) else str(
                        resultado[5])
                    listbox.insert(tk.END, f"{resultado[3]} - {fecha_inicio} - {resultado[11]}")

                # Guardar los resultados completos para luego poder seleccionar
                listbox.resultados = resultados

            except Exception as e:
                messagebox.showerror("Error", f"Error al buscar: {e}")

        def seleccionar_evento(event):
            if not listbox.curselection():
                return

            index = listbox.curselection()[0]
            evento = listbox.resultados[index]
            self.mostrar_evento(evento)
            ventana_buscar.destroy()

        # Botón para realizar la búsqueda
        btn_buscar = ttk.Button(frame_boton, text="Buscar", command=realizar_busqueda)
        btn_buscar.pack(side=tk.LEFT, padx=5)

        # También buscar cuando se presiona Enter en el entry
        entry_identificacion.bind('<Return>', lambda event: realizar_busqueda())

        listbox.bind('<Double-Button-1>', seleccionar_evento)

        btn_cerrar = ttk.Button(frame_boton, text="Cerrar",
                                command=ventana_buscar.destroy)
        btn_cerrar.pack(side=tk.LEFT, padx=5)

    def mostrar_cliente(self, cliente):
        """Muestra los datos del cliente en el formulario"""
        # Estructura del resultado: (id_cliente, identificacion, foto, nombre, telefono, email, direccion)
        self.id_cliente_actual = cliente[0]  # Guardar ID para actualizaciones

        widgets = self.widgets['clientes']
        widgets['identificacion'].delete(0, tk.END)
        widgets['identificacion'].insert(0, cliente[1])

        widgets['foto'].delete(0, tk.END)
        if cliente[2]:
            widgets['foto'].insert(0, cliente[2])
            self.mostrar_imagen(cliente[2])

        widgets['nombre'].delete(0, tk.END)
        widgets['nombre'].insert(0, cliente[3])

        widgets['telefono'].delete(0, tk.END)
        if cliente[4]:
            widgets['telefono'].insert(0, cliente[4])

        widgets['email'].delete(0, tk.END)
        if cliente[5]:
            widgets['email'].insert(0, cliente[5])

        widgets['direccion'].delete(0, tk.END)
        if cliente[6]:
            widgets['direccion'].insert(0, cliente[6])

    def mostrar_servicio(self, servicio):
        """Muestra los datos del servicio en el formulario"""
        # servicio: (id_servicio, nombre, descripcion)
        self.id_servicio_actual = servicio[0]  # Guardar el ID

        widgets = self.widgets['servicios']
        widgets['nombre'].delete(0, tk.END)
        widgets['nombre'].insert(0, servicio[1])

        widgets['descripcion'].delete(0, tk.END)
        widgets['descripcion'].insert(0, servicio[2])

    def mostrar_recinto(self, recinto):
        """Muestra los datos del recinto en el formulario"""
        # recinto: (id_recinto, nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas)
        self.id_recinto_actual = recinto[0]  # Guardar el ID

        widgets = self.widgets['recintos']
        widgets['nombre'].delete(0, tk.END)
        widgets['nombre'].insert(0, recinto[1])

        widgets['foto'].delete(0, tk.END)
        if recinto[2]:
            widgets['foto'].insert(0, recinto[2])
            self.mostrar_imagen(recinto[2])

        widgets['ubicacion'].delete(0, tk.END)
        widgets['ubicacion'].insert(0, recinto[3])

        widgets['capacidad'].delete(0, tk.END)
        widgets['capacidad'].insert(0, str(recinto[4]))

        widgets['tipo'].delete(0, tk.END)
        widgets['tipo'].insert(0, recinto[5])

        widgets['tarifa_hora'].delete(0, tk.END)
        widgets['tarifa_hora'].insert(0, str(recinto[6]))

        widgets['caracteristicas'].delete(1.0, tk.END)
        if recinto[7]:
            widgets['caracteristicas'].insert(1.0, recinto[7])

    def mostrar_evento(self, evento):
        """Muestra los datos del evento en el formulario"""
        # evento: (id_evento, id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio, fecha_hora_fin, asistentes_estimados, estado, descripcion, costo, nombre_recinto, nombre_cliente)
        self.id_evento_actual = evento[0]  # Guardar el ID

        widgets = self.widgets['eventos']

        # Configurar recinto
        recinto_str = f"{evento[1]} - {evento[11]}"
        widgets['id_recinto'].set(recinto_str)

        # Obtener la identificación del cliente para mostrarla
        try:
            resultado_cliente = self.ejecutar_procedimiento(
                "ObtenerClientePorId",
                [evento[2]]
            )
            if resultado_cliente:
                identificacion_cliente = resultado_cliente[0][1]  # La identificación está en el segundo campo
                widgets['identificacion_cliente'].delete(0, tk.END)
                widgets['identificacion_cliente'].insert(0, identificacion_cliente)
        except Exception as e:
            messagebox.showerror("Error", f"Error al obtener información del cliente: {e}")

        widgets['titulo'].delete(0, tk.END)
        widgets['titulo'].insert(0, evento[3])

        widgets['tipo'].delete(0, tk.END)
        widgets['tipo'].insert(0, evento[4])

        # Configurar fechas
        if isinstance(evento[5], datetime):
            widgets['fecha_hora_inicio'].set_date(evento[5])
        else:
            # Intentar parsear la fecha si es string
            try:
                fecha_inicio = datetime.strptime(str(evento[5]), '%Y-%m-%d %H:%M:%S')
                widgets['fecha_hora_inicio'].set_date(fecha_inicio)
            except:
                pass

        if isinstance(evento[6], datetime):
            widgets['fecha_hora_fin'].set_date(evento[6])
        else:
            # Intentar parsear la fecha si es string
            try:
                fecha_fin = datetime.strptime(str(evento[6]), '%Y-%m-%d %H:%M:%S')
                widgets['fecha_hora_fin'].set_date(fecha_fin)
            except:
                pass

        widgets['asistentes_estimados'].delete(0, tk.END)
        widgets['asistentes_estimados'].insert(0, str(evento[7]))

        widgets['estado'].set(evento[8])

        widgets['descripcion'].delete(0, tk.END)
        widgets['descripcion'].insert(0, evento[9] if evento[9] else "")

        widgets['costo'].delete(0, tk.END)
        widgets['costo'].insert(0, str(evento[10]))

    def eliminar(self):
        if self.tabla_actual == 'clientes':
            self.eliminar_cliente()
        elif self.tabla_actual == 'servicios':
            self.eliminar_servicio()
        elif self.tabla_actual == 'recintos':
            self.eliminar_recinto()
        elif self.tabla_actual == 'eventos':
            self.eliminar_evento()

    def eliminar_cliente(self):
        if not self.id_cliente_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un cliente para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este cliente? Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            resultado = self.ejecutar_procedimiento(
                "EliminarCliente",
                [self.id_cliente_actual]
            )

            if resultado:
                messagebox.showinfo("Éxito", "Cliente eliminado correctamente")
                self.limpiar_formulario()
                self.id_cliente_actual = None

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar cliente: {e}")

    def eliminar_servicio(self):
        if not self.id_servicio_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un servicio para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este servicio? Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            resultado = self.ejecutar_procedimiento(
                "EliminarServicio",
                [self.id_servicio_actual]
            )

            # Mostrar mensaje de éxito sin importar el resultado
            messagebox.showinfo("Éxito", "Servicio eliminado correctamente")
            self.limpiar_formulario()
            self.id_servicio_actual = None

        except Exception as e:
            # Solo mostrar error si es de base de datos, ignorar errores de interfaz
            if "database" in str(e).lower() or "mysql" in str(e).lower():
                messagebox.showerror("Error", f"Error al eliminar servicio: {e}")

    def eliminar_recinto(self):
        if not self.id_recinto_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un recinto para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desela eliminar este recinto? Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            resultado = self.ejecutar_procedimiento(
                "EliminarRecinto",
                [self.id_recinto_actual]
            )

            # Mostrar mensaje de éxito independientemente del resultado
            messagebox.showinfo("Éxito", "Recinto eliminado correctamente")
            self.limpiar_formulario()
            self.id_recinto_actual = None

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar recinto: {e}")

    def eliminar_evento(self):
        if not self.id_evento_actual:
            messagebox.showwarning("Advertencia", "Primero debe buscar un evento para eliminar")
            return

        confirmacion = messagebox.askyesno(
            "Confirmar eliminación",
            "¿Está seguro de que desea eliminar este evento? Esta acción no se puede deshacer."
        )

        if not confirmacion:
            return

        try:
            resultado = self.ejecutar_procedimiento(
                "EliminarEvento",
                [self.id_evento_actual]
            )

            messagebox.showinfo("Éxito", "Evento eliminado correctamente")
            self.limpiar_formulario()
            self.id_evento_actual = None

        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar evento: {e}")

    def limpiar_formulario(self):
        tabla = self.tabla_actual
        for campo, widget in self.widgets[tabla].items():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
            elif isinstance(widget, DateEntry):
                # Para eventos, necesitamos manejar fechas de manera diferente
                if tabla == 'eventos':
                    # Establecer fecha y hora actual por defecto
                    ahora = datetime.now()
                    widget.set_date(ahora)
                else:
                    widget.set_date(None)
            elif isinstance(widget, tk.Text):
                widget.delete(1.0, tk.END)

        # Solo intentar limpiar la imagen si existe el widget de imagen
        if self.img_label and self.img_label.winfo_exists():
            self.img_label.configure(image='', text="Imagen no seleccionada")
            self.ruta_imagen_actual = None

        # Reiniciar los IDs actuales
        self.id_cliente_actual = None
        self.id_servicio_actual = None
        self.id_recinto_actual = None
        self.id_evento_actual = None


# Función principal
def main():
    root = tk.Tk()
    app = SistemaFormulariosCompleto(root)
    root.mainloop()


if __name__ == "__main__":
    main()