# DATA MODEL SPECIFICATION DOCUMENT
## WORKFORCE DYNAMIC LENS – PEOPLE ANALYTICS & WORKFORCE DYNAMICS SOLUTION

**Document Version:** v0.5.0 (People Analytics / HR Data Analyst Portfolio Baseline)  
**Target Audience:** People Analytics Leaders, HR Data Analysts, BI Developers, Solution Reviewers, Recruiters  
**Project Author:** Emmanuel Rodríguez Mendoza  
**Professional Role:** People Analytics / HR Data Analyst  
**Project:** Workforce Dynamic Lens  
**Date:** August 2026  
**Status:** Final Data Model Baseline  

---

## 1. Overview & Scope

El **Data Model Specification Document (v0.5.0)** establece la arquitectura lógica y física del modelo de datos dimensional para la plataforma **Workforce Dynamic Lens**. Este documento traduce los requerimientos de negocio en un esquema optimizado para consultas analíticas (OLAP), cálculo de indicadores de People Analytics, consultas avanzadas en SQL y tableros interactivos en Power BI.

### 1.1 Objective & Alignment
El objetivo es construir un **Modelo Dimensional en Estrella (Star Schema)** sobre PostgreSQL 16+, diseñado para responder a las preguntas de negocio sobre rotación, ausentismo, equidad salarial e impacto financiero en una organización de **4,500 colaboradores activos** y **1,200 registros históricos** en LATAM y Europa.

```text
┌──────────────────────────────────────────────────────────────────────────┐
│ MODEL SUMMARY                                                            │
├──────────────────────────────┬───────────────────────────────────────────┤
│ Database Engine              │ PostgreSQL 16+ (ANSI SQL)                 │
│ Schema Name                  │ people_analytics                          │
│ Architecture Pattern         │ Kimball Dimensional Modeling (Star Schema)│
│ Keying Strategy              │ Surrogate Keys (BIGINT) + Natural Keys    │
│ Primary Focus                │ People Analytics, BI & Executive Decision │
└──────────────────────────────┴───────────────────────────────────────────┘
```

---

## 2. Modeling Philosophy

El diseño adopta la metodología de **Modelado Dimensional de Ralph Kimball**, priorizando la velocidad de lectura, la simplicidad de las consultas DAX/SQL y la claridad analítica sobre la normalización académica.

### 2.1 Why Star Schema (Kimball)?
1. **Rendimiento de Consultas OLAP:** Reduce la necesidad de realizar uniones (*JOINs*) complejas entre múltiples tablas normalizadas, acelerando la carga de paneles en Power BI.
2. **Simplicidad en DAX:** Un modelo en estrella con relaciones de `1:N` unidireccionales simplifica el filtrado y evita comportamientos ambiguos en las medidas de Power BI.
3. **Claridad para el Análisis:** Agrupa métricas numéricas en tablas de hechos y atributos descriptivos en tablas de dimensión.

### 2.2 Surrogate Keys vs. Natural Keys
* **Natural Keys (NK):** Identificadores del sistema de origen (ej. `employee_id = 'EMP01420'`). Se conservan como atributos de negocio para trazabilidad.
* **Surrogate Keys (SK):** Claves primarias sintéticas (`BIGINT GENERATED ALWAYS AS IDENTITY`, ej. `employee_sk = 1042`).
  * *Propósito:* Desacopla la base analítica de cambios en los sistemas fuente y permite gestionar el historial de cambios (**SCD Tipo 2**).

### 2.3 Slowly Changing Dimensions (SCD) Strategy
* **SCD Type 1 (Overwrite):** Para correcciones de datos o atributos sin historial relevante (ej. `first_name`, `last_name`, `work_email`).
* **SCD Type 2 (Add New Row):** Para cambios en variables clave de carrera y compensación (`annual_base_salary_usd`, `department_sk`, `position_sk`). Cada cambio genera un nuevo registro controlado por `row_effective_date`, `row_expiration_date` e `is_current_row`.

### 2.4 Conformed Dimensions
Las dimensiones `dim_departments`, `dim_positions` y `dim_employees` son **Dimensiones Conformadas** conectadas a las tres tablas de hechos (`fact_attendance_logs`, `fact_terminations`, `fact_sla_events`). Esto permite cruzar eventos de ausentismo y penalizaciones con datos de compensación y estructura organizacional.

---

## 3. Conceptual Data Model

```text
┌─────────────────┐       ┌─────────────────┐       ┌──────────────────────┐
│  dim_positions  │       │ dim_departments │       │dim_salary_benchmarks │
└────────┬────────┘       └────────┬────────┘       └──────────┬───────────┘
         │ 1                       │ 1                         │ 1
         │                         │                           │
         │ N                       │ N                         │ N
┌────────┴─────────────────────────┴───────────────────────────┴───────────┐
│                              dim_employees                               │
└────────┬─────────────────────────┬───────────────────────────┬───────────┘
         │ 1                       │ 1                         │ 1
         │                         │                           │
         │ N                       │ N                         │ N
┌────────┴────────┐       ┌────────┴────────┐       ┌──────────┴───────────┐
│fact_attendance_ │       │fact_terminations│       │   fact_sla_events    │
│      logs       │       │                 │       │                      │
└─────────────────┘       └─────────────────┘       └──────────────────────┘
```

---

## 4. Logical Data Model

```text
┌───────────────────────────────────┐       ┌───────────────────────────────────┐
│          dim_departments          │       │           dim_positions           │
├───────────────────────────────────┤       ├───────────────────────────────────┤
│ PK  department_sk : BIGINT        │       │ PK  position_sk : BIGINT          │
│ NK  department_id : VARCHAR(10)   │       │ NK  position_id : VARCHAR(10)     │
│     department_name : VARCHAR(100)│       │     job_title : VARCHAR(100)      │
│     cost_center_code : VARCHAR(20)│       │     job_family : VARCHAR(50)      │
│     vp_responsible : VARCHAR(100) │       │     job_grade : VARCHAR(10)       │
│     region : VARCHAR(20)          │       │     career_level : VARCHAR(20)    │
│     target_headcount : INT        │       │     is_critical_position : SMALLINT│
└─────────────────┬─────────────────┘       └─────────────────┬─────────────────┘
                  │ 1                                         │ 1
                  │                                           │
                  │ N                                         │ N
┌─────────────────┴───────────────────────────────────────────┴─────────────────┐
│                                 dim_employees                                 │
├───────────────────────────────────────────────────────────────────────────────┤
│ PK  employee_sk : BIGINT                                                      │
│ NK  employee_id : VARCHAR(10)                                                 │
│ FK  department_sk : BIGINT                                                    │
│ FK  position_sk : BIGINT                                                      │
│     first_name : VARCHAR(50)                                                  │
│     last_name : VARCHAR(50)                                                   │
│     work_email : VARCHAR(100)                                                 │
│     gender : VARCHAR(20)                                                      │
│     hire_date : DATE                                                          │
│     country_code : VARCHAR(3)                                                 │
│     annual_base_salary_usd : NUMERIC(12,2)                                   │
│     fully_loaded_cost_usd : NUMERIC(12,2)                                    │
│     performance_rating : NUMERIC(3,2)                                         │
│     is_active : SMALLINT                                                      │
│     is_current_row : SMALLINT (SCD2)                                          │
│     row_effective_date : DATE (SCD2)                                          │
│     row_expiration_date : DATE (SCD2)                                         │
└─────────────────┬───────────────────────────┬─────────────────────────┬───────┘
                  │ 1                         │ 1                       │ 1
                  │                           │                         │
                  │ N                         │ N                       │ N
┌─────────────────┴───────────┐   ┌───────────┴───────────┐   ┌─────────┴─────────────────┐
│    fact_attendance_logs     │   │   fact_terminations   │   │     fact_sla_events       │
├─────────────────────────────┤   ├───────────────────────┤   ├───────────────────────────┤
│ PK  attendance_id : BIGINT  │   │ PK  termination_id    │   │ PK  sla_event_id : BIGINT │
│ FK  employee_sk : BIGINT    │   │ FK  employee_sk       │   │ FK  department_sk : BIGINT│
│     date_key : DATE         │   │     termination_date  │   │     event_date : DATE     │
│     planned_hours : NUMERIC │   │     termination_type  │   │     penalty_cost_usd      │
│     actual_hours : NUMERIC  │   │     severance_cost    │   │     attributed_to_staffing│
│     overtime_hours : NUMERIC│   │     is_regrettable    │   │     _deficit : SMALLINT   │
└─────────────────────────────┘   └───────────────────────┘   └───────────────────────────┘
```

---

## 5. Complete Star Schema (Physical View)

```text
┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ POSTGRESQL STAR SCHEMA                                                                                                 │
├────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                                                        │
│  dim_departments                                                                                                       │
│  (PK department_sk) ──────┐                                                                                            │
│                           │ 1:N                                                                                        │
│  dim_positions            │                                                                                            │
│  (PK position_sk) ────────┼──────────┐                                                                                 │
│                           │ 1:N      │ 1:N                                                                             │
│                           ▼          ▼                                                                                 │
│                    ┌─────────────────────────┐                                                                         │
│                    │      dim_employees      │◄────────── dim_salary_benchmarks                                   │
│                    │  (PK employee_sk)       │  1:N       (PK benchmark_sk, FK position_sk)                            │
│                    └──────────┬──────────────┘                                                                         │
│                               │                                                                                        │
│           ┌───────────────────┼───────────────────┐                                                                    │
│           │ 1:N               │ 1:N               │ 1:N                                                                │
│           ▼                   ▼                   ▼                                                                    │
│  fact_attendance_logs     fact_terminations   fact_sla_events                                                      │
│  (PK attendance_id,       (PK termination_id, (PK sla_event_id,                                                        │
│   FK employee_sk)          FK employee_sk)     FK department_sk)                                                       │
│                                                                                                                        │
└────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Table Specifications & Grain Declarations

### 6.1 Dimension Table: `dim_employees`
* **Propósito de Negocio:** Dimensión maestra de colaboradores con historial de cargos, salarios y departamentos.
* **Declaración de Granularidad:** **Una fila representa el estado de un colaborador durante un intervalo de tiempo específico** (`row_effective_date` a `row_expiration_date`).
* **Estrategia SCD:** **SCD Tipo 2** (`annual_base_salary_usd`, `department_sk`, `position_sk`), **SCD Tipo 1** (`first_name`, `last_name`, `work_email`).
* **Keys:** Primary Key: `employee_sk` (`BIGINT`), Natural Key: `employee_id` (`VARCHAR(10)`).
* **Data Lineage:** `HRIS Core` → `raw_employees` → `stg_employees` → `dim_employees`.
* **Volumen:** ~4,500 colaboradores activos + ~1,200 registros históricos.

### 6.2 Dimension Table: `dim_departments`
* **Propósito de Negocio:** Estructura organizacional, centros de costo, presupuestos y VPs responsables.
* **Declaración de Granularidad:** **Una fila representa un departamento o área funcional activa**.
* **Estrategia SCD:** **SCD Tipo 1**.
* **Keys:** Primary Key: `department_sk` (`BIGINT`), Natural Key: `department_id` (`VARCHAR(10)`).
* **Data Lineage:** `HRIS Org Catalog` → `dim_departments`.
* **Volumen:** 15 - 25 filas.

### 6.3 Dimension Table: `dim_positions`
* **Propósito de Negocio:** Catálogo de puestos, familias profesionales, niveles de carrera e índice de escasez.
* **Declaración de Granularidad:** **Una fila representa un perfil de puesto formal en la compañía**.
* **Estrategia SCD:** **SCD Tipo 1**.
* **Keys:** Primary Key: `position_sk` (`BIGINT`), Natural Key: `position_id` (`VARCHAR(10)`).
* **Data Lineage:** `Job Architecture Catalog` → `dim_positions`.
* **Volumen:** 80 - 150 filas.

### 6.4 Reference Table: `dim_salary_benchmarks`
* **Propósito de Negocio:** Puntos medios salariales de mercado (Percentiles P25, P50, P75) por puesto, país y año.
* **Declaración de Granularidad:** **Una fila representa un estudio salarial para un puesto en un país y año fiscal específico**.
* **Keys:** Primary Key: `benchmark_sk` (`BIGINT`), Natural Key: `benchmark_id` (`VARCHAR(15)`).
* **Data Lineage:** `External Market Intel Feed` → `dim_salary_benchmarks`.
* **Volumen:** 300 - 500 filas.

### 6.5 Fact Table: `fact_attendance_logs`
* **Propósito de Negocio:** Registro diario de asistencia, marcas de tiempo, ausencias y horas extra.
* **Declaración de Granularidad:** **Una fila representa el registro diario de asistencia de un colaborador en un día calendario**.
* **Keys:** Primary Key: `attendance_id` (`BIGINT`), Foreign Key: `employee_sk` → `dim_employees(employee_sk)`.
* **Data Lineage:** `Time Tracker Logs` → `fact_attendance_logs`.
* **Volumen:** ~1.6 Millones de filas por año (4,500 empleados × 365 días).

### 6.6 Fact Table: `fact_terminations`
* **Propósito de Negocio:** Eventos de egreso, costos de liquidación, causa reportada y causa proxy corregida.
* **Declaración de Granularidad:** **Una fila representa el evento único de salida voluntaria o involuntaria de un colaborador**.
* **Keys:** Primary Key: `termination_id` (`BIGINT`), Foreign Key: `employee_sk` → `dim_employees(employee_sk)`.
* **Data Lineage:** `HRIS Termination Workflow` → `fact_terminations`.
* **Volumen:** ~1,200 filas históricas + ~450 salidas anuales.

### 6.7 Fact Table: `fact_sla_events`
* **Propósito de Negocio:** Penalizaciones financieras B2B atribuibles a déficit de personal en operaciones.
* **Declaración de Granularidad:** **Una fila representa un evento discreto de penalización por SLA en un turno y contrato**.
* **Keys:** Primary Key: `sla_event_id` (`BIGINT`), Foreign Key: `department_sk` → `dim_departments(department_sk)`.
* **Data Lineage:** `Service Desk CRM` → `fact_sla_events`.
* **Volumen:** 100 - 300 eventos anuales.

---

## 7. Relationship Matrix & Cardinality

| Tabla Padre (PK) | Tabla Hija (FK) | Cardinalidad | Columna Join (Padre) | Columna Join (Hija) |
| :--- | :--- | :--- | :--- | :--- |
| `dim_departments` | `dim_employees` | 1 : N | `department_sk` | `department_sk` |
| `dim_positions` | `dim_employees` | 1 : N | `position_sk` | `position_sk` |
| `dim_positions` | `dim_salary_benchmarks` | 1 : N | `position_sk` | `position_sk` |
| `dim_employees` | `fact_attendance_logs` | 1 : N | `employee_sk` | `employee_sk` |
| `dim_employees` | `fact_terminations` | 1 : N (0..1) | `employee_sk` | `employee_sk` |
| `dim_departments` | `fact_sla_events` | 1 : N | `department_sk` | `department_sk` |

---

## 8. Indexing Strategy & Performance

Para asegurar que los tableros en Power BI respondan de manera fluida y las consultas SQL de análisis ejecuten rápidamente, se definen los siguientes índices B-Tree:

* **Natural Key Lookups:** Índice B-Tree en `dim_employees(employee_id, is_current_row)`.
* **Foreign Key Joins:** Índices B-Tree en claves foráneas de tablas de hechos (`fact_attendance_logs(employee_sk)`, `fact_terminations(employee_sk)`).
* **Composite Filtering:** Índice compuesto en `fact_attendance_logs(employee_sk, date_key)` e índice parcial en `fact_attendance_logs(employee_sk) WHERE is_unplanned_absence = 1` para optimizar el cálculo del Factor de Bradford (`BR-06`).

---

## 9. Scalability Strategy

* **Current Scope (4,500 Employees):** Manejo eficiente en una instancia estándar de PostgreSQL mediante el modelo en estrella propuesto.
* **Future Scope (up to 50,000 Employees):** Si la empresa se expande, la arquitectura soportará crecimiento mediante la adición de índices compuestos y particionamiento mensual en `fact_attendance_logs` sin cambiar la estructura lógica.

---

## 10. Architecture Decision Record (ADR-001)

### ADR-001: Adoption of Kimball Star Schema Design
* **Status:** Approved
* **Context:** Se necesita un modelo de datos analítico para calcular indicadores clave (rotación, ausentismo, equidad salarial) y alimentar Power BI sin sobrecargar la base de datos con uniones complejas.
* **Decision:** Adoptar un diseño Dimensional en Estrella (Star Schema) con 3 dimensiones conformadas y 3 tablas de hechos.
* **Consequences:** Facilita la creación de medidas DAX en Power BI, optimiza la velocidad de filtrado y separa las lecturas analíticas de los sistemas operacionales de origen.

---

## 11. Traceability Matrix

| Requirement ID | Target Entity | Column | Target KPI | Core Dashboard View |
| :--- | :--- | :--- | :--- | :--- |
| FR-01 / FR-06 | `dim_employees` | `employee_id`, `employee_sk` | Master ID | HRBP Action Center |
| FR-08 / FR-21 | `dim_employees` | `annual_base_salary_usd` | KPI-HR-02 (Compa-Ratio) | Financial What-If Sim |
| FR-10 / FR-11 | `fact_terminations` | `is_regrettable_attrition` | KPI-EXEC-01 (HP Retention) | Boardroom Overview |
| FR-16 / FR-17 | `fact_attendance_logs` | `is_absence_instance_start` | KPI-OP-01 (Bradford Score) | HRBP Action Center |
| FR-27 | `fact_sla_events` | `penalty_cost_usd` | KPI-FIN-02 (SLA Penalty) | Boardroom Overview |

---

## 12. SQL Codebase Structure

Para mantener la separación profesional entre la documentación y el código fuente ejecutable, los scripts DDL en SQL se organizan en el directorio `sql/` del repositorio de la siguiente manera:

* `sql/01_create_schema.sql`: Creación del esquema `people_analytics`.
* `sql/02_create_dimensions.sql`: Tablas de dimensión (`dim_departments`, `dim_positions`, `dim_employees`, `dim_salary_benchmarks`).
* `sql/03_create_facts.sql`: Tablas de hechos (`fact_attendance_logs`, `fact_terminations`, `fact_sla_events`).
* `sql/04_indexes.sql`: Creación de índices B-Tree y restricciones de calidad (`CHECK`, `FK`).
* `sql/05_views.sql`: Vistas analíticas y agregaciones precalculadas.

### 12.1 `sql/01_create_schema.sql`

```sql
-- ============================================================================
-- SCRIPT 01: SCHEMA CREATION
-- Target Engine: PostgreSQL 16+
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS people_analytics;
SET search_path TO people_analytics, public;
```

### 12.2 `sql/02_create_dimensions.sql`

```sql
-- ============================================================================
-- SCRIPT 02: DIMENSION TABLES
-- Target Engine: PostgreSQL 16+
-- Schema: people_analytics
-- ============================================================================

SET search_path TO people_analytics, public;

-- 1. DIMENSION: DEPARTMENTS
CREATE TABLE IF NOT EXISTS dim_departments (
    department_sk       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_id       VARCHAR(10) NOT NULL UNIQUE,
    department_name     VARCHAR(100) NOT NULL,
    cost_center_code    VARCHAR(20) NOT NULL,
    vp_responsible      VARCHAR(100) NOT NULL,
    region              VARCHAR(20) NOT NULL,
    budget_annual_usd   NUMERIC(14,2) NOT NULL CHECK (budget_annual_usd > 0),
    target_headcount    INT NOT NULL CHECK (target_headcount > 0),
    strategic_level     VARCHAR(20) NOT NULL
);

-- 2. DIMENSION: POSITIONS
CREATE TABLE IF NOT EXISTS dim_positions (
    position_sk         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    position_id         VARCHAR(10) NOT NULL UNIQUE,
    job_title           VARCHAR(100) NOT NULL,
    job_family          VARCHAR(50) NOT NULL,
    job_grade           VARCHAR(10) NOT NULL,
    career_level        VARCHAR(20) NOT NULL,
    is_critical_position SMALLINT NOT NULL DEFAULT 0 CHECK (is_critical_position IN (0, 1)),
    is_remote_eligible  SMALLINT NOT NULL DEFAULT 0 CHECK (is_remote_eligible IN (0, 1)),
    market_scarcity_index NUMERIC(3,2) NOT NULL CHECK (market_scarcity_index BETWEEN 1.00 AND 3.00)
);

-- 3. DIMENSION: EMPLOYEES (SCD TYPE 2)
CREATE TABLE IF NOT EXISTS dim_employees (
    employee_sk         BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_id         VARCHAR(10) NOT NULL,
    first_name          VARCHAR(50) NOT NULL,
    last_name           VARCHAR(50) NOT NULL,
    work_email          VARCHAR(100) NOT NULL,
    gender              VARCHAR(20) NOT NULL,
    birth_date          DATE NOT NULL,
    hire_date           DATE NOT NULL,
    department_sk       BIGINT NOT NULL REFERENCES dim_departments(department_sk),
    position_sk         BIGINT NOT NULL REFERENCES dim_positions(position_sk),
    country_code        VARCHAR(3) NOT NULL,
    work_location_type  VARCHAR(20) NOT NULL,
    base_salary_orig    NUMERIC(12,2) NOT NULL CHECK (base_salary_orig > 0),
    salary_currency_orig VARCHAR(3) NOT NULL,
    annual_base_salary_usd NUMERIC(12,2) NOT NULL CHECK (annual_base_salary_usd > 0),
    fully_loaded_cost_usd NUMERIC(12,2) NOT NULL CHECK (fully_loaded_cost_usd > 0),
    performance_rating  NUMERIC(3,2) CHECK (performance_rating BETWEEN 1.00 AND 5.00),
    potential_rating    VARCHAR(10),
    is_active           SMALLINT NOT NULL DEFAULT 1 CHECK (is_active IN (0, 1)),
    is_current_row      SMALLINT NOT NULL DEFAULT 1 CHECK (is_current_row IN (0, 1)),
    row_effective_date  DATE NOT NULL DEFAULT CURRENT_DATE,
    row_expiration_date  DATE DEFAULT '9999-12-31' NOT NULL
);

-- 4. REFERENCE DIMENSION: SALARY BENCHMARKS
CREATE TABLE IF NOT EXISTS dim_salary_benchmarks (
    benchmark_sk        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    benchmark_id        VARCHAR(15) NOT NULL UNIQUE,
    position_sk         BIGINT NOT NULL REFERENCES dim_positions(position_sk),
    country_code        VARCHAR(3) NOT NULL,
    market_min_salary_usd NUMERIC(12,2) NOT NULL CHECK (market_min_salary_usd > 0),
    market_midpoint_salary_usd NUMERIC(12,2) NOT NULL CHECK (market_midpoint_salary_usd > market_min_salary_usd),
    market_max_salary_usd NUMERIC(12,2) NOT NULL CHECK (market_max_salary_usd > market_midpoint_salary_usd),
    survey_provider     VARCHAR(50) NOT NULL,
    effective_year      INT NOT NULL CHECK (effective_year BETWEEN 2020 AND 2030)
);
```

### 12.3 `sql/03_create_facts.sql`

```sql
-- ============================================================================
-- SCRIPT 03: FACT TABLES
-- Target Engine: PostgreSQL 16+
-- Schema: people_analytics
-- ============================================================================

SET search_path TO people_analytics, public;

-- 1. FACT: ATTENDANCE LOGS
CREATE TABLE IF NOT EXISTS fact_attendance_logs (
    attendance_id       BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_sk         BIGINT NOT NULL REFERENCES dim_employees(employee_sk),
    date_key            DATE NOT NULL,
    shift_type          VARCHAR(20) NOT NULL,
    clock_in_time       TIMESTAMP WITH TIME ZONE,
    clock_out_time      TIMESTAMP WITH TIME ZONE,
    planned_hours       NUMERIC(4,2) NOT NULL CHECK (planned_hours >= 0),
    actual_hours_worked NUMERIC(4,2) NOT NULL CHECK (actual_hours_worked >= 0),
    overtime_hours      NUMERIC(4,2) NOT NULL CHECK (overtime_hours >= 0),
    absence_type        VARCHAR(30),
    is_unplanned_absence SMALLINT NOT NULL DEFAULT 0 CHECK (is_unplanned_absence IN (0, 1)),
    is_absence_instance_start SMALLINT NOT NULL DEFAULT 0 CHECK (is_absence_instance_start IN (0, 1))
);

-- 2. FACT: TERMINATIONS
CREATE TABLE IF NOT EXISTS fact_terminations (
    termination_id      BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    employee_sk         BIGINT NOT NULL REFERENCES dim_employees(employee_sk),
    termination_date    DATE NOT NULL,
    termination_type    VARCHAR(20) NOT NULL,
    hris_exit_reason    VARCHAR(100) NOT NULL,
    proxy_reclassified_reason VARCHAR(100) NOT NULL,
    severance_cost_usd  NUMERIC(12,2) NOT NULL CHECK (severance_cost_usd >= 0),
    notice_period_days  INT NOT NULL CHECK (notice_period_days >= 0),
    is_regrettable_attrition SMALLINT NOT NULL DEFAULT 0 CHECK (is_regrettable_attrition IN (0, 1))
);

-- 3. FACT: SLA EVENTS
CREATE TABLE IF NOT EXISTS fact_sla_events (
    sla_event_id        BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    department_sk       BIGINT NOT NULL REFERENCES dim_departments(department_sk),
    client_contract_id  VARCHAR(20) NOT NULL,
    event_date          DATE NOT NULL,
    shift_id            VARCHAR(20) NOT NULL,
    breach_type         VARCHAR(50) NOT NULL,
    hours_delayed       NUMERIC(4,2) NOT NULL CHECK (hours_delayed > 0),
    penalty_cost_usd    NUMERIC(10,2) NOT NULL CHECK (penalty_cost_usd > 0),
    attributed_to_staffing_deficit SMALLINT NOT NULL DEFAULT 0 CHECK (attributed_to_staffing_deficit IN (0, 1))
);
```

### 12.4 `sql/04_indexes.sql`

```sql
-- ============================================================================
-- SCRIPT 04: INDEXES & PERFORMANCE TUNING
-- Target Engine: PostgreSQL 16+
-- Schema: people_analytics
-- ============================================================================

SET search_path TO people_analytics, public;

-- Natural Key & SCD Indexes
CREATE INDEX IF NOT EXISTS idx_dim_emp_natural_id ON dim_employees (employee_id, is_current_row);
CREATE INDEX IF NOT EXISTS idx_dim_emp_dept_pos ON dim_employees (department_sk, position_sk);

-- Fact Foreign Key & Filter Indexes
CREATE INDEX IF NOT EXISTS idx_fact_att_emp_date ON fact_attendance_logs (employee_sk, date_key);
CREATE INDEX IF NOT EXISTS idx_fact_att_bradford ON fact_attendance_logs (employee_sk, date_key) WHERE is_unplanned_absence = 1;
CREATE INDEX IF NOT EXISTS idx_fact_term_emp ON fact_terminations (employee_sk);
CREATE INDEX IF NOT EXISTS idx_fact_sla_dept_date ON fact_sla_events (department_sk, event_date);
```

### 12.5 `sql/05_views.sql`

```sql
-- ============================================================================
-- SCRIPT 05: ANALYTICAL VIEWS
-- Target Engine: PostgreSQL 16+
-- Schema: people_analytics
-- ============================================================================

SET search_path TO people_analytics, public;

CREATE OR REPLACE VIEW view_monthly_attrition_summary AS
SELECT 
    d.department_name,
    DATE_TRUNC('month', t.termination_date)::DATE AS month_start,
    COUNT(*) FILTER (WHERE t.termination_type = 'Voluntaria') AS voluntary_exits,
    COUNT(*) FILTER (WHERE t.is_regrettable_attrition = 1) AS high_performer_exits,
    SUM(t.severance_cost_usd) AS total_severance_cost_usd
FROM fact_terminations t
JOIN dim_employees e ON t.employee_sk = e.employee_sk
JOIN dim_departments d ON e.department_sk = d.department_sk
GROUP BY d.department_name, DATE_TRUNC('month', t.termination_date);
```
