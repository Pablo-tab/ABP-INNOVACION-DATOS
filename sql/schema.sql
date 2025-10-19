-- ============================================================================
-- TRABAJO PRACTICO: PROCESO ETL - ANALISIS DE DATOS DE VENTAS Y CLIENTES
-- TSCDIA 2025
-- 
-- Integrantes:
-- - Paola Garcia (DNI: 29463402)
-- - Pablo Taborda (DNI: 28270596)
-- - Julio Orjindo (DNI: 26482639)
-- - Rodenas Elias Gabriel (DNI: 36356976)
--
-- Asignatura: Innovacion de Datos
-- Profesores: Alejandro Mainero, Carlos Charletti
-- ============================================================================

-- Crear base de datos (SQLite creara automaticamente el archivo .db)
-- Para otros motores como MariaDB/MySQL, descomentar la siguiente linea:
-- CREATE DATABASE IF NOT EXISTS ventas_estambul;
-- USE ventas_estambul;

-- ============================================================================
-- TABLA: datos_limpios
-- Contiene toda la informacion del proceso ETL con datos integrados
-- ============================================================================

DROP TABLE IF EXISTS datos_limpios;

CREATE TABLE datos_limpios (
    -- Identificadores
    invoice_no VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    
    -- Datos demograficos del cliente
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('Male', 'Female')),
    age INTEGER NOT NULL CHECK (age >= 18 AND age <= 100),
    age_group VARCHAR(30) NOT NULL,
    
    -- Informacion de pago
    payment_method VARCHAR(20) NOT NULL CHECK (payment_method IN ('Cash', 'Credit Card', 'Debit Card')),
    
    -- Informacion del producto
    category VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL CHECK (quantity > 0),
    price DECIMAL(10, 2) NOT NULL CHECK (price >= 0),
    total_sale DECIMAL(10, 2) NOT NULL CHECK (total_sale >= 0),
    
    -- Informacion temporal
    invoice_date DATE NOT NULL,
    year INTEGER NOT NULL,
    month INTEGER NOT NULL CHECK (month >= 1 AND month <= 12),
    day_of_week VARCHAR(10) NOT NULL,
    
    -- Ubicacion
    shopping_mall VARCHAR(100) NOT NULL,
    
    -- Restricciones
    PRIMARY KEY (invoice_no)
);

-- ============================================================================
-- INDICES PARA OPTIMIZAR CONSULTAS
-- ============================================================================

CREATE INDEX idx_customer_id ON datos_limpios(customer_id);
CREATE INDEX idx_payment_method ON datos_limpios(payment_method);
CREATE INDEX idx_gender ON datos_limpios(gender);
CREATE INDEX idx_age ON datos_limpios(age);
CREATE INDEX idx_age_group ON datos_limpios(age_group);
CREATE INDEX idx_category ON datos_limpios(category);
CREATE INDEX idx_invoice_date ON datos_limpios(invoice_date);
CREATE INDEX idx_shopping_mall ON datos_limpios(shopping_mall);

-- ============================================================================
-- COMENTARIOS SOBRE EL ESQUEMA
-- ============================================================================

-- Restricciones de integridad implementadas:
-- 1. PRIMARY KEY en invoice_no: Garantiza unicidad de cada transaccion
-- 2. NOT NULL: Campos criticos no pueden ser nulos
-- 3. CHECK en gender: Solo permite valores 'Male' o 'Female'
-- 4. CHECK en age: Rango valido entre 18 y 100 años
-- 5. CHECK en payment_method: Solo metodos validos (Cash, Credit Card, Debit Card)
-- 6. CHECK en quantity: Debe ser mayor a 0
-- 7. CHECK en price y total_sale: No pueden ser negativos
-- 8. CHECK en month: Rango valido de 1 a 12

-- Indices creados para optimizar:
-- - Busquedas por cliente (customer_id)
-- - Filtros por metodo de pago, genero, edad
-- - Agrupaciones por categoria y ubicacion
-- - Consultas temporales por fecha

-- ============================================================================
-- FIN DEL ESQUEMA
-- ============================================================================
