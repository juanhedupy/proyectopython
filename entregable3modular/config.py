from datetime import datetime

# Configuración de estilos (compartida)
ESTILOS = {
    'TFrame': {'background': '#f0f8ff'},
    'TLabel': {'background': '#f0f8ff', 'font': ('Arial', 10)},
    'TButton': {'font': ('Arial', 10, 'bold')},
    'Header.TLabel': {'font': ('Arial', 14, 'bold'), 'foreground': '#2c3e50'},
    'Title.TLabel': {'font': ('Arial', 16, 'bold'), 'foreground': '#2c3e50'}
}

# Configuración de tablas (campos, títulos, etc.)
CONFIG_TABLAS = {
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

# Colores para botones (compartidos)
COLORES_BOTONES = {
    'guardar': '#27ae60',
    'actualizar': '#3498db',
    'buscar': '#f39c12',
    'eliminar': '#e74c3c',
    'limpiar': '#95a5a6',
    'exportar': '#9b59b6'
}

# Configuración de BD
CONFIG_BD = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',  # Cambia por tu contraseña
    'database': 'gestionevent'
}
