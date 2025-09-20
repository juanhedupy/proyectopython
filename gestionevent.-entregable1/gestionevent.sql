-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-09-2025 a las 00:58:59
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

-- --------------------------------------------------------

--
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

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `servicios`
--

CREATE TABLE `servicios` (
  `id_servicio` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

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
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `eventos`
--
ALTER TABLE `eventos`
  MODIFY `id_evento` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recintos`
--
ALTER TABLE `recintos`
  MODIFY `id_recinto` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `servicios`
--
ALTER TABLE `servicios`
  MODIFY `id_servicio` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `servicio_proveedor`
--
ALTER TABLE `servicio_proveedor`
  MODIFY `id_servicio_proveedor` int(11) NOT NULL AUTO_INCREMENT;

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

# NOTA IMPORTANTE:
# La base de datos del semestre 1 presentaba múltiples errores y no funcionaba correctamente.
# Por esa razón, diseñé una nueva estructura enfocada en un proyecto más mediano pero funcional.
# Aún faltan los procedimientos almacenados, ya que para este primer entregable solo era necesario
# diseñar la interfaz. En el segundo entregable, donde se implementará toda la lógica para las
# operaciones CRUD, se incluirá la base de datos completa con sus respectivos procedimientos almacenados.