-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-11-2024 a las 16:32:01
-- Versión del servidor: 10.4.27-MariaDB
-- Versión de PHP: 8.2.0

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `ventas`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `categorias`
--

CREATE TABLE `categorias` (
  `cat` int(2) NOT NULL,
  `nomcat` text NOT NULL,
  `supercat` varchar(250) DEFAULT NULL,
  `superest` int(1) DEFAULT NULL,
  `subcat` varchar(250) DEFAULT NULL,
  `subest` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `categorias`
--

INSERT INTO `categorias` (`cat`, `nomcat`, `supercat`, `superest`, `subcat`, `subest`) VALUES
(0, '2', '3 DF HDFG HDFGH DFGH DFGH D', 0, '0', 1),
(1, 'Categoria uno 11', 'Aca va un mensaje referido a la primera oferta', 1, 'Aca va el mensaje para abajo de la categoria uno', 3),
(2, '3fghedfghdfghdfg', 'Ofertas tres (3)', 0, '1', 0),
(3, '11111111111111111111111111111', 'Grupo UNO', 0, '1', 0),
(4, 'Ofertas 4', 'Oferta Categoria 4', 2, '', 4),
(5, '1', 'zzzzzzzzzzzzzzzzzzzzzzzz', 1, 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzz', 1),
(6, 'asdfasd', NULL, 1, NULL, 1),
(7, '1', NULL, 1, NULL, 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `producto`
--

CREATE TABLE `producto` (
  `id` int(5) NOT NULL,
  `codigo` int(13) NOT NULL,
  `producto` varchar(75) NOT NULL,
  `detalle` varchar(250) DEFAULT NULL,
  `imagen` varchar(250) DEFAULT NULL,
  `img1` varchar(250) DEFAULT NULL,
  `img2` varchar(250) DEFAULT NULL,
  `img3` varchar(250) DEFAULT NULL,
  `categoria` int(1) NOT NULL,
  `costo` decimal(10,2) NOT NULL,
  `por1` decimal(10,2) DEFAULT NULL,
  `precio1` decimal(10,2) DEFAULT NULL,
  `por2` decimal(10,2) DEFAULT NULL,
  `precio2` decimal(10,2) DEFAULT NULL,
  `stock` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `producto`
--

INSERT INTO `producto` (`id`, `codigo`, `producto`, `detalle`, `imagen`, `img1`, `img2`, `img3`, `categoria`, `costo`, `por1`, `precio1`, `por2`, `precio2`, `stock`) VALUES
(24, 10001, 'Campera de cuero con aplique metalicos modelo 12345 67890 123456789- 123 45', 'Detalle largo. largo', '/static/images/Amigos_Asado.jpeg', '/static/images/Amigos_Futbol.jpeg', '/static/images/17250777742945659540186838971779.jpg', '', 4, '15000.00', '1.00', '1.00', '1.00', '1.00', 5),
(25, 200001, 'pelota de trapo 1', 'Aqui va el detalle completo del producto. Se puede agregar tambien algunb detalle de la forma de pago, calidad, etc. FG DF GD FG D FG DF GD FG DF GD FG DF G DFG DF G DF GD FG DF GDFG DF G DF GDF G DF GD FG DFG DF GD FG DF G', '/static/images/delfin.png', '/static/images/Matambre_2.jpg', '/static/images/WhatsApp_Image_2024-08-06_at_18.31.29.jpeg', '/static/images/17270647588642724746185011267375.jpg', 4, '5000.00', '1.00', '1.00', '1.00', '1235.00', 10),
(32, 1234567890, 'qwerqwerqwer', 'Detalle no muy largo', '/static/images/FC.jpg', '', '', '', 3, '10.00', '1.00', '1.00', '1.00', '1.00', 1),
(34, 12, 'kjh', '54w4e5', '', '', '', '', 3, '3.00', '3.00', '3.00', '3.00', '3.00', 3),
(35, 6516576, 'pioupoiup', 'iuoiuoi', '', '', '', '', 3, '2.00', '2.00', '2.00', '2.00', '2.00', 2),
(39, 898451621, 'hkhbk', 'kjnbk', '', '', '', '', 2, '2.00', '2.00', '2.00', '2.00', '2.00', 2),
(41, 2147483647, '9879879', '987', '', '', '', '', 1, '1.00', '1.00', '1.00', '1.00', '1.00', 1),
(43, 98798798, 'jhgjhg', 'kjhgjhgj', '', '', '', '', 2, '2.00', '2.00', '2.00', '2.00', '2.00', 2),
(46, 100012, '123123', '123123', '', '', '', '', 1, '1.00', '1.00', '1.00', '1.00', '1.00', 1),
(47, 12412, 'Reloj de pared simil madera con punteros dorados a pila AA modelo 123456789', 'Reloj de pared simil madera con punteros dorados a pila AA', '/static/images/reloj1.jfif', '', '', '', 0, '1.00', '1.00', '15000.99', '1.00', '1.00', 1),
(48, 5454, 'HJRTJRTY', 'Prueba de Sistema', '', '', '/static/images/DJI_0018.jpg', '', 4, '100.00', '1.00', '5454.00', '1.00', '1.00', 2),
(50, 7, 'ULTIMO AGREGADO', NULL, '', '', '', '', 1, '7.00', '0.00', '0.00', '0.00', '0.00', 7),
(52, 100013, 'zzzzzzzzzzzzzzz', 'zzzzzzzzzzzzzzzzzzzzzzzzzzz', '/static/images/WhatsApp_Image_2024-10-15_at_10.32.29.jpeg', '', '', '', 1, '1.00', '1.00', '1.00', '1.00', '1.00', 1),
(56, 11, 'D', 'swert', '', '', '', '', 3, '1.00', '0.00', '0.00', '0.00', '0.00', 1);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL DEFAULT 'NOT NULL',
  `password` varchar(255) NOT NULL DEFAULT 'NOT NULL'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'ruben', 'scrypt:32768:8:1$WtYz6tujydW1qBka$7c6c87ff46d8955cb0fd016970c576dd7c15f2b867fcbd9ecaec2e2f6e7cea72b52ef345d4f4504ff53741797f9a001fc1610fd524366f1919a5f89a946bd9a7');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `categorias`
--
ALTER TABLE `categorias`
  ADD PRIMARY KEY (`cat`);

--
-- Indices de la tabla `producto`
--
ALTER TABLE `producto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `USUARIO` (`username`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `producto`
--
ALTER TABLE `producto`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=58;

--
-- AUTO_INCREMENT de la tabla `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
