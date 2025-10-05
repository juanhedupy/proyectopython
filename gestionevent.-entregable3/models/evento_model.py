from bd.database import Database

class EventoModel:
    def __init__(self, db):
        self.db = db

    def guardar(self, id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio, fecha_hora_fin,
                asistentes_estimados, estado, descripcion, costo):
        return self.db.ejecutar_procedimiento(
            "InsertarEvento",
            [id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio, fecha_hora_fin,
             asistentes_estimados, estado, descripcion, costo]
        )

    def actualizar(self, id_evento, id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio,
                   fecha_hora_fin, asistentes_estimados, estado, descripcion, costo):
        return self.db.ejecutar_procedimiento(
            "ActualizarEvento",
            [id_evento, id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio, fecha_hora_fin,
             asistentes_estimados, estado, descripcion, costo]
        )

    def obtener_por_cliente(self, id_cliente):
        return self.db.ejecutar_procedimiento("ObtenerEventosPorCliente", [id_cliente])

    def obtener_cliente_por_identificacion(self, identificacion):
        return self.db.ejecutar_procedimiento("ObtenerClientePorIdentificacion", [identificacion])

    def obtener_cliente_por_id(self, id_cliente):
        return self.db.ejecutar_procedimiento("ObtenerClientePorId", [id_cliente])

    def eliminar(self, id_evento):
        return self.db.ejecutar_procedimiento("EliminarEvento", [id_evento])

    def obtener_todos(self):
        """
        Obtiene TODOS los clientes usando el procedimientoObtenerTodosLosEventos(corregido para generator de stored_results).
        Retorna: Lista de tuplas con todos los campos de clientes (de SELECT *).
        """
        try:
            cursor = self.db.conexion.cursor()
            cursor.callproc('ObtenerTodosLosEventos')  # Llama al proc

            # FIX CLAVE: Maneja el generator de stored_results correctamente
            stored_results = cursor.stored_results()
            resultados = []
            if stored_results:
                # Extrae el primer result set (el SELECT del proc)
                result_set = next(stored_results)
                resultados = result_set.fetchall()  # Ahora sí, fetchall() en el cursor real

            cursor.close()
            print(f"DEBUG MODEL: Obtenidos {len(resultados)} eventos de BD")  # Debería mostrar 9 ahora
            return resultados
        except Exception as e:
            print(f"DEBUG MODEL ERROR en obtener_todos: {e}")  # Debug si aún falla
            return []  # Retorna vacío solo si hay error grave
