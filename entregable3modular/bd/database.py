import mysql.connector
from mysql.connector import Error
from tkinter import messagebox

class Database:
    def __init__(self, config):
        self.config = config
        self.conexion = self.conectar()

    def conectar(self):
        """Establece conexión con la base de datos MySQL"""
        try:
            conexion = mysql.connector.connect(**self.config)
            if conexion.is_connected():
                print("Conexión exitosa a la base de datos")
                return conexion
        except Error as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar a la base de datos: {e}")
            return None

    def ejecutar_procedimiento(self, procedimiento, parametros=None):
        """Ejecuta un procedimiento almacenado en la base de datos"""
        if not self.conexion:
            return None
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
