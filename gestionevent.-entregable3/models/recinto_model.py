from bd.database import Database

class RecintoModel:
    def __init__(self, db):
        self.db = db

    def guardar(self, nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas):
        return self.db.ejecutar_procedimiento(
            "InsertarRecinto",
            [nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas]
        )

    def actualizar(self, id_recinto, nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas):
        return self.db.ejecutar_procedimiento(
            "ActualizarRecinto",
            [id_recinto, nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas]
        )

    def buscar_por_nombre(self, nombre):
        return self.db.ejecutar_procedimiento("BuscarRecintoPorNombre", [nombre])

    def obtener_todos(self):
        return self.db.ejecutar_procedimiento("ObtenerRecintos")

    def eliminar(self, id_recinto):
        return self.db.ejecutar_procedimiento("EliminarRecinto", [id_recinto])


    def obtener_todos(self):
        """
        Obtiene TODOS los recintos usando el procedimiento ObtenerTodosServicios (corregido para generator de stored_results).
        Retorna: Lista de tuplas con todos los campos de recintos (de SELECT *).
        """
        try:
            cursor = self.db.conexion.cursor()
            cursor.callproc('ObtenerTodosLosRecintos')  # Llama al proc

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


