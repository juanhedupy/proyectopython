-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 22-09-2025 a las 19:28:04
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `gestionevent`
--
create DATABASE if NOT EXISTS gestionevent;
USE gestionevent;


-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `identificacion` varchar(20) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `identificacion`, `foto`, `nombre`, `telefono`, `email`, `direccion`) VALUES
(3, 'CID001', 'foto1.jpg', 'Ana GarcíaSSS', '+123456789', 'ana@email.com', 'Calle 123, Ciudad'),
(4, 'CID002', 'foto2.jpg', 'Carlos RuizZ', '+987654321', 'carlos@email.com', 'Avenida 456, Ciudad'),
(5, 'CID003', 'foto3.jpg', 'María López', '+112233445', 'maria@email.com', 'Plaza 789, Ciudad'),
(13, 'zccccs', 'C:/Users/Usuario/Pictures/Saved Pictures/istockphoto-1389348844-612x612.jpg', 'acaca', 'cacac', 'acaca', 'cacc'),
(16, '100655212', 'C:/Users/Usuario/Pictures/Saved Pictures/foto-ambiente-lab-01.jpg', 'Sara Hernandez ', '31246402132', 'sara@gmail.com', 'calle 25'),
(17, '21215313125', 'C:/Users/Usuario/Pictures/Saved Pictures/43-9061.00.jpg', 'Juan Carlos Perez', '3126012564', 'perez@gmail.com', 'calle 15');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos`
--

CREATE TABLE `eventos` (
  `id_evento` int(11) NOT NULL,
  `id_recinto` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `titulo` varchar(200) NOT NULL,
  `tipo` varchar(200) NOT NULL,
  `fecha_hora_inicio` datetime NOT NULL,
  `fecha_hora_fin` datetime NOT NULL,
  `asistentes_estimados` int(11) DEFAULT NULL,
  `estado` varchar(200) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `costo` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `eventos`
--

INSERT INTO `eventos` (`id_evento`, `id_recinto`, `id_cliente`, `titulo`, `tipo`, `fecha_hora_inicio`, `fecha_hora_fin`, `asistentes_estimados`, `estado`, `descripcion`, `costo`) VALUES
(23, 8, 4, 'FIESTAAAAAA', 'AAAAAA', '2025-09-05 00:00:00', '2025-09-04 00:00:00', 1200, 'Confirmado', 'SDADA', 12000.00),
(24, 8, 16, 'FIESTA DE SARA', 'FIESTA', '2025-09-22 00:00:00', '2025-09-22 00:00:00', 100, 'Planificado', 'es una fiesta con mucho licor ', 100000.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `eventos_servicios`
--

CREATE TABLE `eventos_servicios` (
  `id_evento` int(11) NOT NULL,
  `id_servicio_proveedor` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `identificacion` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `identificacion`, `nombre`, `telefono`, `email`) VALUES
(1, 'PID001', 'Catering S.A.', '+445566778', 'info@cateringsa.com'),
(2, 'PID002', 'AudioPro', '+556677889', 'contacto@audiopro.com'),
(3, 'PID003', 'Decoraciones VIP', '+667788990', 'ventas@decovip.com');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recintos`
--

CREATE TABLE `recintos` (
  `id_recinto` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `foto` varchar(100) NOT NULL,
  `ubicacion` varchar(200) NOT NULL,
  `capacidad` int(11) NOT NULL,
  `tipo` varchar(200) NOT NULL,
  `tarifa_hora` decimal(10,2) NOT NULL,
  `caracteristicas` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `recintos`
--

INSERT INTO `recintos` (`id_recinto`, `nombre`, `foto`, `ubicacion`, `capacidad`, `tipo`, `tarifa_hora`, `caracteristicas`) VALUES
(2, 'Salón EliteaaaaAaA', 'elite.jpg', 'Centro', 150, 'Interior', 200.00, 'Aire acondicionado, escenario y iluminación profesional'),
(8, 'JARDIN', 'C:/Users/Usuario/Pictures/Saved Pictures/istockphoto-1389348844-612x612.jpg', 'SSSSS', 23231, 'JARDIN', 1121311.00, 'SSSS'),
(9, 'arboletes', 'dddd', 'sad', 11321, 'salon', 21234.00, 'dadad');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id_servicio` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicios`
--

INSERT INTO `servicios` (`id_servicio`, `nombre`, `descripcion`) VALUES
(1, 'Catering', 'Servicio de comida y bebida para eventos'),
(3, 'Decoración', 'Diseño y montaje de decoración temáticas'),
(4, 'fotografiaassssa', 'fotografia profesionalñss'),
(11, 'pinturas', 'pinturas para niñosAAA');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicio_proveedor`
--

CREATE TABLE `servicio_proveedor` (
  `id_servicio_proveedor` int(11) NOT NULL,
  `id_servicio` int(11) NOT NULL,
  `id_proveedor` int(11) NOT NULL,
  `precio` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `servicio_proveedor`
--

INSERT INTO `servicio_proveedor` (`id_servicio_proveedor`, `id_servicio`, `id_proveedor`, `precio`) VALUES
(1, 1, 1, 1200.00),
(3, 3, 3, 950.75);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `identificacion` (`identificacion`);

--
-- Indices de la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD PRIMARY KEY (`id_evento`),
  ADD KEY `id_recinto` (`id_recinto`),
  ADD KEY `id_cliente` (`id_cliente`);

--
-- Indices de la tabla `eventos_servicios`
--
ALTER TABLE `eventos_servicios`
  ADD PRIMARY KEY (`id_evento`,`id_servicio_proveedor`),
  ADD KEY `id_servicio_proveedor` (`id_servicio_proveedor`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`),
  ADD UNIQUE KEY `identificacion` (`identificacion`);

--
-- Indices de la tabla `recintos`
--
ALTER TABLE `recintos`
  ADD PRIMARY KEY (`id_recinto`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `servicios`
--
ALTER TABLE `servicios`
  ADD PRIMARY KEY (`id_servicio`),
  ADD UNIQUE KEY `nombre` (`nombre`);

--
-- Indices de la tabla `servicio_proveedor`
--
ALTER TABLE `servicio_proveedor`
  ADD PRIMARY KEY (`id_servicio_proveedor`),
  ADD UNIQUE KEY `unique_servicio_proveedor` (`id_servicio`,`id_proveedor`),
  ADD KEY `id_proveedor` (`id_proveedor`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id_evento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT de la tabla `recintos`
--
ALTER TABLE `recintos`
  MODIFY `id_recinto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT de la tabla `servicio_proveedor`
--
ALTER TABLE `servicio_proveedor`
  MODIFY `id_servicio_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `eventos`
--
ALTER TABLE `eventos`
  ADD CONSTRAINT `eventos_ibfk_1` FOREIGN KEY (`id_recinto`) REFERENCES `recintos` (`id_recinto`) ON DELETE CASCADE,
  ADD CONSTRAINT `eventos_ibfk_2` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`) ON DELETE CASCADE;

--
-- Filtros para la tabla `eventos_servicios`
--
ALTER TABLE `eventos_servicios`
  ADD CONSTRAINT `eventos_servicios_ibfk_1` FOREIGN KEY (`id_evento`) REFERENCES `eventos` (`id_evento`) ON DELETE CASCADE,
  ADD CONSTRAINT `eventos_servicios_ibfk_2` FOREIGN KEY (`id_servicio_proveedor`) REFERENCES `servicio_proveedor` (`id_servicio_proveedor`) ON DELETE CASCADE;

--
-- Filtros para la tabla `servicio_proveedor`
--
ALTER TABLE `servicio_proveedor`
  ADD CONSTRAINT `servicio_proveedor_ibfk_1` FOREIGN KEY (`id_servicio`) REFERENCES `servicios` (`id_servicio`) ON DELETE CASCADE,
  ADD CONSTRAINT `servicio_proveedor_ibfk_2` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


DELIMITER $$

CREATE PROCEDURE `ActualizarCliente` (IN `p_id_cliente` INT, IN `p_identificacion` VARCHAR(20), IN `p_foto` VARCHAR(100), IN `p_nombre` VARCHAR(100), IN `p_telefono` VARCHAR(20), IN `p_email` VARCHAR(100), IN `p_direccion` VARCHAR(200))   BEGIN
    DECLARE cliente_existe INT;
    DECLARE identificacion_existe INT;

    -- Verificar si el cliente existe
    SELECT COUNT(*) INTO cliente_existe
    FROM clientes
    WHERE id_cliente = p_id_cliente;

    IF cliente_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No existe un cliente con este ID';
    ELSE
        -- Verificar si la nueva identificación ya existe en otro cliente
        SELECT COUNT(*) INTO identificacion_existe
        FROM clientes
        WHERE identificacion = p_identificacion AND id_cliente != p_id_cliente;

        IF identificacion_existe > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: Ya existe otro cliente con esta identificación';
        ELSE
            -- Actualizar el cliente
            UPDATE clientes
            SET identificacion = p_identificacion,
                foto = p_foto,
                nombre = p_nombre,
                telefono = p_telefono,
                email = p_email,
                direccion = p_direccion
            WHERE id_cliente = p_id_cliente;

            SELECT 'Cliente actualizado correctamente' AS Mensaje;
        END IF;
    END IF;
END$$

CREATE  PROCEDURE `ActualizarEvento` (IN `p_id_evento` INT, IN `p_id_recinto` INT, IN `p_id_cliente` INT, IN `p_titulo` VARCHAR(200), IN `p_tipo` VARCHAR(200), IN `p_fecha_hora_inicio` DATETIME, IN `p_fecha_hora_fin` DATETIME, IN `p_asistentes_estimados` INT, IN `p_estado` VARCHAR(200), IN `p_descripcion` VARCHAR(200), IN `p_costo` DECIMAL(10,2))   BEGIN
    UPDATE eventos
    SET id_recinto = p_id_recinto,
        id_cliente = p_id_cliente,
        titulo = p_titulo,
        tipo = p_tipo,
        fecha_hora_inicio = p_fecha_hora_inicio,
        fecha_hora_fin = p_fecha_hora_fin,
        asistentes_estimados = p_asistentes_estimados,
        estado = p_estado,
        descripcion = p_descripcion,
        costo = p_costo
    WHERE id_evento = p_id_evento;
END$$

CREATE  PROCEDURE `ActualizarRecinto` (IN `p_id_recinto` INT, IN `p_nombre` VARCHAR(100), IN `p_foto` VARCHAR(100), IN `p_ubicacion` VARCHAR(200), IN `p_capacidad` INT, IN `p_tipo` VARCHAR(200), IN `p_tarifa_hora` DECIMAL(10,2), IN `p_caracteristicas` TEXT)   BEGIN
    UPDATE recintos
    SET nombre = p_nombre,
        foto = p_foto,
        ubicacion = p_ubicacion,
        capacidad = p_capacidad,
        tipo = p_tipo,
        tarifa_hora = p_tarifa_hora,
        caracteristicas = p_caracteristicas
    WHERE id_recinto = p_id_recinto;
END$$

CREATE  PROCEDURE `ActualizarServicio` (IN `p_id_servicio` INT, IN `p_nombre` VARCHAR(100), IN `p_descripcion` VARCHAR(100))   BEGIN
    DECLARE existe INT DEFAULT 0;

    -- Verificar si otro servicio tiene el mismo nombre
    SELECT COUNT(*) INTO existe
    FROM servicios
    WHERE nombre = p_nombre
    AND id_servicio <> p_id_servicio;

    IF existe > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Ya existe otro servicio con ese nombre';
    ELSE
        UPDATE servicios
        SET nombre = p_nombre,
            descripcion = p_descripcion
        WHERE id_servicio = p_id_servicio;
    END IF;
END$$

CREATE  PROCEDURE `BuscarClientePorIdentificacion` (IN `p_identificacion` VARCHAR(20))   BEGIN
    SELECT id_cliente, identificacion, foto, nombre, telefono, email, direccion
    FROM clientes
    WHERE identificacion LIKE CONCAT('%', p_identificacion, '%');
END$$

CREATE  PROCEDURE `BuscarEventosPorRecinto` (IN `p_nombre_recinto` VARCHAR(100))   BEGIN
    SELECT e.*, r.nombre as nombre_recinto, c.nombre as nombre_cliente
    FROM eventos e
    INNER JOIN recintos r ON e.id_recinto = r.id_recinto
    INNER JOIN clientes c ON e.id_cliente = c.id_cliente
    WHERE r.nombre LIKE CONCAT('%', p_nombre_recinto, '%')
    ORDER BY e.fecha_hora_inicio DESC;
END$$

CREATE  PROCEDURE `BuscarEventosPorTitulo` (IN `p_titulo` VARCHAR(200))   BEGIN
    SELECT e.*, r.nombre AS nombre_recinto, c.nombre AS nombre_cliente
    FROM eventos e
    INNER JOIN recintos r ON e.id_recinto = r.id_recinto
    INNER JOIN clientes c ON e.id_cliente = c.id_cliente
    WHERE e.titulo LIKE CONCAT('%', p_titulo, '%')
    ORDER BY e.fecha_hora_inicio DESC;
END$$

CREATE  PROCEDURE `BuscarRecintoPorNombre` (IN `p_nombre` VARCHAR(100))   BEGIN
    SELECT * FROM recintos WHERE nombre LIKE CONCAT('%', p_nombre, '%');
END$$

CREATE  PROCEDURE `BuscarServicio` (IN `p_nombre` VARCHAR(100))   BEGIN
    SELECT id_servicio, nombre, descripcion
    FROM servicios
    WHERE nombre LIKE CONCAT('%', p_nombre, '%');
END$$

CREATE  PROCEDURE `EliminarCliente` (IN `p_id_cliente` INT)   BEGIN
    DECLARE cliente_existe INT;
    DECLARE tiene_eventos INT;

    -- Verificar si el cliente existe
    SELECT COUNT(*) INTO cliente_existe
    FROM clientes
    WHERE id_cliente = p_id_cliente;

    IF cliente_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No existe un cliente con este ID';
    ELSE
        -- Verificar si el cliente tiene eventos asociados
        SELECT COUNT(*) INTO tiene_eventos
        FROM eventos
        WHERE id_cliente = p_id_cliente;

        IF tiene_eventos > 0 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Error: No se puede eliminar el cliente porque tiene eventos asociados';
        ELSE
            -- Eliminar el cliente
            DELETE FROM clientes WHERE id_cliente = p_id_cliente;

            SELECT 'Cliente eliminado correctamente' AS Mensaje;
        END IF;
    END IF;
END$$

CREATE  PROCEDURE `EliminarEvento` (IN `p_id_evento` INT)   BEGIN
    DELETE FROM eventos WHERE id_evento = p_id_evento;
END$$

CREATE  PROCEDURE `EliminarRecinto` (IN `p_id_recinto` INT)   BEGIN
    DELETE FROM recintos WHERE id_recinto = p_id_recinto;
END$$

CREATE  PROCEDURE `EliminarServicio` (IN `p_id_servicio` INT)   BEGIN
    DELETE FROM servicios
    WHERE id_servicio = p_id_servicio;
END$$

CREATE  PROCEDURE `InsertarCliente` (IN `p_identificacion` VARCHAR(20), IN `p_foto` VARCHAR(100), IN `p_nombre` VARCHAR(100), IN `p_telefono` VARCHAR(20), IN `p_email` VARCHAR(100), IN `p_direccion` VARCHAR(200))   BEGIN
    DECLARE cliente_existe INT;

    -- Verificar si el cliente ya existe por identificación
    SELECT COUNT(*) INTO cliente_existe
    FROM clientes
    WHERE identificacion = p_identificacion;

    IF cliente_existe > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: Ya existe un cliente con esta identificación';
    ELSE
        -- Insertar el nuevo cliente
        INSERT INTO clientes (identificacion, foto, nombre, telefono, email, direccion)
        VALUES (p_identificacion, p_foto, p_nombre, p_telefono, p_email, p_direccion);

        SELECT 'Cliente insertado correctamente' AS Mensaje;
    END IF;
END$$

CREATE PROCEDURE `InsertarEvento` (IN `p_id_recinto` INT, IN `p_id_cliente` INT, IN `p_titulo` VARCHAR(200), IN `p_tipo` VARCHAR(200), IN `p_fecha_hora_inicio` DATETIME, IN `p_fecha_hora_fin` DATETIME, IN `p_asistentes_estimados` INT, IN `p_estado` VARCHAR(200), IN `p_descripcion` VARCHAR(200), IN `p_costo` DECIMAL(10,2))   BEGIN
    INSERT INTO eventos (id_recinto, id_cliente, titulo, tipo, fecha_hora_inicio,
                        fecha_hora_fin, asistentes_estimados, estado, descripcion, costo)
    VALUES (p_id_recinto, p_id_cliente, p_titulo, p_tipo, p_fecha_hora_inicio,
            p_fecha_hora_fin, p_asistentes_estimados, p_estado, p_descripcion, p_costo);

    SELECT LAST_INSERT_ID() as id_evento;
END$$

CREATE  PROCEDURE `InsertarRecinto` (IN `p_nombre` VARCHAR(100), IN `p_foto` VARCHAR(100), IN `p_ubicacion` VARCHAR(200), IN `p_capacidad` INT, IN `p_tipo` VARCHAR(200), IN `p_tarifa_hora` DECIMAL(10,2), IN `p_caracteristicas` TEXT)   BEGIN
    INSERT INTO recintos (nombre, foto, ubicacion, capacidad, tipo, tarifa_hora, caracteristicas)
    VALUES (p_nombre, p_foto, p_ubicacion, p_capacidad, p_tipo, p_tarifa_hora, p_caracteristicas);
END$$

CREATE  PROCEDURE `InsertarServicio` (IN `p_nombre` VARCHAR(100), IN `p_descripcion` VARCHAR(100))   BEGIN
    DECLARE existe INT DEFAULT 0;

    -- Verificar si el servicio ya existe
    SELECT COUNT(*) INTO existe
    FROM servicios
    WHERE nombre = p_nombre;

    IF existe > 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: El servicio ya existe';
    ELSE
        INSERT INTO servicios (nombre, descripcion)
        VALUES (p_nombre, p_descripcion);
    END IF;
END$$

CREATE PROCEDURE `ObtenerClientePorId` (IN `p_id_cliente` INT)   BEGIN
    SELECT id_cliente, identificacion, foto, nombre, telefono, email, direccion
    FROM clientes
    WHERE id_cliente = p_id_cliente;
END$$

CREATE  PROCEDURE `ObtenerClientePorIdentificacion` (IN `p_identificacion` VARCHAR(20))   BEGIN
    DECLARE cliente_existe INT;

    -- Verificar si el cliente existe
    SELECT COUNT(*) INTO cliente_existe
    FROM clientes
    WHERE identificacion = p_identificacion;

    IF cliente_existe = 0 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Error: No existe un cliente con esta identificación';
    ELSE
        -- Obtener el cliente
        SELECT * FROM clientes WHERE identificacion = p_identificacion;
    END IF;
END$$

CREATE  PROCEDURE `ObtenerClientes` ()   BEGIN
    SELECT id_cliente, identificacion, nombre, telefono, email
    FROM clientes
    ORDER BY nombre;
END$$

CREATE  PROCEDURE `ObtenerEventosPorCliente` (IN `p_id_cliente` INT)   BEGIN
    SELECT e.id_evento, e.id_recinto, e.id_cliente, e.titulo, e.tipo,
           e.fecha_hora_inicio, e.fecha_hora_fin, e.asistentes_estimados,
           e.estado, e.descripcion, e.costo, r.nombre as nombre_recinto,
           c.nombre as nombre_cliente
    FROM eventos e
    INNER JOIN recintos r ON e.id_recinto = r.id_recinto
    INNER JOIN clientes c ON e.id_cliente = c.id_cliente
    WHERE e.id_cliente = p_id_cliente
    ORDER BY e.fecha_hora_inicio DESC;
END$$

CREATE  PROCEDURE `ObtenerRecintos` ()   BEGIN
    SELECT id_recinto, nombre FROM recintos;
END$$

CREATE PROCEDURE `ObtenerTodosClientes` ()   BEGIN
    SELECT * FROM clientes ORDER BY nombre;
END$$

CREATE  PROCEDURE `ObtenerTodosLosEventos` ()   BEGIN
    SELECT e.*, r.nombre as nombre_recinto, c.nombre as nombre_cliente
    FROM eventos e
    INNER JOIN recintos r ON e.id_recinto = r.id_recinto
    INNER JOIN clientes c ON e.id_cliente = c.id_cliente
    ORDER BY e.fecha_hora_inicio DESC;
END$$

CREATE  PROCEDURE `ObtenerTodosLosRecintos` ()   BEGIN
    SELECT * FROM recintos;
END$$

CREATE  PROCEDURE `ObtenerTodosServicios` ()   BEGIN
    SELECT id_servicio, nombre, descripcion
    FROM servicios
    ORDER BY nombre;
END$$

DELIMITER ;
