from bd.database import Database

class ServicioModel:
    def __init__(self, db):
        self.db = db

    def guardar(self, nombre, descripcion):
        return self.db.ejecutar_procedimiento("InsertarServicio", [nombre, descripcion])

    def actualizar(self, id_servicio, nombre, descripcion):
        return self.db.ejecutar_procedimiento("ActualizarServicio", [id_servicio, nombre, descripcion])

    def buscar(self, nombre):
        return self.db.ejecutar_procedimiento("BuscarServicio", [nombre])

    def eliminar(self, id_servicio):
        return self.db.ejecutar_procedimiento("EliminarServicio", [id_servicio])

    def obtener_todos(self):
        """
        Obtiene TODOS los servicios usando el procedimiento ObtenerTodosServicios (corregido para generator de stored_results).
        Retorna: Lista de tuplas con todos los campos de servicios (de SELECT *).
        """
        try:
            cursor = self.db.conexion.cursor()
            cursor.callproc('ObtenerTodosServicios')  # Llama al proc

            # FIX CLAVE: Maneja el generator de stored_results correctamente
            stored_results = cursor.stored_results()
            resultados = []
            if stored_results:
                # Extrae el primer result set (el SELECT del proc)
                result_set = next(stored_results)
                resultados = result_set.fetchall()  # Ahora sí, fetchall() en el cursor real

            cursor.close()
            print(f"DEBUG MODEL: Obtenidos {len(resultados)} Servicios de BD")  # Debería mostrar 9 ahora
            return resultados
        except Exception as e:
            print(f"DEBUG MODEL ERROR en obtener_todos: {e}")  # Debug si aún falla
            return []  # Retorna vacío solo si hay error grave
