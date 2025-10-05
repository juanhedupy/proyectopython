# Sistema de Gestión de Eventos

![Favicon](assets/faviconn.ico) 

## Descripción

Este es un **sistema completo de gestión de eventos** desarrollado en Python utilizando el patrón **MVC (Model-View-Controller)**. Permite administrar clientes, servicios, recintos y eventos de manera integrada, con operaciones CRUD (Crear, Leer, Actualizar, Eliminar), búsqueda avanzada y exportación a Excel.

El sistema está diseñado para un entorno de eventos (ej. bodas, conferencias), donde puedes:
- Registrar y buscar clientes por identificación.
- Gestionar servicios (ej. catering, decoración).
- Administrar recintos (lugares para eventos).
- Crear eventos vinculando clientes, recintos y servicios, con fechas, costos y estados.

Incluye una interfaz gráfica intuitiva con Tkinter, base de datos MySQL y validaciones básicas. Es modular y extensible.

**Autor**: [JUAN PABLO HERNANDEZ"]  
**Versión**: 3.0  


## Funcionalidades Principales

- **Selección de Módulos**: Cambia entre formularios de Clientes, Servicios, Recintos y Eventos mediante un combobox.
- **CRUD Completo**:
  - Guardar/Actualizar/Eliminar registros.
  - Limpiar formularios.
- **Búsqueda Avanzada**: Busca clientes por identificación y eventos asociados (con ventana modal y selección por doble clic).
- **Integraciones**:
  - Eventos vinculan clientes y recintos (combobox dinámicos).
  - Manejo de fechas con calendario (tkcalendar) para eventos.
  - Vista previa de imágenes para clientes.
- **Exportación**: Genera reportes en Excel para cada tabla.
- **UI/UX**: Botones con emojis y colores temáticos (verde para guardar, azul para actualizar, etc.), estilos ttk y favicon personalizado.
- **Base de Datos**: Usa procedimientos almacenados MySQL para eficiencia y seguridad.

## Tecnologías y Dependencias

- **Lenguaje**: Python 3.8+.
- **Interfaz Gráfica**: Tkinter (nativo) + ttk para temas modernos + tkcalendar para selectores de fecha.
- **Base de Datos**: MySQL (con mysql-connector-python) + procedimientos almacenados.
- **Otras Librerías**:
  - `pandas` y `openpyxl`: Para exportar a Excel.
  - `datetime`: Manejo de fechas.
- **Estructura**: Patrón MVC puro (separación de lógica, datos y vistas).

## Requisitos de Instalación

1. **Python 3.8 o superior**: Descarga desde [python.org](https://www.python.org/downloads/).
2. **MySQL Server**: Instala MySQL 8.0+ (ej. XAMPP, MySQL Workbench). Crea la base de datos `gestion_eventos` y ejecuta el script SQL en `bd/database.sql` (incluye tablas y procedimientos almacenados).
3. **Instala dependencias** (ejecuta en terminal/cmd):

