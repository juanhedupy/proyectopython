from bd.database import Database

class ClienteModel:
    def __init__(self, db):
        self.db = db

    def guardar(self, identificacion, foto, nombre, telefono, email, direccion):
        return self.db.ejecutar_procedimiento(
            "InsertarCliente",
            [identificacion, foto, nombre, telefono, email, direccion]
        )

    def actualizar(self, id_cliente, identificacion, foto, nombre, telefono, email, direccion):
        return self.db.ejecutar_procedimiento(
            "ActualizarCliente",
            [id_cliente, identificacion, foto, nombre, telefono, email, direccion]
        )

    def buscar_por_identificacion(self, identificacion):
        return self.db.ejecutar_procedimiento("ObtenerClientePorIdentificacion", [identificacion])

    def eliminar(self, id_cliente):
        return self.db.ejecutar_procedimiento("EliminarCliente", [id_cliente])

    def obtener_todos(self):
        """
        Obtiene TODOS los clientes usando el procedimiento ObtenerTodosClientes (corregido para generator de stored_results).
        Retorna: Lista de tuplas con todos los campos de clientes (de SELECT *).
        """
        try:
            cursor = self.db.conexion.cursor()
            cursor.callproc('ObtenerTodosClientes')  # Llama al proc

            # FIX CLAVE: Maneja el generator de stored_results correctamente
            stored_results = cursor.stored_results()
            resultados = []
            if stored_results:
                # Extrae el primer result set (el SELECT del proc)
                result_set = next(stored_results)
                resultados = result_set.fetchall()  # Ahora sí, fetchall() en el cursor real

            cursor.close()
            print(f"DEBUG MODEL: Obtenidos {len(resultados)} clientes de BD")  # Debería mostrar 9 ahora
            return resultados
        except Exception as e:
            print(f"DEBUG MODEL ERROR en obtener_todos: {e}")  # Debug si aún falla
            return []  # Retorna vacío solo si hay error grave