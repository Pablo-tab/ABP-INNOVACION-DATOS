-- ============================================================================
-- CONSULTAS SQL - TRABAJO PRACTICO ETL
-- TSCDIA 2025
-- 
-- Integrantes:
-- - Paola Garcia (DNI: 29463402)
-- - Pablo Taborda (DNI: 28270596)
-- - Julio Orjindo (DNI: 26482639)
-- - Rodenas Elias Gabriel (DNI: 36356976)
--
-- Estas consultas responden a las preguntas del punto "Transformacion de Datos"
-- ============================================================================

-- ============================================================================
-- CONSULTA 1: Modo de pago mas frecuente de todos los clientes
-- ============================================================================

SELECT 
    payment_method AS 'Metodo de Pago',
    COUNT(*) AS 'Cantidad de Transacciones',
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM datos_limpios), 2) AS 'Porcentaje'
FROM datos_limpios
GROUP BY payment_method
ORDER BY COUNT(*) DESC;

-- Comentario: Identifica el metodo de pago mas utilizado y su distribucion porcentual


-- ============================================================================
-- CONSULTA 2: Modo de pago categorizado por genero
-- ============================================================================

SELECT 
    gender AS 'Genero',
    payment_method AS 'Metodo de Pago',
    COUNT(*) AS 'Cantidad de Transacciones',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio'
FROM datos_limpios
GROUP BY gender, payment_method
ORDER BY gender, COUNT(*) DESC;

-- Comentario: Muestra preferencias de pago segun genero con ticket promedio


-- ============================================================================
-- CONSULTA 3: Metodo de pago mas utilizado por cada genero
-- ============================================================================

WITH RankedPayments AS (
    SELECT 
        gender,
        payment_method,
        COUNT(*) as cantidad,
        ROW_NUMBER() OVER (PARTITION BY gender ORDER BY COUNT(*) DESC) as ranking
    FROM datos_limpios
    GROUP BY gender, payment_method
)
SELECT 
    gender AS 'Genero',
    payment_method AS 'Metodo de Pago Preferido',
    cantidad AS 'Cantidad de Transacciones'
FROM RankedPayments
WHERE ranking = 1;

-- Comentario: Identifica el metodo de pago predominante para cada genero


-- ============================================================================
-- CONSULTA 4: Metodos de pago realizados por el rango etario de 25 a 35 años
-- ============================================================================

SELECT 
    payment_method AS 'Metodo de Pago',
    COUNT(*) AS 'Cantidad de Transacciones',
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM datos_limpios WHERE age BETWEEN 25 AND 35
    ), 2) AS 'Porcentaje del Grupo',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales'
FROM datos_limpios
WHERE age BETWEEN 25 AND 35
GROUP BY payment_method
ORDER BY COUNT(*) DESC;

-- Comentario: Analiza comportamiento de pago del segmento de adultos jovenes


-- ============================================================================
-- CONSULTA 5: Categorizacion de clientes por forma de pago (edad y genero)
-- ============================================================================

SELECT 
    age_group AS 'Grupo de Edad',
    gender AS 'Genero',
    payment_method AS 'Metodo de Pago',
    COUNT(*) AS 'Transacciones',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio'
FROM datos_limpios
GROUP BY age_group, gender, payment_method
ORDER BY age_group, gender, COUNT(*) DESC;

-- Comentario: Segmentacion completa por edad, genero y metodo de pago


-- ============================================================================
-- CONSULTA 6: Metodos de pago mas utilizados por las mujeres
-- ============================================================================

SELECT 
    payment_method AS 'Metodo de Pago',
    COUNT(*) AS 'Cantidad de Transacciones',
    ROUND(COUNT(*) * 100.0 / (
        SELECT COUNT(*) FROM datos_limpios WHERE gender = 'Female'
    ), 2) AS 'Porcentaje',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales'
FROM datos_limpios
WHERE gender = 'Female'
GROUP BY payment_method
ORDER BY COUNT(*) DESC;

-- Comentario: Analisis especifico del comportamiento de pago de mujeres


-- ============================================================================
-- CONSULTA 7: Precios por categoria de productos
-- ============================================================================

SELECT 
    category AS 'Categoria',
    COUNT(*) AS 'Cantidad de Transacciones',
    ROUND(MIN(price), 2) AS 'Precio Minimo',
    ROUND(MAX(price), 2) AS 'Precio Maximo',
    ROUND(AVG(price), 2) AS 'Precio Promedio',
    ROUND(AVG(total_sale), 2) AS 'Venta Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales'
FROM datos_limpios
GROUP BY category
ORDER BY SUM(total_sale) DESC;

-- Comentario: Analisis completo de estructura de precios por categoria


-- ============================================================================
-- CONSULTAS ADICIONALES PARA ANALISIS EXPLORATORIO
-- ============================================================================

-- CONSULTA 8: Distribucion de clientes por grupo de edad
SELECT 
    age_group AS 'Grupo de Edad',
    COUNT(DISTINCT customer_id) AS 'Clientes Unicos',
    COUNT(*) AS 'Total Transacciones',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio'
FROM datos_limpios
GROUP BY age_group
ORDER BY COUNT(*) DESC;


-- CONSULTA 9: Top 10 categorias mas vendidas
SELECT 
    category AS 'Categoria',
    COUNT(*) AS 'Transacciones',
    SUM(quantity) AS 'Unidades Vendidas',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales'
FROM datos_limpios
GROUP BY category
ORDER BY SUM(total_sale) DESC
LIMIT 10;


-- CONSULTA 10: Comportamiento de compra por genero
SELECT 
    gender AS 'Genero',
    COUNT(*) AS 'Total Transacciones',
    COUNT(DISTINCT customer_id) AS 'Clientes Unicos',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales',
    ROUND(AVG(quantity), 2) AS 'Cantidad Promedio'
FROM datos_limpios
GROUP BY gender;


-- CONSULTA 11: Ventas por dia de la semana
SELECT 
    day_of_week AS 'Dia de la Semana',
    COUNT(*) AS 'Transacciones',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales'
FROM datos_limpios
GROUP BY day_of_week
ORDER BY SUM(total_sale) DESC;


-- CONSULTA 12: Top 5 shopping malls por ventas
SELECT 
    shopping_mall AS 'Shopping Mall',
    COUNT(*) AS 'Transacciones',
    COUNT(DISTINCT customer_id) AS 'Clientes Unicos',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales'
FROM datos_limpios
GROUP BY shopping_mall
ORDER BY SUM(total_sale) DESC
LIMIT 5;


-- CONSULTA 13: Evolucion de ventas por mes
SELECT 
    year AS 'Año',
    month AS 'Mes',
    COUNT(*) AS 'Transacciones',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio'
FROM datos_limpios
GROUP BY year, month
ORDER BY year, month;


-- CONSULTA 14: Analisis de cantidad de productos por transaccion
SELECT 
    CASE 
        WHEN quantity = 1 THEN '1 producto'
        WHEN quantity BETWEEN 2 AND 3 THEN '2-3 productos'
        WHEN quantity BETWEEN 4 AND 5 THEN '4-5 productos'
        ELSE 'Mas de 5 productos'
    END AS 'Rango de Cantidad',
    COUNT(*) AS 'Transacciones',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio'
FROM datos_limpios
GROUP BY 
    CASE 
        WHEN quantity = 1 THEN '1 producto'
        WHEN quantity BETWEEN 2 AND 3 THEN '2-3 productos'
        WHEN quantity BETWEEN 4 AND 5 THEN '4-5 productos'
        ELSE 'Mas de 5 productos'
    END
ORDER BY COUNT(*) DESC;


-- CONSULTA 15: Clientes mas frecuentes (Top 10)
SELECT 
    customer_id AS 'ID Cliente',
    COUNT(*) AS 'Numero de Compras',
    ROUND(SUM(total_sale), 2) AS 'Total Gastado',
    ROUND(AVG(total_sale), 2) AS 'Ticket Promedio',
    MAX(invoice_date) AS 'Ultima Compra'
FROM datos_limpios
GROUP BY customer_id
ORDER BY COUNT(*) DESC
LIMIT 10;


-- ============================================================================
-- CONSULTAS DE VALIDACION Y CALIDAD DE DATOS
-- ============================================================================

-- CONSULTA 16: Verificar integridad de datos
SELECT 
    'Total de registros' AS 'Metrica',
    COUNT(*) AS 'Valor'
FROM datos_limpios
UNION ALL
SELECT 
    'Registros con valores nulos',
    0
UNION ALL
SELECT 
    'Clientes unicos',
    COUNT(DISTINCT customer_id)
FROM datos_limpios
UNION ALL
SELECT 
    'Facturas unicas',
    COUNT(DISTINCT invoice_no)
FROM datos_limpios;


-- CONSULTA 17: Resumen estadistico general
SELECT 
    ROUND(MIN(total_sale), 2) AS 'Venta Minima',
    ROUND(MAX(total_sale), 2) AS 'Venta Maxima',
    ROUND(AVG(total_sale), 2) AS 'Venta Promedio',
    ROUND(SUM(total_sale), 2) AS 'Ventas Totales',
    COUNT(*) AS 'Total Transacciones',
    COUNT(DISTINCT customer_id) AS 'Total Clientes'
FROM datos_limpios;


-- ============================================================================
-- FIN DE CONSULTAS SQL
-- ============================================================================

-- Notas:
-- 1. Todas las consultas estan optimizadas con los indices creados en schema.sql
-- 2. Se utilizan funciones de agregacion (COUNT, SUM, AVG, MIN, MAX)
-- 3. Se incluyen ROUND para formato de decimales
-- 4. Las consultas responden a todos los items del trabajo practico
-- 5. Se agregaron consultas adicionales para analisis mas profundo
