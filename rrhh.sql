-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 09-10-2024 a las 23:48:04
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
-- Base de datos: `rrhh`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `entrevistas`
--

CREATE TABLE `entrevistas` (
  `id` binary(16) NOT NULL DEFAULT uuid(),
  `vacante_id` binary(16) NOT NULL,
  `postulacion_id` binary(16) NOT NULL,
  `fecha` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `postulaciones`
--

CREATE TABLE `postulaciones` (
  `id` binary(16) NOT NULL,
  `vacante_id` binary(16) DEFAULT NULL,
  `nombre` varchar(255) DEFAULT NULL,
  `email` varchar(255) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `cv` varchar(200) DEFAULT NULL,
  `respuestas` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`respuestas`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `postulaciones`
--

INSERT INTO `postulaciones` (`id`, `vacante_id`, `nombre`, `email`, `telefono`, `cv`, `respuestas`) VALUES
(0x62343866656462352d623463632d3435, 0x38343931363332382d643064612d3436, 'Jaziel', 'admin@admin.com', '04247537350', 'cv\\b072d7c1-ea6b-4a50-8775-ccb3ab9ac4fb.pdf', ''),
(0x32613931666439312d636635652d3436, 0x38343931363332382d643064612d3436, 'Jaziel', 'njmarquezm@gmail.com', '04247537350', 'cv\\68669458-4f65-41bf-af08-4f9002202b45.pdf', ''),
(0x35616266386463342d346366652d3434, 0x38343931363332382d643064612d3436, 'Angel', 'fm1132792@gmail.com', '123456', 'cv\\703500a5-c442-4c1a-9d93-e26bb414c113.pdf', ''),
(0x63373036656335392d373337622d3435, 0x31363438643766322d316130622d3430, 'Jaziel', 'admin@admin.com', '04247537350', 'cv\\a2591dbb-0f6a-4411-9a29-d0464bdd6f7a.pdf', '{\"\\u00bfPython es?\": \"Una serpiente\", \"\\u00bfDos y dos son cuatro, cuatro y dos son seis?\": \" seis y dos son ocho y ocho diecis\\u00e9is \"}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pruebas`
--

CREATE TABLE `pruebas` (
  `vacante_id` binary(16) NOT NULL,
  `prueba` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`prueba`))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pruebas`
--

INSERT INTO `pruebas` (`vacante_id`, `prueba`) VALUES
(0x31363438643766322d316130622d3430, '{\"id\": \"1580042c-fd51-4e40-a931-badfd7548642\", \"vacante_id\": \"bytearray(b\'1648d7f2-1a0b-40\')\", \"preguntas\": [{\"pregunta\": \"\\u00bfPython es?\", \"opciones\": [\"Una serpiente\", \" un lenguaje de bajo nivel\", \" un lenguaje de alto nivel\"]}, {\"pregunta\": \"\\u00bfDos y dos son cuatro, cuatro y dos son seis?\", \"opciones\": [\"Verdadero\", \" Falso\", \" seis y dos son ocho y ocho diecis\\u00e9is \"]}]}'),
(0x31363438643766322d316130622d3430, '{\"id\": \"0fc035f8-1b61-45ff-9c05-9146b8a377f1\", \"vacante_id\": \"bytearray(b\'1648d7f2-1a0b-40\')\", \"preguntas\": [{\"pregunta\": \"\\u00bf2 + 2?\", \"opciones\": [\"4\", \" 3\", \" pinga\"]}]}');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `users`
--

CREATE TABLE `users` (
  `id` binary(16) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `email` varchar(30) NOT NULL,
  `telefono` varchar(15) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  `email_correo` varchar(255) DEFAULT NULL,
  `password_correo` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `users`
--

INSERT INTO `users` (`id`, `nombre`, `email`, `telefono`, `contrasena`, `email_correo`, `password_correo`) VALUES
<<<<<<< HEAD
(0x37343961323330382d613333362d3430, 'Nelvin', 'admin@admin.com', '04247537350', '12345678', NULL, NULL),
=======
(0x37343961323330382d613333362d3430, 'Nelvin', 'admin@admin.com', '04247537350', '12345678', NULL, 'No lo voy a dejar aqui por obvias razones'),
>>>>>>> f81498f4aa327eb3d23e7b5a6d4b9b2a979814be
(0x64613938663935642d313934392d3437, 'Nelvin', 'njmarquezm@gmail.com', '04247537350', '12345678', 'njmarquezm@gmail.com', 'No lo voy a dejar aqui por obvias razones');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vacantes`
--

CREATE TABLE `vacantes` (
  `id` binary(16) NOT NULL,
  `iduser` binary(16) NOT NULL,
  `titulo` varchar(255) NOT NULL,
  `descripcion` text NOT NULL,
  `ubicacion` varchar(255) DEFAULT NULL,
  `salario` decimal(10,2) DEFAULT NULL,
  `fecha_publicacion` date DEFAULT NULL,
  `fecha_cierre` date DEFAULT NULL,
  `tipo_contrato` enum('Tiempo Completo','Medio Tiempo','Contrato','Temporal','Prácticas') DEFAULT NULL,
  `experiencia_requerida` varchar(255) DEFAULT NULL,
  `educacion_requerida` varchar(255) DEFAULT NULL,
  `habilidades_requeridas` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `vacantes`
--

INSERT INTO `vacantes` (`id`, `iduser`, `titulo`, `descripcion`, `ubicacion`, `salario`, `fecha_publicacion`, `fecha_cierre`, `tipo_contrato`, `experiencia_requerida`, `educacion_requerida`, `habilidades_requeridas`) VALUES
(0x31363438643766322d316130622d3430, 0x64613938663935642d313934392d3437, 'Programador', 'Desarrollador Web Full Stack', 'Remoto', 3000.00, '2024-10-08', '2024-10-15', 'Tiempo Completo', '2 años', 'Experiencia demostrable', 'HTML, CSS, JS, REACTJS'),
(0x38343931363332382d643064612d3436, 0x64613938663935642d313934392d3437, 'Programador', 'Python Senior Developer', 'Remoto', 1100.00, '2024-10-04', '2024-10-09', 'Tiempo Completo', '2 años', 'Experiencia demostrable', 'Python');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `entrevistas`
--
ALTER TABLE `entrevistas`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `vacantes`
--
ALTER TABLE `vacantes`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
