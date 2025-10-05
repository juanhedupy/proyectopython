import tkinter as tk
from tkinter import ttk
from config import ESTILOS, CONFIG_TABLAS, CONFIG_BD
from bd.database import Database
from models.cliente_model import ClienteModel
from models.servicio_model import ServicioModel
from models.recinto_model import RecintoModel
from models.evento_model import EventoModel
from controllers.cliente_controller import ClienteController
from controllers.servicio_controller import ServicioController
from controllers.recinto_controller import RecintoController
from controllers.evento_controller import EventoController


class SistemaFormulariosCompleto:
    def __init__(self, root):
        print("DEBUG: Iniciando SistemaFormulariosCompleto...")  # Debug (opcional, remueve si quieres)
        self.root = root
        self.root.title("Sistema de Gestión de Eventos - GESTION EVENT")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f0f8ff')

        # Variables para IDs actuales (estado compartido)
        self.id_cliente_actual = None
        self.id_servicio_actual = None
        self.id_recinto_actual = None
        self.id_evento_actual = None

        # Configurar estilos
        try:
            print("DEBUG: Configurando estilos...")  # Debug
            self.style = ttk.Style()
            for estilo, props in ESTILOS.items():
                self.style.configure(estilo, **props)
            print("DEBUG: Estilos configurados OK.")
        except Exception as e:
            print(f"DEBUG ERROR en estilos: {e}")

        # Inicializar BD y models
        try:
            print("DEBUG: Intentando conectar a BD...")  # Debug
            self.db = Database(CONFIG_BD)
            if not self.db.conexion:
                print("DEBUG: Conexión BD falló, saliendo temprano.")
                from tkinter import messagebox
                messagebox.showerror("Error Crítico",
                                     "No se pudo inicializar la base de datos. Verifica MySQL y credenciales.")
                return  # Salir si no hay conexión
            print("DEBUG: BD conectada OK.")
        except Exception as e:
            print(f"DEBUG ERROR en BD: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error Crítico", f"Error al inicializar BD: {e}")
            return

        try:
            print("DEBUG: Creando models...")  # Debug
            self.cliente_model = ClienteModel(self.db)
            self.servicio_model = ServicioModel(self.db)
            self.recinto_model = RecintoModel(self.db)
            self.evento_model = EventoModel(self.db)
            print("DEBUG: Models creados OK.")
        except Exception as e:
            print(f"DEBUG ERROR en models: {e}")
            return

        # Diccionario para controllers y views actuales
        self.current_controller = None
        self.current_view = None
        self.tabla_actual = None

        # Contenedor para formularios
        self.contenedor_formulario = None

        try:
            print("DEBUG: Llamando crear_interfaz()...")  # Debug
            self.crear_interfaz()
            print("DEBUG: Interfaz creada OK.")
        except Exception as e:
            print(f"DEBUG ERROR en crear_interfaz: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error Crítico", f"Error al crear interfaz: {e}")

    def crear_interfaz(self):
        print("DEBUG: Dentro de crear_interfaz...")  # Debug
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Frame de selección de tabla
        selector_frame = ttk.Frame(main_frame)
        selector_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(selector_frame, text="SELECCIONAR TABLA:", style='Header.TLabel').pack(side=tk.LEFT, padx=(0, 10))

        self.tabla_var = tk.StringVar()
        tablas = list(CONFIG_TABLAS.keys())
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
        print("DEBUG: crear_interfaz completado.")

    def cambiar_tabla(self, event=None):
        print(f"DEBUG: Cambiando a tabla: {self.tabla_var.get()}")  # Debug
        # Limpiar contenedor anterior
        if self.current_controller:
            for widget in self.contenedor_formulario.winfo_children():
                widget.destroy()
        self.current_controller = None
        self.current_view = None

        tabla = self.tabla_var.get()
        self.tabla_actual = tabla

        try:
            # Crear nuevo controller y view según tabla
            if tabla == 'clientes':
                self.current_controller = ClienteController(self.contenedor_formulario, self, self.cliente_model)
                self.current_view = self.current_controller.view
                print("DEBUG: ClienteController creado OK.")
            elif tabla == 'servicios':
                self.current_controller = ServicioController(self.contenedor_formulario, self, self.servicio_model)
                self.current_view = self.current_controller.view
                print("DEBUG: ServicioController creado OK.")
            elif tabla == 'recintos':
                self.current_controller = RecintoController(self.contenedor_formulario, self, self.recinto_model)
                self.current_view = self.current_controller.view
                print("DEBUG: RecintoController creado OK.")
            elif tabla == 'eventos':
                self.current_controller = EventoController(self.contenedor_formulario, self, self.evento_model,
                                                           self.cliente_model, self.recinto_model)
                self.current_view = self.current_controller.view
                print("DEBUG: EventoController creado OK.")

            # Para eventos, cargar recintos inmediatamente
            if tabla == 'eventos' and self.current_controller:
                self.current_controller.cargar_recintos()

            # Resetear IDs
            if tabla != 'clientes':
                self.id_cliente_actual = None
            if tabla != 'servicios':
                self.id_servicio_actual = None
            if tabla != 'recintos':
                self.id_recinto_actual = None
            if tabla != 'eventos':
                self.id_evento_actual = None
            print(f"DEBUG: Tabla {tabla} cargada OK.")
        except Exception as e:
            print(f"DEBUG ERROR en cambiar_tabla: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error", f"Error al cargar tabla {tabla}: {e}")


# Función principal
def main():
    print("DEBUG: Iniciando main()...")  # Debug
    root = tk.Tk()

    # NUEVO: Agregar favicon (icono de la ventana)
    try:
        root.iconbitmap('assets/faviconn.ico')  # Ruta relativa desde la carpeta raíz
        print("DEBUG: Favicon cargado exitosamente.")  # Opcional
    except tk.TclError as e:
        print(f"DEBUG: Error al cargar favicon: {e}. Continuando sin icono.")  # No rompe el programa
    except FileNotFoundError:
        print("DEBUG: Archivo faviconn.ico no encontrado en assets/. Continuando sin icono.")
    except Exception as e:
        print(f"DEBUG: Error inesperado con favicon: {e}. Continuando sin icono.")

    app = SistemaFormulariosCompleto(root)
    print("DEBUG: App creada, iniciando mainloop.")  # Debug
    root.mainloop()


if __name__ == "__main__":
    main()